#!/usr/bin/env python3
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = os.environ.get("WIKI_API", "https://enthusia.miraheze.org/w/api.php")
OUT = Path(os.environ.get("WIKI_BACKUP_DIR", "wiki-preservation-output"))
USER_AGENT = "EnthusiaWikiPreserver/1.0 (read-only pre-redesign backup)"


def request(params, method="GET", retries=4):
    full = {"format": "json", "formatversion": "2", "maxlag": "5", **params}
    data = None
    url = API
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if method == "POST":
        data = urllib.parse.urlencode(full).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    else:
        url = API + "?" + urllib.parse.urlencode(full)

    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                payload = response.read()
                result = json.loads(payload.decode("utf-8"))
                if "error" in result:
                    code = result["error"].get("code")
                    if code == "maxlag" and attempt + 1 < retries:
                        time.sleep(2 + attempt * 2)
                        continue
                    raise RuntimeError(f"MediaWiki API error: {json.dumps(result['error'], ensure_ascii=False)}")
                return result
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt + 1 < retries:
                time.sleep(2 + attempt * 2)
                continue
            raise RuntimeError(f"HTTP {exc.code} from MediaWiki API: {body[:1000]}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt + 1 < retries:
                time.sleep(2 + attempt * 2)
                continue
            raise RuntimeError(f"Unable to reach MediaWiki API: {exc}") from exc
    raise RuntimeError("MediaWiki request exhausted retries")


def safe_name(title):
    readable = title.replace("/", "∕")
    readable = re.sub(r'[<>:"\\|?*\x00-\x1f]', "_", readable)[:120]
    digest = hashlib.sha256(title.encode("utf-8")).hexdigest()[:10]
    return f"{readable or 'page'}--{digest}"


def parse_wiki(content):
    links = []
    categories = []
    templates = []
    headings = []

    for match in re.finditer(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]*)?\]\]", content):
        target = match.group(1).strip()
        if target.lower().startswith("category:"):
            categories.append(target.split(":", 1)[1].strip())
        elif not re.match(r"^(file|image|media):", target, flags=re.I):
            links.append(target)

    for match in re.finditer(r"^(={2,6})\s*(.*?)\s*\1\s*$", content, flags=re.M):
        headings.append({"level": len(match.group(1)), "text": match.group(2).strip()})

    for match in re.finditer(r"\{\{\s*([^{}|#]+?)(?:\||\}\})", content):
        templates.append(match.group(1).strip())

    return {
        "links": sorted(set(links)),
        "headings": headings,
        "categories": sorted(set(categories)),
        "templates": sorted(set(templates)),
    }


def list_all_pages(namespace_id):
    pages = []
    cont = {}
    while True:
        result = request({
            "action": "query",
            "list": "allpages",
            "apnamespace": str(namespace_id),
            "aplimit": "max",
            **cont,
        })
        pages.extend(result.get("query", {}).get("allpages", []))
        cont = result.get("continue")
        if not cont:
            return pages


def fetch_current_pages(titles):
    pages = []
    for index in range(0, len(titles), 25):
        batch = titles[index:index + 25]
        result = request({
            "action": "query",
            "prop": "revisions|info",
            "titles": "|".join(batch),
            "rvprop": "ids|timestamp|user|comment|content|contentmodel",
            "rvslots": "main",
            "inprop": "url",
        }, method="POST")
        pages.extend(result.get("query", {}).get("pages", []))
    return pages


def fetch_history(title):
    revisions = []
    cont = {}
    while True:
        result = request({
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "ids|timestamp|user|userid|comment|size|flags|tags",
            "rvlimit": "max",
            "rvdir": "newer",
            **cont,
        }, method="POST")
        page_list = result.get("query", {}).get("pages", [])
        if page_list:
            revisions.extend(page_list[0].get("revisions", []))
        cont = result.get("continue")
        if not cont:
            return revisions


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "pages").mkdir(parents=True)
    (OUT / "history").mkdir(parents=True)

    site = request({
        "action": "query",
        "meta": "siteinfo",
        "siprop": "general|namespaces|namespacealiases",
    })
    query = site.get("query", {})
    namespaces_raw = query.get("namespaces", {})
    namespaces = []
    for ns in namespaces_raw.values():
        ns_id = int(ns.get("id", -1))
        if ns_id >= 0:
            namespaces.append({
                "id": ns_id,
                "name": ns.get("name", ""),
                "canonical": ns.get("canonical", ""),
            })
    namespaces.sort(key=lambda item: item["id"])

    listed = []
    for ns in namespaces:
        pages = list_all_pages(ns["id"])
        for page in pages:
            listed.append({**page, "namespaceName": ns["name"], "namespaceCanonical": ns["canonical"]})
        print(f"namespace {ns['id']} ({ns['name'] or 'Main'}): {len(pages)} pages", flush=True)

    current = fetch_current_pages([page["title"] for page in listed])
    page_index = []
    contributor_totals = {}
    link_backrefs = {}

    for index, page in enumerate(current, start=1):
        if page.get("missing"):
            continue
        revisions = page.get("revisions") or []
        rev = revisions[0] if revisions else {}
        slots = rev.get("slots") or {}
        main_slot = slots.get("main") or {}
        content = main_slot.get("content", "")
        parsed = parse_wiki(content)
        filename = safe_name(page["title"])

        (OUT / "pages" / f"{filename}.wiki").write_text(content, encoding="utf-8")
        history = fetch_history(page["title"])
        (OUT / "history" / f"{filename}.json").write_text(
            json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        contributors = {}
        for item in history:
            user = item.get("user") or "(hidden/unknown)"
            contributors[user] = contributors.get(user, 0) + 1
            contributor_totals[user] = contributor_totals.get(user, 0) + 1

        for target in parsed["links"]:
            link_backrefs.setdefault(target, []).append(page["title"])

        page_index.append({
            "title": page["title"],
            "pageid": page.get("pageid"),
            "ns": page.get("ns"),
            "canonicalurl": page.get("canonicalurl"),
            "currentRevision": {
                "revid": rev.get("revid"),
                "parentid": rev.get("parentid"),
                "timestamp": rev.get("timestamp"),
                "user": rev.get("user"),
                "comment": rev.get("comment"),
                "contentmodel": main_slot.get("contentmodel") or rev.get("contentmodel"),
            },
            "byteLength": len(content.encode("utf-8")),
            "revisionCount": len(history),
            "contributors": [
                {"user": user, "edits": edits}
                for user, edits in sorted(contributors.items(), key=lambda x: (-x[1], x[0].lower()))
            ],
            **parsed,
            "backupFile": f"pages/{filename}.wiki",
            "historyFile": f"history/{filename}.json",
        })

        if index % 10 == 0 or index == len(current):
            print(f"backed up {index}/{len(current)} pages", flush=True)

    titles = {page["title"] for page in page_index}
    missing_targets = []
    for page in page_index:
        for target in page["links"]:
            if target not in titles and ":" not in target:
                missing_targets.append({"from": page["title"], "target": target})

    general = query.get("general", {})
    generated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    review = {
        "generatedAtUtc": generated,
        "api": API,
        "site": general,
        "pageCount": len(page_index),
        "namespaceCounts": {
            str(ns["id"]): sum(1 for page in page_index if page["ns"] == ns["id"])
            for ns in namespaces
        },
        "contributors": [
            {"user": user, "edits": edits}
            for user, edits in sorted(contributor_totals.items(), key=lambda x: (-x[1], x[0].lower()))
        ],
        "pagesByRevisionCount": [
            {"title": page["title"], "revisions": page["revisionCount"]}
            for page in sorted(page_index, key=lambda p: (-p["revisionCount"], p["title"].lower()))
        ],
        "pagesBySize": [
            {"title": page["title"], "bytes": page["byteLength"]}
            for page in sorted(page_index, key=lambda p: (-p["byteLength"], p["title"].lower()))
        ],
        "orphanCandidates": [
            page["title"] for page in page_index
            if page["ns"] == 0
            and page["title"] != general.get("mainpage")
            and not link_backrefs.get(page["title"])
        ],
        "brokenOrMissingTargets": missing_targets,
    }

    manifest = {
        "snapshotType": "pre-ai-preservation-baseline",
        "createdAtUtc": generated,
        "sourceWiki": general.get("base"),
        "generator": "snapshot_enthusia_wiki.py",
        "scope": "all non-negative MediaWiki namespaces; exact current wikitext plus complete revision metadata available through API",
        "note": "Miraheze page histories remain authoritative for original attribution. No wiki edit is performed by this collector.",
        "namespaces": namespaces,
        "pages": page_index,
    }

    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Enthusia pre-redesign wiki preservation baseline\n\n"
        f"Generated: {generated}\n\n"
        "This is a read-only capture of current page source and revision/contributor metadata. "
        "No Miraheze page was edited.\n",
        encoding="utf-8",
    )
    print(f"snapshot complete: {len(page_index)} pages, {len(contributor_totals)} contributors", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr, flush=True)
        raise
