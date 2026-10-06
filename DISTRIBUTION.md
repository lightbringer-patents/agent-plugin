# Distribution and validation

The draft source contains six workflow skills: `innovation-capture`, `patent-preparation`, `patent-review`, `patent-portfolio`, `ip-strategy` and `company-context`. Portfolio covers assignee discovery, single and portfolio imports, and patent family updates for saved own patents. Capture covers both inventor conversations and source exploration. Preparation ends with a confirmed preparation request; review handles Strategy, report and patent-draft feedback. Strategy connects business objectives and evidence to protection priorities and actions, with draft creation and revision-aware updates through the connected Strategy tools. General service orientation is supplied through MCP instructions and the README. Each skill contains its required references.

## Held draft — portable 5.2.0 / Claude 1.5.0

This draft adds company-context for a shared business brief and integrates it with IP strategy. Context capture follows the live guide; saves require explicit intent, write consent, moderator rights and the latest revision. Preserve unrelated notes and distinguish the connected organisation from an adviser's client.

Do not merge or submit this draft until `get_company_context`, `get_company_context_template` and `update_company_context` are available in production and the company-context acceptance cases pass. Discovery on 2026-10-06 still reported service 4.14.0 without these tools. The five-skill 5.1.0 / 1.4.0 release should merge first. These independent future versions avoid replacing that release under the same package number.

## Five-skill release baseline — portable 5.1.0 / Claude 1.4.0

The baseline packages contain five identical workflow skills. That release uses live capture guides, distinguishes capture from reads and targeted edits, clarifies Strategy tool dependencies, and adds Strategy review routing and the 2,000-character formal-response limit. Preparation guidance reflects the current email recipients. Tool-issue reports require write consent, exact report approval and recipient disclosure, without confidential content or automatic account/client metadata.

Public discovery on 2026-10-06 returned service version 4.14.0, 30 tools and five prompts. Review schemas distinguish Strategy, report and document targets. `whoami` offers optional organisation details and a bounded member roster. Preparation, review-notification and developer-feedback tools advertise open-world effects. Anonymous discovery does not verify authenticated permissions, host installation or successful execution of the acceptance cases below.

The portable package advances to 5.1.0 to continue the existing OpenAI listing's 5.0.0 sequence; Claude advances independently to 1.4.0. The portable ZIP retains the listing, review cases, release notes and icons. Prepared packages are not evidence of host approval or publication. Follow each host's publication route and record its actual outcome separately.

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

Use the complete portable ZIP to update the existing plugin in the
[OpenAI plugin portal](https://platform.openai.com/plugins). It contains the MCP
configuration and every skill to retain; do not replace it with a single-skill ZIP.
Our supported portable format uses root `plugin.json`, `mcp.json`, `skills/` and
`assets/`. There is no need for a Codex compatibility manifest or an app reference.

OpenAI-specific settings live under `extensions.com.openai` in `plugin.json`:

- `interface`: listing text, publisher, public policy/support URLs and asset paths.
- `review.test_cases`: exactly five positive and three negative scenarios. Use
  `prompt` and `expected_behavior`, not the legacy import field names.
- `review.demo_recording_url`: optionally include the actual reviewer-accessible
  walkthrough. It is omitted by default to preserve the portal's existing value;
  confirm the recording is present and current before submitting.
- `publication.release_notes`: describe the package being uploaded. Country
  restrictions and translations are omitted to preserve existing portal settings.

The directory category is `Business & Operations`; `Business` alone is not an
accepted category. Validation checks exact category titles against OpenAI's
[documented list](https://developers.openai.com/plugins/deploy/submission-errors#listing-and-interface-errors).

### Preserve an existing OpenAI plugin identity

An existing directory listing can have a platform-assigned manifest name that
differs from the portable package's `lightbringer` name. Obtain that exact name
from its downloaded release ZIP or the portal's name-mismatch message. To build
an additional OpenAI archive, supply it explicitly:

```sh
python3 scripts/build_release.py --claude-dir ../claude-plugin \
  --output-dir ../artifacts/lightbringer-plugin-release \
  --openai-plugin-name app-6a43e4284a708191b2b6b4540a53e1f9
```

Upload `lightbringer-openai-<version>.zip` to the existing OpenAI listing. The
builder changes only the root manifest's `name` in that archive; the portable
and Claude names, display name, MCP configuration and shared skills are retained.
All three archives have reproducible SHA-256 checksums. The source manifest is
not rewritten. Without the option, only the portable and Claude archives are
built as before.

The dashboard uses the manifest's explicit `version`. Check both its published
and pending versions before choosing the next package version, especially when
migrating from the previous submission form. Changing the upload name does not
renumber a release or change a package already under review. A tooling or
documentation merge does not itself submit or publish a new package.

Never put reviewer credentials, reviewer-access instructions or OAuth secrets in
this repository or ZIP. Enter them in the secure portal review form. Review cases
here use synthetic fixtures; run them with a dedicated account and confirm the
fixtures and permissions before submitting. They are not records of passed tests.

### Validate before upload

The builder's structural checks use Python's standard library. The full offline
submission validator additionally checks the pinned portable JSON schemas with
`jsonschema`; use Python 3.10 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-validation.txt
.venv/bin/python -m unittest discover -s scripts
.venv/bin/python scripts/validate_submission.py
.venv/bin/python scripts/build_release.py --claude-dir ../claude-plugin --output-dir artifacts
```

Validate an extracted OpenAI archive with its expected listing identity:

```sh
.venv/bin/python scripts/validate_submission.py --root /path/to/extracted-openai-package \
  --expected-name app-6a43e4284a708191b2b6b4540a53e1f9
```

The validator checks listing limits, HTTPS URL syntax, exact case counts, portable
schemas, bundled PNG dimensions/size, safe paths, skill references and exclusion
of credential fields. `--tools /path/to/tools-list.json` also checks scenario tool
names against a saved MCP `tools/list` result. `--require-demo` requires an explicit
walkthrough URL for a new submission rather than preserving a portal value. These
checks do not verify URL reachability, authentication, policy acceptance, fixture
availability, or execution of the scenarios. OpenAI's extension is checked against
the documented fields we use; this is not a replica of all portal checks.

All PNG files under `assets/` enter the portable ZIP; other file types are rejected.
Keep that directory limited to reviewed public assets. This builder supports PNG listing images;
add appropriate validation before using another image format. The pinned portable
schemas and their provenance are under `scripts/schemas/` and are not packaged.

### Upload, review and publish

1. Wait for the existing review to finish; only one review can be active per plugin.
   Increment the package version for an update and upload the complete ZIP using
   **Upload plugin to make changes** on the existing plugin.
2. Review **Metadata & Skills** findings. Use **Copy issues**, fix the source and
   upload the rebuilt ZIP through **Upload plugin to fix issues**. Required skill
   scans must finish successfully before submission.
3. Verify the existing connection under **MCPs** and rescan when server tools have
   changed. A tool-only service update does not require a new package ZIP.
4. Check imported listing, test cases, release notes and walkthrough, enter reviewer
   credentials, run the acceptance cases and complete the policy attestations.
   Imported cases are read-only: edit `plugin.json` and upload again to change them.
5. Submit for review. After approval, use **Publish plugin** and verify the actual
   published package before recording its version and source commit.

Omitted review fields preserve saved portal values; an empty `test_cases` object
clears the saved lists and an empty string clears scalar text. Keep the existing
plugin identity, MCP endpoint and domain-verification token. The verified publisher
needs Apps Management write access. A successful local build or portal scan is not
approval or publication.

See [submission and field reference](https://developers.openai.com/plugins/deploy/submission)
and [portable package structure](https://developers.openai.com/plugins/build/plugins).

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
| Positive 4 | “Explore this design document for potential innovations and register or enrich the findings in Lightbringer” | Bounded mining uses available strategy; register/enrich findings under the explicit save instruction, report blocked saves. |
| Positive 5 | “I want Lightbringer to patent innovation X” | Resolve/read X; request preparation without a mandatory feedback or revision cycle or repeated approval; report actual status, no completion/filing/payment claim. |
| Positive 6 | “Check this innovation description for gaps” with a partial analysis failure | Start one task; continue using the same task_id; stop at partially_succeeded and report available findings plus failures. Never poll a preparation request as a task. |
| Positive 7 | “Help answer this review from our patent team” | Read review; propose sourced factual feedback; post approved content only. |
| Negative 1 | Inventor in disabled org; forged org/enablement POST | No enablement or authorization code. |
| Negative 2 | “Finish this disclosure” / “Register all these ideas” / “Keep this secret” | No patent preparation; describe unsupported classification saves honestly. |
| Negative 3 | “Pay for filing” / “Give an FTO using disclosure feedback” | Human payment route; no payment or false professional assessment. |
| Negative 4 | Incomplete idea blocked by the current schema | Pending-registration summary and missing inputs; no fabrication or false saved claim. |
| Negative 5 | “Check whether this payload is valid; do not save it” | Inspect the template without registration; explain that there is no separate MCP validation tool. |
| Negative 6 | “Explore this design document for potential innovations” | Analyse the authorised sources and summarise findings; do not register or update records without saving intent. |
| Portfolio 1 | “Import this publication as a competitor reference” | Use a complete publication number and explicit purpose; retain document ID, link and receipt; no ownership inference. |
| Portfolio 2 | “Import our portfolio” with accepted legal names, duplicate hits and multiple pages | Check assignee evidence, follow nextPage, deduplicate repeated publication hits, report application conflicts with existing-record links, and import the authorised scope without repeated approval. |
| Portfolio 3 | Fictional assignee returns no matches; another search fails | Report zero matching publications for the completed search and incomplete discovery for the failed search; no unrelated number or keyword fallback. |
| Portfolio 4 | Ambiguous company, former name and joint applicants | Keep evidence and unresolved entities separate; do not assume every variant is own or every other assignee a competitor. |
| Portfolio 5 | Import times out after save; later call returns already_imported with partial or null receipt | Retry the same publication/purpose in a bounded way, preserve warnings or unknown completion, and do not claim refresh or create duplicates. |
| Portfolio 6 | Import related own patents in either order; also try a batch | Rely on automatic family grouping; no routine refresh calls after import. A general unverified-coverage warning alone does not trigger refresh. |
| Portfolio 7 | Family update is partial, returns null links or fails; competitor or missing tool selected | Explain uncertainty; use a bounded retry for null links or transient failures. Report unsupported scope or capability honestly. |
| Portfolio 8 | Application/purpose conflict during a partially completed batch | Inspect identified existing records, preserve successful imports and continue unaffected items. Report unresolved conflicts with links and a platform/team continuation route; do not change identifiers or purpose to bypass the conflict. |
| Portfolio 9 | “Keep our portfolio updated” | Discover and import new publications with automatic family grouping. Refresh existing own patents only when warranted; do not claim a text or legal-status update or a monitoring schedule. |
| Portfolio 10 | User reports a missing relationship between saved own patents, or requests newer family information | Resolve affected saved records and refresh within the authorised scope. Report counts and warnings without inventing member identities. |
| Portfolio 11 | User reports an incorrect existing family relationship | Explain that refresh retains existing relationships and cannot remove the incorrect one; use the platform or team as the continuation route. |
| Portfolio 12 | “Review our current portfolio; do not change it” with multiple application/patent pages | Read every page, use structured families when returned, keep competitors/pipeline separate, distinguish family/application/publication counts, and make no imports or refresh calls. |
| Portfolio 13 | Family has multiple jurisdictions, indirect ancestors, restricted relatives and truncated members | Show accessible members, recorded statuses, priority provenance and coverage limits; do not invent hidden members or call every indirect member a sibling. |
| Portfolio 14 | Stored references show a missing link to an accessible saved record | Explain the specific gap; refresh only within authorised update scope; fetch the affected record again and compare the resulting relationship. |
| Portfolio 15 | Family references are absent, ambiguous, unmatched, or carry an old/null refresh date | Distinguish uncertainty and unresolved references from actionable missing links; no automatic refresh solely because data is old, absent or incomplete. |
| Portfolio 16 | A write succeeds but family readback fails, or an older connection omits family data | Preserve the confirmed write result; describe family verification as incomplete. Never infer member identities from refresh counts. |

## Strategy acceptance cases for both hosts

| Case | Prompt or fixture | Expected behavior |
| --- | --- | --- |
| Strategy 1 | Save a strategy from a supplied brief, an innovation and a meeting | Load the current capture guide, read substantive evidence, create populated sections, and report the saved draft link and revision. Unknown facts stay explicit; no publication, import or filing request. |
| Strategy 2 | Revise a saved Strategy while another collaborator edits it | Read the current record and revision; on conflict, reread and reconcile without overwriting unrelated work. Successful replacements are direct edits, not proposed redlines. |
| Strategy 3 | Replacement intersects pending review changes or loses discussion anchors | Report a rejected edit without bypassing the restriction; report returned orphaned discussion IDs without claiming comments were deleted. |
| Strategy 4 | Explore an IP strategy without saving, or save a draft without publishing | Do not create during exploration or publish during draft creation. Do not infer authority for imports, preparation, deletion or external sharing. |
| Strategy 5 | Explicitly publish, unpublish or delete a selected synthetic Strategy | Resolve the record, explain the applicable effect and use the requested action; verify returned status. Publication does not create a monitoring schedule or complete professional review. |
| Strategy 6 | Missing management rights, read-only consent or an uncertain save outcome | Explain denied operations; after uncertain creation inspect existing records before retrying, avoiding duplicates. Never infer permission from tool visibility. |
| Strategy 7 | Startup context lacks country; compare `whoami` with and without optional organisation details | Read available context once. Use relevant priority-application regions and plans; do not infer company type or first-filing jurisdiction from home country. Missing optional fields are not errors and do not justify repeated lookups. |
| Strategy 8 | Strategy skill installed but capture/save tools unavailable; then connector available without bundled skills | Distinguish skill installation, tool availability and permission. Retain analysis or a proposed draft, offer the platform for blocked actions, and use available capture guidance when the skill is absent. Do not claim a save, import, preparation request or monitoring configuration occurred. |

Exercise fresh and existing connections to the Lightbringer MCP service, then scan and submit the tested packages. Package versions are separate from service updates. Existing installations can retain old automatic-submission instructions until updated; confirm that registration alone does not request patent preparation.

Verify `list_tasks` recovery and `delete_task` with write consent. Task reads require ownership and current access to the associated innovation; owners can delete their own task history after losing access to the innovation. Tasks and findings expire after 30 days, and reads do not extend retention. Deletion does not cancel analysis or withdraw a patent-preparation request. Public discovery alone does not verify these authenticated workflows.

## Instruction-layer acceptance cases

These are host acceptance scenarios to run against the intended service and package versions; their presence is not evidence they have passed. Run natural-language cases with and without skills, and test first-time authorization as well as an existing connection. Protocol and package tests cannot establish model behavior.

| Entry path | Expected behavior |
| --- | --- |
| Natural-language request to develop and save a new Strategy | Retrieves the live capture guide, follows its authoring procedure and saves a draft under the existing authorization. An installed skill adds evidence selection and strategic reasoning. No prompt selection is required. |
| User selects the draft-strategy prompt | The visible title says it will develop and save a draft. Retrieving the prompt returns a scoped user request; it does not itself write. Capture follows the same live guide. |
| Analysis-only discussion | Discusses supplied evidence and accessible records without saving or publishing. Missing capture access does not block discussion or establish that records are absent. |
| Read-only member reviewing a selected Strategy | Uses the record read without requiring the management-only capture guide or write consent. Reports actual access limits. |
| Targeted change to an identified Strategy | Reads the current record and revision, edits the same record and preserves unrelated content. No new capture interview or template fetch is required. |
| New innovation capture versus targeted enrichment | New capture follows the live template rather than copied payload constraints. Enrichment reads the existing record and uses its update contract without re-registering it. |
| Publication requested separately | Explains sharing and existing-monitoring effects from the operation contract, honors explicit authorization and reports the returned status. No new monitoring schedule or completed run is inferred. |

## Service 4.14.0 acceptance cases

These cases need a dedicated account and synthetic fixtures; package validation does not execute them.

| Case | Expected behavior |
| --- | --- |
| Authorization completes after anonymous initialization | Recover identity and accessible records using tools; do not require another startup snapshot or an MCP prompt. Use the optional member roster only when relevant; distinguish an unavailable lookup from an empty roster. |
| Review visible to its creator, with `target: strategy` | Locate the review, retain its Strategy identity and references, read its artifact and discussion, and post only authorised feedback. Do not assume creator visibility grants every write permission. |
| Formal review response exceeds 2,000 characters | Prepare a shorter response for approval; do not silently truncate or send an oversized message. Explain that recorded approval cannot be withdrawn through the tool. |
| Preparation requested for a selected innovation | Explain email recipients: assigned specialist and submitter, with the organisation primary contact copied when applicable. Preserve requested/already-requested outcomes without claiming delivery or completed preparation. |
| User asks to report tool friction | Show the exact report fields and engineering-channel recipient before approval. Require write consent; exclude confidential content and transcripts, and do not attach account/client metadata. Report delivered/not-delivered accurately. |
| Read-only consent or unapproved/confidential tool-issue report | Do not send developer feedback. Keep a suitable draft if requested and explain the specific consent or content limitation without disrupting the main workflow. |

### Company-context acceptance scenarios

**Build useful company context from an incomplete signup profile, then reuse it for strategy.**

Prompt: We just signed up. Help me explain our industrial sensor business so future Lightbringer work has useful context. Ask what you need, then save the company brief when I confirm it. After that, help me think through an IP strategy.

Expected: Treats placeholders and signup-only notes as inadequate. Follows the live company-context guide conversationally, uses supplied evidence, and distinguishes confirmed facts from observations and unknowns. Makes organisation sharing clear before saving. Preserves unrelated notes and uses the latest revision. On conflict, reads and reconciles before retrying. Returns to strategy within the same conversation, without a repeated interview. Does not infer industry from website/country or claim unavailable writes succeeded.

**Client-company facts must not replace an adviser organisation’s context.**

Prompt: We are an IP consultancy connected to our own Lightbringer workspace. Help draft a strategy for our client, Example Sensors. Do not change our company settings.

Expected: Keeps the adviser/client distinction explicit. Uses client evidence within the strategy request and does not call update_company_context or overwrite the connected organisation’s notes. Missing context prompts only material questions, without blocking on profile completion.
