# Distribution and validation

The package contains four workflow skills: `innovation-capture`, `patent-preparation`, `patent-review` and `patent-portfolio`. Portfolio covers assignee discovery, single and portfolio imports, and patent family updates for saved own patents. Capture covers both inventor conversations and source exploration. Preparation ends with a confirmed preparation request; review handles report and patent-draft feedback. General service orientation is supplied through MCP instructions and the README. Each skill contains its required references.

## Prepared release — 1.2.0

Both package manifests are prepared at version 1.2.0 with identical skills trees. The portfolio skill checks runtime availability of `search_public_patents`, `import_patent` and `refresh_patent_family`; preparing these instructions does not establish deployment or authenticated host acceptance. Family refresh improves grouping of related saved applications; it does not update text, assets or legal status. Run the portfolio acceptance cases below before claiming host verification.

## Interface verification — 2026-09-15

Public discovery confirmed the Lightbringer MCP innovation tools and four prompts on 2026-09-15. Package builds and manifest validation passed during that review; host installation and authenticated production acceptance cases remain separate checks. That review covered portable package version 1.1.0 and Claude package version 1.1.1, with identical skills trees; it did not verify the portfolio workflows added later. See the [connector release guide](https://github.com/lightbringer-patents/mcp-connector/blob/main/RELEASE.md) for compatibility, verification scope and registry publication steps.

The packages use the renamed innovation tools, including `register_innovation` and `request_patent_preparation`. Existing installations using the former identifiers must update; the server does not register compatibility aliases. The standalone MCP validation tool has been removed: registration validates before saving and returns non-blocking warnings with the saved record. The preparation action is `request_patent_preparation`, and its MCP prompt is `request-patent-preparation` with only an innovation selector. Update saved tool and prompt references when installing the new packages. Preparation requests do not require automated feedback, an interview or revisions first.

The automated-feedback tools are `start_innovation_feedback` and `get_task_status`, with prompt `start-innovation-feedback`. Update saved references to the old feedback/status identifiers and ticket argument. The public status input is `task_id`, and one ID covers the entire feedback run. Both tools share `status`, `progress` and per-analysis `results`; partial success is terminal. Findings use readable `title`/`description` fields and documented analysis names. Report `findings_error` as unavailable findings, without retrying terminal tasks. Both tools are annotated non-read-only and available under read consent: starting dispatches analysis; status retrieval persists refreshed status and findings. Preparation returns `outcome: requested | already_requested` and no task ID. The MCP surface has no old-tool aliases.

## Build

With `claude-plugin` beside this repository:

```sh
python3 scripts/build_release.py --claude-dir ../claude-plugin --output-dir ../artifacts/lightbringer-plugin-release
```

The script checks package versions, JSON, skill links and mirror equality, and creates portable and Claude ZIPs with SHA-256 checksums. It includes only public package files. Archive validation is not host approval.

The builder uses each package's own manifest version in its archive filename. Package versions may differ; the complete shared skills trees must still match exactly. Bump the version of each package whose published contents change.

## ChatGPT and Codex

Use the [OpenAI plugin portal](https://platform.openai.com/plugins) and **With MCP** for the remote server plus uploaded skills. Submit `https://mcp.lightbringer.com/mcp`, configure OAuth, scan the deployed tools, and upload the tested portable bundle. Review all four skills and their references. An existing integration reference or skills-only upload does not register this combination. Public release follows review and a separate publish action. See [submission requirements](https://developers.openai.com/plugins/deploy/submission) and [portable package structure](https://developers.openai.com/plugins/build/plugins#plugin-structure).

The publisher needs a verified identity and Apps Management write access. Keep reviewer credentials in the portal, never in this public repo. Confirm listing details, countries, policy URLs and claims with the publisher. Preserve existing domain verification tokens.

## Anthropic

Run `claude plugin validate ../claude-plugin --strict`, then exercise the package with `claude --plugin-dir ../claude-plugin`. After the repository release is pushed, customers can add `lightbringer-patents/claude-plugin` as a marketplace and install `lightbringer@lightbringer` in Claude Code.

Submit for community review through [Claude Console](https://platform.claude.com/plugins/submit) or the [organisation form](https://claude.ai/admin-settings/directory/submissions/plugins/new). This is distinct from Anthropic's curated official marketplace. After approval, verify the listing and pinned commit in the actual catalog. See [publication guidance](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace).

For Claude chat and managed workspaces, test the supported plugin upload or organisation distribution flow and verify that skills accompany the connector. A custom MCP connector alone does not install skills. Organisation sync has separate access rules; a public Claude Code marketplace is not automatically an organisation-managed marketplace. See [organisation distribution](https://code.claude.com/docs/en/plugin-marketplaces#distribute-through-organization-settings).

## Acceptance cases for both hosts

Use a dedicated test account and synthetic invention material. Record public package versions, endpoint, host, date and actual results. These are expected outcomes, not claims of completed host tests.

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
| Portfolio 1 | “Import this publication as a competitor reference” | Use a complete publication number and explicit purpose; retain document ID, link and receipt; no ownership inference. |
| Portfolio 2 | “Import our portfolio” with accepted legal names, duplicate hits and multiple pages | Check assignee evidence, follow nextPage, deduplicate repeated publication hits and use the platform’s application-conflict handling, import the authorised scope without repeated approval. |
| Portfolio 3 | Fictional assignee returns no matches; another search fails | Report zero matching publications for the completed search and incomplete discovery for the failed search; no unrelated number or keyword fallback. |
| Portfolio 4 | Ambiguous company, former name and joint applicants | Keep evidence and unresolved entities separate; do not assume every variant is own or every other assignee a competitor. |
| Portfolio 5 | Import times out after save; later call returns already_imported with partial or null receipt | Retry the same publication/purpose in a bounded way, preserve warnings or unknown completion, and do not claim refresh or create duplicates. |
| Portfolio 6 | Refresh saved own patents after relatives are imported; repeat refresh | Use saved document IDs, report the family update outcome and remaining uncertainty; no implicit import of missing relatives. |
| Portfolio 7 | Family update is partial or fails; competitor or missing tool selected | Explain missing applications or uncertain family information, retry only transient failures, and report unsupported scope or capability honestly. |
| Portfolio 8 | Application/purpose conflict during a partially completed batch | Preserve successful records, report conflicts and pending entries, do not change identifiers or purpose to bypass the conflict. |
| Portfolio 9 | “Keep our portfolio updated” | Discover new filings and update family grouping for selected own patents; explain that text, assets and legal status are unchanged and no schedule was created. |

Exercise fresh and existing connections to the Lightbringer MCP service, then scan and submit the tested packages. Package versions are separate from service updates. Existing installations can retain old automatic-submission instructions until updated; confirm that registration alone does not request patent preparation.

Verify `list_tasks` recovery and `delete_task` with write consent. Task reads require ownership and current access to the associated innovation; owners can delete their own task history after losing access to the innovation. Tasks and findings expire after 30 days, and reads do not extend retention. Deletion does not cancel analysis or withdraw a patent-preparation request. Public discovery alone does not verify these authenticated workflows.
