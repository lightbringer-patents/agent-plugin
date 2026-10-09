"""Regression checks for the actual portable upload package and rejected inputs."""

import copy
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import zlib

from build_release import package_files
from validate_submission import ROOT, validate_openai, validate_schemas, no_credentials


class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        for name in ("plugin.json", "mcp.json", "README.md", "LICENSE", "DISTRIBUTION.md"):
            shutil.copyfile(ROOT / name, self.root / name)
        for name in ("skills", "assets"):
            shutil.copytree(ROOT / name, self.root / name)
        self.manifest = json.loads((self.root / "plugin.json").read_text())
        self.mcp = json.loads((self.root / "mcp.json").read_text())

    def check(self):
        validate_openai(self.root, self.manifest, self.mcp)

    def test_submission_and_referenced_assets_are_packaged(self):
        self.check()
        _, files = package_files(self.root, True)
        self.assertEqual(files["assets/logo-square-light.png"], (ROOT / "assets/logo-square-light.png").read_bytes())
        self.assertEqual(len([p for p in files if p.endswith("/SKILL.md")]), 6)
        self.assertFalse(any(p.startswith("scripts/") for p in files))

    def test_portable_schemas_reject_unknown_fields_and_transport(self):
        validate_schemas(self.manifest, self.mcp)
        bad = copy.deepcopy(self.manifest)
        bad["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "portable manifest schema"):
            validate_schemas(bad, self.mcp)
        bad = copy.deepcopy(self.mcp)
        bad["mcpServers"]["lightbringer"]["type"] = "http"
        with self.assertRaisesRegex(ValueError, "portable manifest schema"):
            validate_schemas(self.manifest, bad)

    def test_directory_category_requires_an_exact_supported_title(self):
        interface = self.manifest["extensions"]["com.openai"]["interface"]
        for category in ("Business & Operations", "Productivity", "Other"):
            interface["category"] = category
            self.check()
        for category in ("Business", "business & operations", "Business &amp; Operations"):
            interface["category"] = category
            with self.subTest(category=category), self.assertRaisesRegex(ValueError, "allowed OpenAI"):
                self.check()

    def test_exact_case_counts_and_new_field_names(self):
        cases = self.manifest["extensions"]["com.openai"]["review"]["test_cases"]
        cases["positive"].append(copy.deepcopy(cases["positive"][0]))
        with self.assertRaisesRegex(ValueError, "Exactly 5"):
            self.check()
        cases["positive"].pop()
        cases["negative"].pop()
        with self.assertRaisesRegex(ValueError, "Exactly 3"):
            self.check()
        case = cases["positive"][0]
        case["user_prompt"] = case.pop("prompt")
        with self.assertRaisesRegex(ValueError, "Unsupported review case"):
            self.check()

    def test_private_fields_and_url_credentials_are_rejected_without_values(self):
        secret = "never-print-this-value"
        self.manifest["extensions"]["com.openai"]["review"]["test_credentials"] = secret
        with self.assertRaises(ValueError) as error:
            self.check()
        self.assertNotIn(secret, str(error.exception))
        del self.manifest["extensions"]["com.openai"]["review"]["test_credentials"]
        self.manifest["extensions"]["com.openai"]["interface"]["supportURL"] = "https://user:secret@example.com"
        with self.assertRaisesRegex(ValueError, "without credentials"):
            self.check()

    def test_asset_traversal_and_parent_symlinks_are_rejected(self):
        interface = self.manifest["extensions"]["com.openai"]["interface"]
        interface["logo"] = "./assets/../plugin.json"
        with self.assertRaisesRegex(ValueError, "Invalid package path"):
            self.check()
        interface["logo"] = "./assets/logo-square-light.png"
        shutil.rmtree(self.root / "assets")
        (self.root / "assets").symlink_to(ROOT / "assets", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.check()

    def test_missing_malformed_and_nonsquare_icons_are_rejected(self):
        icon = self.root / "assets/logo-square-light.png"
        content = icon.read_bytes()
        icon.unlink()
        with self.assertRaisesRegex(ValueError, "Missing package file"):
            self.check()
        icon.write_bytes(b"not a PNG")
        with self.assertRaisesRegex(ValueError, "must be a PNG"):
            self.check()
        changed = content[:16] + struct.pack(">II", 100, 101) + content[24:29]
        icon.write_bytes(changed + struct.pack(">I", zlib.crc32(changed[12:29])) + content[33:])
        with self.assertRaisesRegex(ValueError, "dimensions"):
            self.check()

    def test_broken_skill_reference_blocks_packaging(self):
        skill = self.root / "skills/patent-portfolio/SKILL.md"
        skill.write_text(skill.read_text() + "\n[Missing](references/absent.md)\n")
        with self.assertRaisesRegex(ValueError, "Missing or escaping skill reference"):
            package_files(self.root, True)

    def test_unrelated_asset_files_and_unpackaged_skill_links_are_rejected(self):
        unrelated = self.root / "assets/notes.txt"
        unrelated.write_text("Not an image")
        with self.assertRaisesRegex(ValueError, "Only public PNG"):
            package_files(self.root, True)
        unrelated.unlink()
        (self.root / "not-packaged.md").write_text("Reference outside the skills tree")
        skill = self.root / "skills/patent-portfolio/SKILL.md"
        skill.write_text(skill.read_text() + "\n[Outside](../../not-packaged.md)\n")
        with self.assertRaisesRegex(ValueError, "Missing or escaping skill reference"):
            package_files(self.root, True)

    def test_unused_malformed_and_oversized_assets_are_rejected(self):
        unused = self.root / "assets/unused.png"
        unused.write_bytes(b"Not an image")
        with self.assertRaisesRegex(ValueError, "must be a PNG"):
            package_files(self.root, True)
        with unused.open("wb") as output:
            output.truncate(5 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(ValueError, "5 MiB"):
            package_files(self.root, True)

    def test_nested_and_variant_credential_fields_and_packaged_json_are_rejected(self):
        for value in ({"api_key": "hidden"}, {"config": {"client_secret": "hidden"}},
                      {"items": [{"test_credentials": {"password": "hidden"}}]},
                      {"myApiKey": "hidden"}):
            with self.subTest(value_type=list(value)):
                with self.assertRaises(ValueError) as error:
                    no_credentials(value)
                self.assertNotIn("hidden", str(error.exception))
        no_credentials({"apikeys_used": 5, "password_length_policy": 12})
        (self.root / "skills/patent-portfolio/references/example.json").write_text('{"password":"hidden"}')
        with self.assertRaisesRegex(ValueError, "Credential"):
            package_files(self.root, True)

    def test_truncated_and_trailing_png_data_are_rejected(self):
        icon = self.root / "assets/logo-square-light.png"
        content = icon.read_bytes()
        for bad in (content[:33], content[:-2], content + b"trailing"):
            icon.write_bytes(bad)
            with self.assertRaisesRegex(ValueError, "PNG"):
                self.check()

    def test_onboarding_must_resolve_to_packaged_skill(self):
        extension = self.manifest["extensions"]["com.openai"]
        extension["onboardingSkill"] = "./skills/missing/SKILL.md"
        with self.assertRaisesRegex(ValueError, "Missing package file"):
            self.check()


if __name__ == "__main__":
    unittest.main()
