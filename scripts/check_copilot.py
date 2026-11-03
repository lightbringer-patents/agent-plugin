#!/usr/bin/env python3
"""Check Copilot installation and discovery in disposable CLI state (no model calls)."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copilot", default=str(ROOT / "scripts/copilot/node_modules/.bin/copilot"))
    parser.add_argument("--source-sha", help="Load the repository marketplace from GitHub at this checkout's full commit SHA")
    parser.add_argument("--entry-output", type=Path, help="Write the tested external listing JSON (requires --source-sha)")
    args = parser.parse_args()
    if args.entry_output and not args.source_sha:
        parser.error("--entry-output requires --source-sha")
    if args.source_sha:
        if not re.fullmatch(r"[0-9a-f]{40}", args.source_sha):
            parser.error("--source-sha must be a full lowercase commit SHA")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        if head != args.source_sha:
            parser.error("--source-sha must match this checkout's HEAD")
        subprocess.run(["git", "diff", "--exit-code", "HEAD", "--", "."], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL)

    manifest = json.loads((ROOT / "plugin.json").read_text())
    fields = ("name", "description", "version", "author", "repository", "homepage", "license", "keywords")
    entry = {key: manifest[key] for key in fields}
    expected_skills = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    if not expected_skills:
        raise ValueError("The candidate must contain skills")
    expected_mcp = json.loads((ROOT / "mcp.json").read_text())["mcpServers"]["lightbringer"]
    marketplace = json.loads((ROOT / "marketplace.json").read_text())
    if marketplace["plugins"] != [{"name": manifest["name"], "source": "./"}]:
        raise ValueError("The catalogue must reference the canonical plugin root without duplicating metadata")
    marketplace_name = marketplace["name"]

    with tempfile.TemporaryDirectory(prefix="lightbringer-copilot-") as temporary:
        work = Path(temporary)
        catalog = work / "marketplace"
        if args.source_sha:
            entry["source"] = {"source": "github", "repo": "lightbringer-patents/agent-plugin",
                               "sha": args.source_sha}
            catalog_source = f"lightbringer-patents/agent-plugin#{args.source_sha}"
        else:
            # Test the repository layout, including other hosts' metadata, without
            # treating contributor instructions as runtime plugin content.
            shutil.copytree(ROOT, catalog, ignore=shutil.ignore_patterns(
                ".git", "node_modules", "__pycache__", ".venv", "artifacts"))
            catalog_source = str(catalog)
        env = dict(os.environ)
        for key in ("GH_TOKEN", "GITHUB_TOKEN", "COPILOT_GITHUB_TOKEN"):
            env.pop(key, None)
        env.update(COPILOT_HOME=str(work / "state"), COPILOT_CACHE_HOME=str(work / "cache"),
                   COPILOT_AUTO_UPDATE="false", NO_COLOR="1", CI="true")

        def run(*arguments, json_output=False):
            result = subprocess.run([args.copilot, *arguments], cwd=work, env=env,
                                    text=True, capture_output=True, timeout=180)
            if result.returncode:
                raise RuntimeError(f"Copilot {' '.join(arguments)} failed:\n{result.stderr}\n{result.stdout}")
            return json.loads(result.stdout) if json_output else result.stdout.strip()

        print(run("--version"))
        run("plugin", "marketplace", "add", catalog_source)
        run("plugin", "install", f"{manifest['name']}@{marketplace_name}")
        plugins = run("plugin", "list", "--json", json_output=True)
        installed = [item for item in plugins if item["name"] == manifest["name"]]
        if len(installed) != 1 or installed[0].get("version") != manifest["version"] or not installed[0].get("enabled"):
            raise ValueError("Copilot did not enable the expected plugin version")

        skills = run("skill", "list", "--json", json_output=True)
        discovered = {item["name"] for item in skills if item.get("enabled")}
        if not expected_skills.issubset(discovered):
            raise ValueError(f"Skills not discovered: {sorted(expected_skills - discovered)}")
        servers = run("mcp", "list", "--json", json_output=True)
        server = servers.get("mcpServers", {}).get("lightbringer", {})
        if (server.get("url") != expected_mcp["url"] or server.get("type") != "http"
                or server.get("sourcePlugin") != manifest["name"]
                or server.get("sourcePluginVersion") != manifest["version"]
                or server.get("source") != "plugin" or not server.get("enabled")):
            raise ValueError("Copilot did not enable the expected plugin MCP configuration")
        run("plugin", "uninstall", f"{manifest['name']}@{marketplace_name}")
        # Local marketplace sources remain on disk after uninstall and appear
        # disabled; GitHub sources are removed. Neither may remain active.
        if any(item["name"] == manifest["name"] and item.get("enabled")
               for item in run("plugin", "list", "--json", json_output=True)):
            raise ValueError("Copilot left the plugin enabled after uninstall")
        remaining_skills = run("skill", "list", "--json", json_output=True)
        if any(item["name"] in expected_skills and item.get("enabled") for item in remaining_skills):
            raise ValueError("Copilot left plugin skills enabled after uninstall")
        remaining_servers = run("mcp", "list", "--json", json_output=True)
        if remaining_servers.get("mcpServers", {}).get("lightbringer", {}).get("enabled"):
            raise ValueError("Copilot left the plugin MCP server enabled after uninstall")
        print(f"Installation, {len(expected_skills)} skills, MCP configuration and deactivation verified.")

    if args.entry_output:
        args.entry_output.write_text(json.dumps(entry, indent=2) + "\n")
        print(f"Wrote tested marketplace entry to {args.entry_output}")


if __name__ == "__main__":
    main()
