from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "examples" / "manifests"
REQUIRED_MANIFEST_KEYS = {
    "schema_version",
    "plugin",
    "artifact",
    "profiles",
    "configs",
    "databases",
    "dependencies",
    "actions",
}
LIST_KEYS = {"profiles", "configs", "databases", "dependencies", "actions"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
PLUGIN_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
ALLOWED_PLUGIN_KEYS = {"id", "name", "main_class"}
ALLOWED_ARTIFACT_KEYS = {"name", "jar_path"}
ALLOWED_DEPENDENCY_KEYS = {"id", "kind"}


class ManifestExampleTests(unittest.TestCase):
    def test_all_manifest_examples_parse_and_keep_the_documented_top_level_contract(self) -> None:
        manifests = sorted(MANIFESTS.glob("*.yml"))
        self.assertGreater(len(manifests), 0, "expected at least one documented manifest example")

        for path in manifests:
            with self.subTest(path=path.name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIsInstance(data, dict)
                self.assertEqual(REQUIRED_MANIFEST_KEYS, set(data), f"{path} top-level contract drifted")
                self.assertEqual(1, data["schema_version"], f"{path} uses an unexpected schema version")
                for key in LIST_KEYS:
                    self.assertIsInstance(data[key], list, f"{path}:{key} must remain a list")

    def test_plugin_and_artifact_identifiers_are_nonblank_relative_and_safe(self) -> None:
        for path in sorted(MANIFESTS.glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            plugin = data["plugin"]
            artifact = data["artifact"]
            with self.subTest(path=path.name):
                self.assertIsInstance(plugin, dict)
                self.assertIsInstance(artifact, dict)
                self.assertRegex(plugin.get("id", ""), PLUGIN_ID)
                self.assertTrue(str(plugin.get("name", "")).strip())
                self.assertIn(".", str(plugin.get("main_class", "")))
                self.assertTrue(str(artifact.get("name", "")).strip())

                jar_path = Path(str(artifact.get("jar_path", "")))
                self.assertFalse(jar_path.is_absolute(), f"{path} artifact path must be repository-relative")
                self.assertNotIn("..", jar_path.parts, f"{path} artifact path must not escape the repository")
                self.assertEqual(".jar", jar_path.suffix.lower(), f"{path} artifact must point to a JAR")

    def test_public_examples_cannot_embed_private_provenance_controls(self) -> None:
        for path in sorted(MANIFESTS.glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            with self.subTest(path=path.name):
                self.assertEqual(
                    ALLOWED_PLUGIN_KEYS,
                    set(data["plugin"]),
                    f"{path}: plugin repositories may describe identity, not private trust/provenance controls",
                )
                self.assertEqual(
                    ALLOWED_ARTIFACT_KEYS,
                    set(data["artifact"]),
                    f"{path}: artifact examples may describe local build output only",
                )
                for dependency in data["dependencies"]:
                    self.assertEqual(
                        ALLOWED_DEPENDENCY_KEYS,
                        set(dependency),
                        f"{path}: dependency examples may request stable id/kind only; provenance stays operator-owned",
                    )

    def test_profiles_and_dependencies_have_explicit_nonblank_identifiers(self) -> None:
        for path in sorted(MANIFESTS.glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            with self.subTest(path=path.name):
                profiles = data["profiles"]
                self.assertGreater(len(profiles), 0, f"{path} should demonstrate at least one profile")
                self.assertEqual(len(profiles), len(set(profiles)), f"{path} profiles must be unique")
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in profiles))

                dependency_ids: list[str] = []
                for dependency in data["dependencies"]:
                    self.assertIsInstance(dependency, dict)
                    identifier = dependency.get("id")
                    kind = dependency.get("kind")
                    self.assertIsInstance(identifier, str)
                    self.assertTrue(identifier.strip())
                    self.assertIsInstance(kind, str)
                    self.assertTrue(kind.strip())
                    dependency_ids.append(identifier)
                self.assertEqual(len(dependency_ids), len(set(dependency_ids)), f"{path} dependency ids must be unique")


class BuildExampleTests(unittest.TestCase):
    def test_maven_example_is_valid_xml_and_targets_java_21(self) -> None:
        path = ROOT / "examples" / "maven" / "pom.xml"
        root = ET.parse(path).getroot()
        namespace = {"m": "http://maven.apache.org/POM/4.0.0"}

        self.assertEqual("project", root.tag.rsplit("}", 1)[-1])
        self.assertEqual("4.0.0", root.findtext("m:modelVersion", namespaces=namespace))
        self.assertEqual("21", root.findtext("m:properties/m:maven.compiler.release", namespaces=namespace))
        self.assertEqual("SentinelExample", root.findtext("m:build/m:finalName", namespaces=namespace))

    def test_gradle_example_keeps_java_21_and_expected_artifact_name(self) -> None:
        path = ROOT / "examples" / "gradle" / "build.gradle.kts"
        source = path.read_text(encoding="utf-8")

        self.assertIn("JavaLanguageVersion.of(21)", source)
        self.assertIn('archiveFileName.set("SentinelExample.jar")', source)
        self.assertIn("./gradlew build", source)
        self.assertIn("build/libs/SentinelExample.jar", source)


class MarkdownLinkTests(unittest.TestCase):
    def test_repository_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        for markdown in sorted(ROOT.rglob("*.md")):
            text = markdown.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK.finditer(text):
                raw_target = match.group(1).strip().strip("<>")
                if not raw_target:
                    continue
                lowered = raw_target.lower()
                if lowered.startswith(("http://", "https://", "mailto:", "data:")):
                    continue

                path_part, separator, fragment = raw_target.partition("#")
                path_part = unquote(path_part.split("?", 1)[0])
                if path_part.startswith("/"):
                    continue

                candidate = markdown if not path_part else (markdown.parent / path_part).resolve()
                try:
                    candidate.relative_to(ROOT)
                except ValueError:
                    failures.append(f"{markdown.relative_to(ROOT)} -> {raw_target} escapes repository root")
                    continue
                if not candidate.exists():
                    failures.append(f"{markdown.relative_to(ROOT)} -> {raw_target} does not exist")
                    continue

                if separator and fragment and candidate.is_file() and candidate.suffix.lower() == ".md":
                    anchors = markdown_anchors(candidate)
                    decoded_fragment = unquote(fragment).lower()
                    if decoded_fragment not in anchors:
                        failures.append(
                            f"{markdown.relative_to(ROOT)} -> {raw_target} points to missing Markdown heading"
                        )

        self.assertEqual([], failures, "broken repository-local Markdown links:\n" + "\n".join(failures))


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    duplicate_counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = github_heading_slug(match.group(1))
        if not base:
            continue
        duplicate_index = duplicate_counts.get(base, 0)
        duplicate_counts[base] = duplicate_index + 1
        anchors.add(base if duplicate_index == 0 else f"{base}-{duplicate_index}")
    return anchors


def github_heading_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"[`*_~]", "", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    heading = re.sub(r"\s+", "-", heading)
    return heading


if __name__ == "__main__":
    unittest.main()
