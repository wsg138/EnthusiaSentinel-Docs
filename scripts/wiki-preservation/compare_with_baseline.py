#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

CURRENT = Path('wiki-preservation-output/manifest.json')
OUT = Path('wiki-preservation-output/comparison.json')


def load_baseline():
    raw = subprocess.check_output([
        'git','show','origin/wiki-preservation-baseline:manifest.json'
    ], text=True)
    return json.loads(raw)


def page_map(manifest):
    return {p['title']: p for p in manifest.get('pages', [])}


def main():
    baseline = load_baseline()
    current = json.loads(CURRENT.read_text(encoding='utf-8'))
    before = page_map(baseline)
    after = page_map(current)

    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = []
    for title in sorted(set(before) & set(after)):
        b = before[title]
        a = after[title]
        br = (b.get('currentRevision') or {}).get('revid')
        ar = (a.get('currentRevision') or {}).get('revid')
        if br != ar:
            changed.append({
                'title': title,
                'baselineRevid': br,
                'currentRevid': ar,
                'baselineTimestamp': (b.get('currentRevision') or {}).get('timestamp'),
                'currentTimestamp': (a.get('currentRevision') or {}).get('timestamp'),
                'baselineUser': (b.get('currentRevision') or {}).get('user'),
                'currentUser': (a.get('currentRevision') or {}).get('user'),
                'currentComment': (a.get('currentRevision') or {}).get('comment'),
            })

    result = {
        'baselineCreatedAtUtc': baseline.get('createdAtUtc'),
        'currentCreatedAtUtc': current.get('createdAtUtc'),
        'baselinePageCount': len(before),
        'currentPageCount': len(after),
        'addedPages': added,
        'removedPages': removed,
        'changedPages': changed,
        'unchanged': not added and not removed and not changed,
    }
    OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
