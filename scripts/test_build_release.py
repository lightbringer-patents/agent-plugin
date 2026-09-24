"""Package release regression tests. Run: python3 -m unittest discover -s scripts."""

import hashlib
import importlib.util
import json
from pathlib import Path
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
            root = Path(directory)
            portable, claude, output = root / "portable", root / "claude", root / "output"
            self.package(portable, True, "1.1.0")
            self.package(claude, False, "1.1.1")
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
                self.assertTrue((output / "lightbringer-portable-1.1.0.zip").is_file())

    def test_different_skills_still_block_packaging(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
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


if __name__ == "__main__":
    unittest.main()
