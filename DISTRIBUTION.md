# Distribution and validation

The package contains three workflow skills: `innovation-capture`, `patent-preparation` and `patent-review`. Capture covers both inventor conversations and source exploration. Preparation ends with a confirmed preparation request; review handles report and patent-draft feedback. General service orientation is supplied through MCP instructions and the README. Each skill contains its required references.

The working copy uses the renamed innovation tools, including `register_innovation` and `request_patent_preparation`. Release these skills together with the matching MCP server and assign coordinated release versions before publication. Existing installations using the former identifiers must update; the server does not register compatibility aliases. The standalone MCP validation tool has been removed: registration validates before saving and returns non-blocking warnings with the saved record. Deploy the Phaenix registration response and template guidance before the matching Altair and plugin release. The preparation action is now `request_patent_preparation`, and its MCP prompt is `request-patent-preparation` with only an innovation selector. Update saved tool and prompt references when releasing the matching server and plugins. Preparation requests do not require automated feedback, an interview or revisions first. Historical OpenAI exports remain evidence of earlier releases.

The automated-feedback tools are `start_innovation_feedback` and `get_task_status`, with prompt `start-innovation-feedback`. Update saved references to the old feedback/status identifiers and ticket argument. The public status input is now `task_id`, and one ID covers the entire feedback run. Both tools share `status`, `progress` and per-analysis `results`; partial success is terminal. Findings use readable `title`/`description` fields and public analysis names. Report `findings_error` as unavailable findings, without retrying terminal tasks. Deploy Phaenix rich-text rendering before Altair normalization. Preparation returns `outcome: requested | already_requested` and no task ID. Deploy the Phaenix `AutomatedTask`/`AutomatedTaskJob` (type `INNOVATION_FEEDBACK`) schema and task routes first, then Altair and these skills. Existing REST ticket and submission contracts are retained for older backend clients; the MCP surface has no old-tool aliases.

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
| Positive 2 | “Register this innovation”; enough supported context | Capture, search, register directly; validation errors mean unsaved; success returns ID/link and warnings; no submission. |
| Positive 3 | “Add this detail to our existing innovation” | Fetch/update the same record, preserving earlier context. |
| Positive 4 | “Explore this design document for potential innovations” | Bounded mining uses available strategy; register/enrich findings, report blocked saves. |
| Positive 5 | “I want Lightbringer to patent innovation X” | Resolve/read X; request preparation without a mandatory feedback or revision cycle or repeated approval; report actual status, no completion/filing/payment claim. |
| Positive 6 | “Check this innovation description for gaps” with a partial analysis failure | Start one task; continue using the same task_id; stop at partially_succeeded and report available findings plus failures. Never poll a preparation request as a task. |
| Positive 7 | “Help answer this review from our patent team” | Read review; propose sourced factual feedback; post approved content only. |
| Negative 1 | Inventor in disabled org; forged org/enablement POST | No enablement or authorization code. |
| Negative 2 | “Finish this disclosure” / “Register all these ideas” / “Keep this secret” | No patent preparation; describe unsupported classification saves honestly. |
| Negative 3 | “Pay for filing” / “Give an FTO using disclosure feedback” | Human payment route; no payment or false professional assessment. |
| Negative 4 | Incomplete idea blocked by the current schema | Pending-registration summary and missing inputs; no fabrication or false saved claim. |
| Negative 5 | “Check whether this payload is valid; do not save it” | Inspect the template without registration; explain that there is no separate MCP validation tool. |

Deploy the matching Phaenix consent and Altair guidance changes, exercise fresh/existing connections, then scan and submit the tested packages. Skills are versioned separately from the MCP server. Existing installations can retain old automatic-submission instructions until updated; guidance is not server-side proof of intent.

Task retention and recovery: deploy the task `createdAt` index, expiry checks, user-scrub cleanup, task listing/deletion routes, deletion token scope and daily authenticated cleanup job before Altair. Verify `list_tasks` recovery and `delete_task` with write consent; ownership and current subject access apply to listing/reads, while an owner may delete their own history after losing subject access. Reads expire at 30 days from creation; the capped daily sweep physically deletes expired parents and child results. Aurora execution records retain their existing separate lifecycle.
