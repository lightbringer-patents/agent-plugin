"""Regression checks for the actual portable upload package and rejected inputs."""

import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

from build_release import package_files
from validate_submission import (
    ROOT, main as validate_submission, validate_antigravity, validate_openai,
    validate_schemas, no_credentials,
)


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
        for variant in ("light", "dark"):
            path = f"assets/lightbringer-icon-{variant}.png"
            self.assertEqual(files[path], (ROOT / path).read_bytes())
        self.assertEqual(
            {p for p in files if p.endswith("/SKILL.md")},
            {
                "skills/setup/SKILL.md",
                "skills/novelty-exploration/SKILL.md",
                "skills/trade-secrets/SKILL.md",
                "skills/company-context/SKILL.md",
                "skills/innovation-capture/SKILL.md",
                "skills/ip-strategy/SKILL.md",
                "skills/lightbringer-navigation/SKILL.md",
                "skills/patent-portfolio/SKILL.md",
                "skills/patent-preparation/SKILL.md",
            },
        )
        for reference in ("patent-process.md", "workflow-routes.md"):
            path = f"skills/lightbringer-navigation/references/{reference}"
            self.assertEqual(files[path], (ROOT / path).read_bytes())
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
        interface["logo"] = "./assets/lightbringer-icon-light.png"
        shutil.rmtree(self.root / "assets")
        (self.root / "assets").symlink_to(ROOT / "assets", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.check()

    def test_missing_malformed_and_nonsquare_icons_are_rejected(self):
        icon = self.root / "assets/lightbringer-icon-light.png"
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

    def test_links_into_another_skill_are_rejected(self):
        skill = self.root / "skills/patent-portfolio/SKILL.md"
        skill.write_text(skill.read_text() + "\n[Other](../setup/SKILL.md)\n")
        with self.assertRaisesRegex(ValueError, "Missing or escaping skill reference"):
            package_files(self.root, True)

    def test_shared_reference_copies_must_match(self):
        copy_path = self.root / "skills/trade-secrets/references/unresolved-needs.md"
        copy_path.write_text(copy_path.read_text() + "\nDrift.\n")
        with self.assertRaisesRegex(ValueError, "unresolved-needs.md differ"):
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
        icon = self.root / "assets/lightbringer-icon-light.png"
        content = icon.read_bytes()
        for bad in (content[:33], content[:-2], content + b"trailing"):
            icon.write_bytes(bad)
            with self.assertRaisesRegex(ValueError, "PNG"):
                self.check()

    def test_antigravity_listing_matches_portable_package(self):
        shutil.copytree(ROOT / ".antigravity-plugin", self.root / ".antigravity-plugin")
        target = self.root / ".antigravity-plugin/plugin.json"
        shutil.copyfile(ROOT / "mcp_config.json", self.root / "mcp_config.json")
        validate_antigravity(self.root, self.manifest)
        listing = json.loads(target.read_text())
        for field, value, message in (
            ("version", "0.0.1", "version must match"),
            ("description", "x" * 161, "description"),
            ("suggestedPrompts", ["a", "b", "c", "d"], "suggestedPrompts"),
            ("logo", "assets/../plugin.json", "Invalid package path"),
        ):
            bad = dict(listing, **{field: value})
            target.write_text(json.dumps(bad))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message):
                validate_antigravity(self.root, self.manifest)
        target.write_text(json.dumps(listing))
        (self.root / "mcp_config.json").write_text(json.dumps(
            {"mcpServers": {"lightbringer": {"url": "https://example.com/mcp"}}}))
        with self.assertRaisesRegex(ValueError, "Unexpected MCP"):
            validate_antigravity(self.root, self.manifest)

    def validate_cli(self, root, *args):
        with patch("sys.argv", ["validate_submission.py", "--root", str(root), *args]), contextlib.redirect_stdout(io.StringIO()):
            validate_submission()

    def test_portable_and_openai_packages_validate_without_antigravity(self):
        # Start with the complete repository distribution, then validate only
        # the files selected by the real portable/OpenAI packaging path.
        shutil.copytree(ROOT / ".antigravity-plugin", self.root / ".antigravity-plugin")
        shutil.copyfile(ROOT / "mcp_config.json", self.root / "mcp_config.json")
        self.validate_cli(self.root, "--require-antigravity")
        _, files = package_files(self.root, True)
        self.assertNotIn("mcp_config.json", files)
        self.assertFalse(any(name.startswith(".antigravity-plugin/") for name in files))
        extracted = self.root / "extracted"
        for name, data in files.items():
            target = extracted / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        self.validate_cli(extracted)
        with self.assertRaisesRegex(ValueError, "Missing package file"):
            self.validate_cli(extracted, "--require-antigravity")
        metadata = json.loads((extracted / "plugin.json").read_text())
        metadata["name"] = "app-example-existing-listing"
        (extracted / "plugin.json").write_text(json.dumps(metadata))
        self.validate_cli(extracted, "--expected-name", metadata["name"])

    def test_partial_antigravity_adapter_is_rejected(self):
        # Neither an orphan MCP configuration nor a listing without its
        # configuration may be mistaken for a portable-only archive.
        config = self.root / "mcp_config.json"
        shutil.copyfile(ROOT / "mcp_config.json", config)
        with self.assertRaisesRegex(ValueError, "Missing package file: .antigravity-plugin/plugin.json"):
            self.validate_cli(self.root)
        config.unlink()
        shutil.copytree(ROOT / ".antigravity-plugin", self.root / ".antigravity-plugin")
        with self.assertRaisesRegex(ValueError, "Missing package file: mcp_config.json"):
            self.validate_cli(self.root)

    def test_onboarding_must_resolve_to_packaged_skill(self):
        extension = self.manifest["extensions"]["com.openai"]
        extension["onboardingSkill"] = "./skills/missing/SKILL.md"
        with self.assertRaisesRegex(ValueError, "Missing package file"):
            self.check()


if __name__ == "__main__":
    unittest.main()
