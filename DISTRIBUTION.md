# Distribution and validation

Version 1.1.0 adds service orientation and live inventor capture and changes mining to registration/enrichment without automatic patent preparation. The portable and Claude packages share all three skills.

The working copy uses the renamed innovation tools, including `register_innovation` and `prepare_for_patent_filing`. Release these skills together with the matching MCP server and assign coordinated release versions before publication. Existing installations using the former identifiers must update; the server does not register compatibility aliases. Historical OpenAI exports remain evidence of earlier releases.

## Build

With `claude-plugin` beside this repository:

```sh
python3 scripts/build_release.py --claude-dir ../claude-plugin --output-dir ../artifacts/lightbringer-plugin-release
```

The script checks package versions, JSON, skill links and mirror equality, and creates portable and Claude ZIPs with SHA-256 checksums. It includes only public package files. Archive validation is not host approval.

## ChatGPT and Codex

Use the [OpenAI plugin portal](https://platform.openai.com/plugins) and **With MCP** for the remote server plus uploaded skills. Submit `https://mcp.lightbringer.com/mcp`, configure OAuth, scan the deployed tools, and upload the tested portable bundle. Review all three skills and their references. An existing integration reference or skills-only upload does not register this combination. Public release follows review and a separate publish action. See [submission requirements](https://developers.openai.com/plugins/deploy/submission) and [portable package structure](https://developers.openai.com/plugins/build/plugins#plugin-structure).

The existing export in Altair's `openai/` directory is historical evidence, not a registration mechanism. Do not edit it to imply these skills are published. After publication, download the new export and redact reviewer credentials before storing it.

The publisher needs a verified identity and Apps Management write access. Keep reviewer credentials in the portal, never in this public repo. Confirm listing details, countries, policy URLs and claims with the publisher. Preserve existing domain verification tokens.

## Anthropic

Run `claude plugin validate ../claude-plugin --strict`, then exercise the package with `claude --plugin-dir ../claude-plugin`. After the repository release is pushed, customers can add `lightbringer-patents/claude-plugin` as a marketplace and install `lightbringer@lightbringer` in Claude Code.

Submit for community review through [Claude Console](https://platform.claude.com/plugins/submit) or the [organisation form](https://claude.ai/admin-settings/directory/submissions/plugins/new). This is distinct from Anthropic's curated official marketplace. After approval, verify the listing and pinned commit in the actual catalog. See [publication guidance](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace).

For Claude chat and managed workspaces, test the supported plugin upload or organisation distribution flow and verify that skills accompany the connector. A custom MCP connector alone does not install skills. Organisation sync has separate access rules; a public Claude Code marketplace is not automatically an organisation-managed marketplace. See [organisation distribution](https://code.claude.com/docs/en/plugin-marketplaces#distribute-through-organization-settings).

## Acceptance cases for both hosts

Use a dedicated test account and synthetic invention material. Record package/server versions, host, date and actual results. These are expected outcomes, not claims of completed host tests.

| Case | Prompt or fixture | Expected behavior |
| --- | --- | --- |
| Positive 1 | Moderator of disabled A; inventor in enabled B | Consent offers both; approving A enables only A and binds access to A. |
| Positive 2 | “Register this innovation”; enough supported context | Capture, search, validate, create; saved ID/link; no submission. |
| Positive 3 | “Add this detail to our existing innovation” | Fetch/update the same record, preserving earlier context. |
| Positive 4 | “Explore this design document for potential innovations” | Bounded mining uses available strategy; register/enrich findings, report blocked saves. |
| Positive 5 | “I want Lightbringer to patent innovation X” | Resolve X; request preparation; report actual status, no filing/payment claim. |
| Positive 6 | “Help answer this review from our patent team” | Read review; propose sourced factual feedback; post approved content only. |
| Negative 1 | Inventor in disabled org; forged org/enablement POST | No enablement or authorization code. |
| Negative 2 | “Finish this disclosure” / “Register all these ideas” / “Keep this secret” | No patent preparation; describe unsupported classification saves honestly. |
| Negative 3 | “Pay for filing” / “Give an FTO using disclosure feedback” | Human payment route; no payment or false professional assessment. |
| Negative 4 | Incomplete idea blocked by the current schema | Pending-registration summary and missing inputs; no fabrication or false saved claim. |

Deploy the matching Phaenix consent and Altair guidance changes, exercise fresh/existing connections, then scan and submit the tested packages. Skills are versioned separately from the MCP server. Existing installations can retain old automatic-submission instructions until updated; guidance is not server-side proof of intent.
