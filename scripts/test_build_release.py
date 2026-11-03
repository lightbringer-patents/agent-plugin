"""Package release regression tests. Run: python3 -m unittest discover -s scripts."""

import hashlib
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile


SCRIPT = Path(__file__).with_name("build_release.py")
spec = importlib.util.spec_from_file_location("build_release", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildReleaseTests(unittest.TestCase):
    def package(self, root, portable, version):
        root.mkdir()
        manifest = root / ("plugin.json" if portable else ".claude-plugin/plugin.json")
        manifest.parent.mkdir(exist_ok=True)
        manifest.write_text(json.dumps({"name": "lightbringer", "version": version}))
        (root / ("mcp.json" if portable else ".mcp.json")).write_text(json.dumps({
            "mcpServers": {"lightbringer": {"url": "https://mcp.lightbringer.com/mcp"}}
        }))
        if not portable:
            (root / ".claude-plugin/marketplace.json").write_text(json.dumps({"plugins": [{"name": "lightbringer"}]}))
        for name in ["README.md", "LICENSE", "DISTRIBUTION.md"]:
            (root / name).write_text("Public package fixture\n")
        skill = root / "skills/example/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: example\ndescription: Example workflow\n---\nExample\n")

    def test_independent_versions_and_reproducible_checksums(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            portable, claude, output = root / "portable", root / "claude", root / "output"
            self.package(portable, True, "1.1.0")
            self.package(claude, False, "1.1.1")
            icon = b"icon fixture"
            (claude / ".claude-plugin/icon.png").write_bytes(icon)
            (claude / ".claude").mkdir()
            (claude / ".claude/CLAUDE.md").write_text("Contributor instructions\n")
            with patch.object(builder, "__file__", str(portable / "scripts/build_release.py")), patch("sys.argv", [
                "build_release.py", "--claude-dir", str(claude), "--output-dir", str(output)
            ]):
                builder.main()
                first = (output / "SHA256SUMS").read_text()
                builder.main()
                self.assertEqual(first, (output / "SHA256SUMS").read_text())
                for line in first.splitlines():
                    checksum, name = line.split("  ")
                    self.assertEqual(checksum, hashlib.sha256((output / name).read_bytes()).hexdigest())
                with zipfile.ZipFile(output / "lightbringer-claude-1.1.1.zip") as archive:
                    self.assertEqual(json.loads(archive.read(".claude-plugin/plugin.json"))["version"], "1.1.1")
                    self.assertEqual(archive.read(".claude-plugin/icon.png"), icon)
                    self.assertNotIn(".claude/CLAUDE.md", archive.namelist())
                self.assertTrue((output / "lightbringer-portable-1.1.0.zip").is_file())

    def test_different_skills_still_block_packaging(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            portable, claude, output = root / "portable", root / "claude", root / "output"
            self.package(portable, True, "1.1.0")
            self.package(claude, False, "1.1.1")
            with (claude / "skills/example/SKILL.md").open("a") as file:
                file.write("Different instructions\n")
            with patch.object(builder, "__file__", str(portable / "scripts/build_release.py")), patch("sys.argv", [
                "build_release.py", "--claude-dir", str(claude), "--output-dir", str(output)
            ]):
                with self.assertRaisesRegex(ValueError, "Shared skills differ"):
                    builder.main()
            self.assertFalse(output.exists())

    def test_openai_archive_changes_only_identity_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            portable, claude, output = root / "portable", root / "claude", root / "output"
            self.package(portable, True, "1.3.0")
            self.package(claude, False, "1.3.1")
            source = (portable / "plugin.json").read_bytes()
            name = "app-example-existing-listing"
            with patch.object(builder, "__file__", str(portable / "scripts/build_release.py")), patch("sys.argv", [
                "build_release.py", "--claude-dir", str(claude), "--output-dir", str(output),
                "--openai-plugin-name", name,
            ]):
                builder.main()
                first = (output / "SHA256SUMS").read_bytes()
                builder.main()
                self.assertEqual(first, (output / "SHA256SUMS").read_bytes())
            with zipfile.ZipFile(output / "lightbringer-openai-1.3.0.zip") as uploaded, zipfile.ZipFile(
                output / "lightbringer-portable-1.3.0.zip"
            ) as canonical:
                self.assertEqual(set(uploaded.namelist()), set(canonical.namelist()))
                for path in canonical.namelist():
                    if path != "plugin.json":
                        self.assertEqual(uploaded.read(path), canonical.read(path))
                metadata = json.loads(uploaded.read("plugin.json"))
                self.assertEqual(metadata["name"], name)
                metadata["name"] = "lightbringer"
                self.assertEqual(metadata, json.loads(canonical.read("plugin.json")))
                staged = root / "staged"
                uploaded.extractall(staged)
            builder.package_files(staged, True, expected_name=name)
            with self.assertRaisesRegex(ValueError, "Invalid release identity"):
                builder.package_files(staged, True)
            self.assertEqual(source, (portable / "plugin.json").read_bytes())
            with zipfile.ZipFile(output / "lightbringer-claude-1.3.1.zip") as archive:
                self.assertEqual(json.loads(archive.read(".claude-plugin/plugin.json"))["name"], "lightbringer")
            for line in first.decode().splitlines():
                checksum, filename = line.split("  ")
                self.assertEqual(checksum, hashlib.sha256((output / filename).read_bytes()).hexdigest())

    def test_antigravity_archive_is_clean_self_contained_and_reproducible(self):
        source = SCRIPT.parent.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            portable, claude, output = root / "portable", root / "claude", root / "output"
            shutil.copytree(source, portable, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            self.package(claude, False, "1.7.2")
            shutil.rmtree(claude / "skills")
            shutil.copytree(portable / "skills", claude / "skills")
            version, expected = builder.antigravity_files(portable)
            _, original_portable = builder.package_files(portable, True)
            with patch.object(builder, "__file__", str(portable / "scripts/build_release.py")), patch("sys.argv", [
                "build_release.py", "--claude-dir", str(claude), "--output-dir", str(output),
                "--openai-plugin-name", "app-example-existing-listing",
            ]):
                builder.main()
                first = (output / "SHA256SUMS").read_bytes()
                builder.main()
                self.assertEqual(first, (output / "SHA256SUMS").read_bytes())
            with zipfile.ZipFile(output / f"lightbringer-antigravity-{version}.zip") as archive:
                files = {name: archive.read(name) for name in archive.namelist()}
                self.assertEqual(files, expected)
                self.assertEqual({name: data for name, data in files.items() if name.startswith("skills/")},
                                 builder.skill_files(source))
                self.assertFalse(any(name.startswith((".", "scripts/", "rules/")) for name in files))
                for name in ("AGENTS.md", "CLAUDE.md", "mcp.json", "DISTRIBUTION.md"):
                    self.assertNotIn(name, files)
                manifest = json.loads(files["plugin.json"])
                self.assertIn(manifest["logo"], files)
                self.assertNotIn("extensions", manifest)
                extracted = root / "extracted"
                archive.extractall(extracted)
                self.assertEqual(builder.antigravity_files(extracted, packaged=True), (version, files))
            with zipfile.ZipFile(output / f"lightbringer-portable-{version}.zip") as archive:
                self.assertEqual({name: archive.read(name) for name in archive.namelist()}, original_portable)
            native_bytes = (output / f"lightbringer-antigravity-{version}.zip").read_bytes()
            with patch.object(builder, "__file__", str(portable / "scripts/build_release.py")), patch("sys.argv", [
                "build_release.py", "--antigravity-only", "--output-dir", str(root / "native-only"),
            ]):
                builder.main()
            self.assertEqual((root / "native-only" / f"lightbringer-antigravity-{version}.zip").read_bytes(), native_bytes)

    def test_invalid_openai_identity_fails_before_writing_archives(self):
        for name in ("", "Wrong Name", "app--example", "../example", "a" * 65):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "output"
                with patch("sys.argv", ["build_release.py", "--claude-dir", directory,
                                       "--output-dir", str(output), "--openai-plugin-name", name]):
                    with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                        builder.main()
                    self.assertEqual(error.exception.code, 2)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
