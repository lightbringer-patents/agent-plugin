#!/usr/bin/env python3
"""Validate mirrored public packages and create reproducible upload archives."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def skill_files(root: Path) -> dict[str, bytes]:
    files = {}
    for path in sorted((root / "skills").rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed in the skill bundle: {path}")
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    entries = [name for name in files if name.endswith("/SKILL.md")]
    if not entries:
        raise ValueError(f"No skills found in {root}")
    for name in entries:
        text = files[name].decode("utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not frontmatter:
            raise ValueError(f"Missing skill frontmatter: {name}")
        declared = re.search(r"^name: ([a-z0-9-]+)$", frontmatter[1], re.M)
        if not declared or declared[1] != Path(name).parent.name:
            raise ValueError(f"Skill name must match its directory: {name}")
        if not re.search(r"^description: \S", frontmatter[1], re.M):
            raise ValueError(f"Missing skill description: {name}")
    for name, content in files.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", content.decode("utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            linked = (root / name).parent.joinpath(target.split("#")[0]).resolve()
            if not linked.is_relative_to(root) or not linked.is_file():
                raise ValueError(f"Missing or escaping skill reference: {name}: {target}")
    return files


def package_files(root: Path, portable: bool) -> tuple[str, dict[str, bytes]]:
    manifest = "plugin.json" if portable else ".claude-plugin/plugin.json"
    config = "mcp.json" if portable else ".mcp.json"
    metadata = json.loads((root / manifest).read_text())
    if metadata["name"] != "lightbringer" or not re.fullmatch(r"\d+\.\d+\.\d+", metadata["version"]):
        raise ValueError(f"Invalid release identity in {manifest}")
    mcp = json.loads((root / config).read_text())
    if mcp["mcpServers"]["lightbringer"]["url"] != "https://mcp.lightbringer.com/mcp":
        raise ValueError(f"Unexpected connector endpoint in {config}")
    files = skill_files(root)
    paths = [manifest, config, "README.md", "LICENSE"]
    if portable:
        paths.append("DISTRIBUTION.md")
    else:
        marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text())
        if marketplace["plugins"][0]["name"] != metadata["name"]:
            raise ValueError("Marketplace plugin name mismatch")
        paths.append(".claude-plugin/marketplace.json")
    for name in paths:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or non-regular package file: {path}")
        files[name] = path.read_bytes()
    return metadata["version"], files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    claude = args.claude_dir.resolve()
    if skill_files(root) != skill_files(claude):
        raise ValueError("Shared skills differ; sync from agent-plugin before packaging")
    version, portable = package_files(root, True)
    claude_version, anthropic = package_files(claude, False)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    checksums = []
    for host, package_version, files in [("portable", version, portable), ("claude", claude_version, anthropic)]:
        path = args.output_dir / f"lightbringer-{host}-{package_version}.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != set(files):
                raise ValueError(f"Archive verification failed: {path}")
        checksums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
        print(f"Built {path} ({len(files)} files)")
    (args.output_dir / "SHA256SUMS").write_text("\n".join(checksums) + "\n")


if __name__ == "__main__":
    main()
