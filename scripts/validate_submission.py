"""Offline checks for Lightbringer's portable OpenAI upload package.

The standard-library checks also run during packaging. This CLI additionally
validates the pinned portable JSON schemas (install requirements-validation.txt).
Portal scans and authenticated acceptance tests remain separate.
"""

import argparse
import json
import re
import zlib
from pathlib import Path
import struct
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent

# https://developers.openai.com/plugins/deploy/submission-errors#listing-and-interface-errors
OPENAI_CATEGORIES = frozenset({
    "Productivity", "Creativity", "Developer Tools", "Business & Operations",
    "Data & Analytics", "Communication", "Education & Research", "Security",
    "Finance", "Healthcare", "Travel", "Entertainment", "Other",
})


class SubmissionError(ValueError):
    pass


FORBIDDEN_KEYS = {
    "test_credentials", "reviewer_instructions", "password", "client_secret",
    "access_token", "refresh_token", "api_key", "authorization", "private_key",
}


def no_credentials(value):
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", key.lower())
            if any(normalized.endswith(field.replace("_", "")) for field in FORBIDDEN_KEYS):
                raise SubmissionError("Credential or reviewer-access fields belong in the portal, not the package")
            no_credentials(child)
    elif isinstance(value, list):
        for child in value:
            no_credentials(child)


def text(value, label, maximum=4000):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise SubmissionError(f"{label} must be nonempty text of at most {maximum} characters")
    return value


def https(value, label):
    text(value, label, 2048)
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise SubmissionError(f"{label} must be an HTTPS URL without credentials")


def regular_file(root, relative):
    """Reject traversal and every symlink component before reading package files."""
    if not isinstance(relative, str) or "\\" in relative or relative.startswith("/"):
        raise SubmissionError("Invalid package path")
    parts = relative.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise SubmissionError("Invalid package path")
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise SubmissionError("Package paths must not contain symlinks")
    if not path.is_file():
        raise SubmissionError(f"Missing package file: {relative}")
    return path


def png_dimensions(data, label):
    if (len(data) < 33 or len(data) > 5 * 1024 * 1024
            or data[:8] != b"\x89PNG\r\n\x1a\n"
            or data[8:16] != b"\x00\x00\x00\x0dIHDR"):
        raise SubmissionError(f"{label} must be a PNG of at most 5 MiB")
    width, height = struct.unpack(">II", data[16:24])
    if not (48 <= width <= 4096 and 48 <= height <= 4096):
        raise SubmissionError(f"{label} has unsupported image dimensions")
    offset, saw_data = 8, False
    while offset < len(data):
        if offset + 12 > len(data):
            raise SubmissionError(f"{label} contains a truncated PNG chunk")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        end = offset + 12 + length
        if end > len(data):
            raise SubmissionError(f"{label} contains a truncated PNG chunk")
        kind = data[offset + 4:offset + 8]
        expected = struct.unpack(">I", data[end - 4:end])[0]
        if zlib.crc32(data[offset + 4:end - 4]) != expected:
            raise SubmissionError(f"{label} contains a corrupt PNG chunk")
        saw_data = saw_data or kind == b"IDAT"
        if kind == b"IEND":
            if length != 0 or end != len(data) or not saw_data:
                raise SubmissionError(f"{label} has trailing data or incomplete PNG content")
            return width, height
        offset = end
    raise SubmissionError(f"{label} is missing its PNG end chunk")


def asset_files(root):
    directory = root / "assets"
    if directory.is_symlink():
        raise SubmissionError("Asset directory must not be a symlink")
    if not directory.exists():
        return {}
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise SubmissionError("Assets must not contain symlinks")
        if path.is_file():
            name = path.relative_to(root).as_posix()
            if path.suffix != ".png":
                raise SubmissionError("Only public PNG images belong in assets/")
            source = regular_file(root, name)
            if source.stat().st_size > 5 * 1024 * 1024:
                raise SubmissionError("Asset exceeds the 5 MiB limit")
            data = source.read_bytes()
            png_dimensions(data, "Asset")
            files[name] = data
    return files


def validate_openai(root, manifest, mcp):
    no_credentials(manifest)
    no_credentials(mcp)
    extension = manifest.get("extensions", {}).get("com.openai")
    if extension is None:
        return  # Older portable packages remain buildable.
    if not isinstance(extension, dict):
        raise SubmissionError("com.openai must be an object")
    if any(k in extension for k in ("apps", "hooks")):
        raise SubmissionError("App references and lifecycle hooks are not supported in submission ZIPs")
    interface = extension.get("interface", {})
    for field, limit in {"displayName": 30, "shortDescription": 30, "longDescription": 4000,
                         "developerName": 80, "category": 120}.items():
        text(interface.get(field), field, limit)
    if interface["category"] not in OPENAI_CATEGORIES:
        raise SubmissionError("category must be an allowed OpenAI directory category")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        text(interface.get(field), field, 1024)
        https(interface[field], field)
    prompts = interface.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if not isinstance(prompts, list) or len(prompts) > 3:
        raise SubmissionError("Use at most three default prompts")
    for prompt in prompts:
        text(prompt, "defaultPrompt", 128)

    assets = asset_files(root)
    references = [(field, interface.get(field), True) for field in ("logo", "composerIcon")]
    references += [(field, interface[field], True) for field in ("logoDark", "composerIconDark") if field in interface]
    screenshots = interface.get("screenshots", [])
    if not isinstance(screenshots, list):
        raise SubmissionError("screenshots must be an array")
    references += [("screenshot", path, False) for path in screenshots]
    for field, reference, square in references:
        if not isinstance(reference, str) or not reference.startswith("./assets/"):
            raise SubmissionError(f"{field} must reference a ./assets/ file")
        regular_file(root, reference[2:])
        data = assets.get(reference[2:], b"")
        # This repository intentionally supports PNG assets only. Other portal
        # formats need a corresponding decoder/check before adding them here.
        width, height = png_dimensions(data, field)
        if square and width != height:
            raise SubmissionError(f"{field} has unsupported image dimensions")

    servers = mcp.get("mcpServers", {})
    if set(servers) != {"lightbringer"}:
        raise SubmissionError("The submission must contain exactly the Lightbringer MCP server")
    server = servers["lightbringer"]
    if server.get("type") != "streamable-http" or server.get("url") != "https://mcp.lightbringer.com/mcp":
        raise SubmissionError("Unexpected MCP connection configuration")
    if set(server) != {"type", "url"}:
        raise SubmissionError("Keep authentication and review configuration out of the MCP connection object")

    review = extension.get("review", {})
    cases = review.get("test_cases", {})
    for kind, count in (("positive", 5), ("negative", 3)):
        entries = cases.get(kind)
        if not isinstance(entries, list) or len(entries) != count:
            raise SubmissionError(f"Exactly {count} {kind} test cases are required")
        for case in entries:
            if not isinstance(case, dict):
                raise SubmissionError("Each review case must be an object")
            allowed = {"description", "prompt", "tools_triggered", "expected_behavior",
                       "file_attachment_urls", "expected_output_url"}
            if set(case) - allowed:
                raise SubmissionError("Unsupported review case fields; use prompt and expected_behavior")
            for field in ("description", "prompt", "expected_behavior"):
                text(case.get(field), field)
            if kind == "positive" or "tools_triggered" in case:
                text(case.get("tools_triggered"), "tools_triggered")
            attachments = case.get("file_attachment_urls", [])
            if not isinstance(attachments, list):
                raise SubmissionError("file_attachment_urls must be an array")
            for url in attachments:
                https(url, "file_attachment_urls")
            if "expected_output_url" in case:
                https(case["expected_output_url"], "expected_output_url")
    if "demo_recording_url" in review:
        https(review["demo_recording_url"], "demo_recording_url")
    text(extension.get("publication", {}).get("release_notes"), "release_notes")
    onboarding = extension.get("onboardingSkill")
    if onboarding is not None:
        if not isinstance(onboarding, str) or not onboarding.startswith("./skills/") or not onboarding.endswith("/SKILL.md"):
            raise SubmissionError("onboardingSkill must reference a packaged SKILL.md")
        regular_file(root, onboarding[2:])


def validate_schemas(manifest, mcp):
    from jsonschema import Draft202012Validator
    for name, value in (("plugin", manifest), ("mcp", mcp)):
        schema = json.loads((Path(__file__).parent / "schemas" / f"{name}.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema).iter_errors(value))
        if errors:
            # Do not print rejected values: malformed packages may contain secrets.
            raise SubmissionError(f"{name}.json does not satisfy its portable manifest schema")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--expected-name", default="lightbringer",
                        help="Expected manifest name when validating an extracted OpenAI update ZIP")
    parser.add_argument("--require-demo", action="store_true", help="Require a packaged walkthrough URL instead of preserving the portal's existing value")
    parser.add_argument("--tools", type=Path, help="Local tools/list JSON for checking scenario tool names")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads(regular_file(root, "plugin.json").read_text())
    mcp = json.loads(regular_file(root, "mcp.json").read_text())
    if "com.openai" not in manifest.get("extensions", {}):
        raise SubmissionError("OpenAI submission metadata is missing")
    validate_openai(root, manifest, mcp)
    validate_schemas(manifest, mcp)
    from build_release import package_files
    _, files = package_files(root, True, expected_name=args.expected_name)
    review = manifest["extensions"]["com.openai"]["review"]
    if "demo_recording_url" not in review:
        if args.require_demo:
            raise SubmissionError("Add the actual reviewer-accessible demo_recording_url before the initial submission")
        print("Walkthrough URL omitted: confirm the existing recording in the portal; upload preserves it.")
    if args.tools:
        catalog = json.loads(args.tools.read_text())
        names = {tool["name"] for tool in catalog.get("result", catalog)["tools"]}
        for case in review["test_cases"]["positive"] + review["test_cases"]["negative"]:
            for name in case.get("tools_triggered", "").split(","):
                if name.strip() and name.strip() not in names:
                    raise SubmissionError("A review case references a tool absent from the supplied catalog")
    print(f"Portable schemas, OpenAI metadata, review cases, skill links and {len(files)} package files validated.")
    print("Local validation does not run portal scans or authenticated review cases.")


if __name__ == "__main__":
    try:
        main()
    except SubmissionError as error:
        raise SystemExit(str(error))
    except (ValueError, KeyError, TypeError, AttributeError, OSError, ImportError):
        raise SystemExit("Submission validation failed. Check required fields, assets and cases; install scripts/requirements-validation.txt for schema validation. No rejected values are printed.")
