# Strategy MCP workflow

Use the schemas advertised by the connected service. Strategy reads use read consent; writes use write consent and strategy management rights, including customer moderators. `get_strategy_template` also requires strategy management rights. A tool being visible does not guarantee permission for a selected record.

## Choose the available interface

The service may expose Strategy-specific tools, shared asset tools, or both.
These interfaces address the same Strategy records. Choose from the tools and
schemas advertised by this connection, not the host name or installed package
version. Installing a skill does not make a tool available.

Prefer each available asset operation for new work. If that operation or its
required read contract is not advertised, use its available Strategy-specific
counterpart before attempting the write. Retain that choice for the intended
write. Errors, conflicts, denied access and uncertain responses are not signals
to switch tool families and replay the request. Read back and reconcile first.
Never create a duplicate Strategy to change interfaces; the user does not need to
choose between them or migrate records.

| Operation | Preferred when advertised | Compatibility path |
| --- | --- | --- |
| Discover/read | `search` with `category: "strategy"` when that category is supported; `fetch` returning complete `asset` state | Available `list_strategies` and `get_strategy` |
| Create | `create_asset` with `asset.type: "strategy"` and `asset.data` | `create_strategy` |
| Update | `update_asset` with the reference, revision and desired changes from a complete structured fetch | `get_strategy` followed by `edit_strategy` using its existing operation schema |
| Delete | `delete_asset` with the resolved typed reference | `delete_strategy` |

Use canonical references from results: asset tools use `report:<id>`; legacy tools
use the corresponding bare Strategy ID. Do not invent a `strategy:` prefix.
A plain-text fetch without `asset.data` and `asset.revision` is not a complete
asset-edit read. New capture still uses `get_strategy_template`; its guide owns
readiness and document content, while the chosen write tool's advertised schema
owns the envelope. A guide example naming a legacy tool does not require using
that interface when its asset counterpart and necessary reads are available.
Publication stays on `set_strategy_publication` in both paths.

## Tool and skill dependencies

Discover the tools and schemas in the current connection before offering actions. Installing this skill does not add tools or grant access; connecting the MCP service alone does not install the other skills.

| Step | Tool dependency | If unavailable or denied |
| --- | --- | --- |
| Company context | `get_company_context`; `get_company_context_template` for material capture gaps; `whoami` when account identity needs verification | Use supplied context and explain missing reads. Identity, country and website do not establish company type or filing jurisdiction. Saving shared context separately requires `update_company_context`, explicit intent, write consent, moderator rights and the latest revision. |
| Read or assess a Strategy | The available structured read/discovery path above | Explain lookup limits without claiming no strategies exist. Reading does not depend on the capture guide or management rights. |
| New capture | `get_strategy_template` | The guide requires Strategy management rights even with read consent. If unavailable, continue discussion of supplied material without inventing a capture procedure or payload. |
| Supporting evidence | `list_innovations`, `get_innovation`, `search`, `fetch`, as relevant to the brief | State source/access limits; do not require every source for every strategy or infer that absent results mean no IP exists. |
| Save or revise | The chosen create/update path above; write consent and record permissions | Keep the proposed draft in the conversation and offer continuation in the platform. Do not promise a connector save or use a different write tool as a substitute. |
| Publication | `set_strategy_publication` and explicit publication intent | A saved draft remains a draft. Do not claim monitoring context has been updated. |

Use supplied evidence and the shared brief from `get_company_context` for company background; use startup context or `whoami` for identity. Do not repeatedly fetch absent optional fields. Read application-region metadata through `search` and `fetch` for filing context, keeping recorded region, planned first filing and home country distinct. For a focused patent-text question, use the selected sections and pagination described in the [portfolio retrieval guide](../../patent-portfolio/references/saved-portfolio.md); use unfiltered reads when family or part metadata is needed.

Related skills are conditional handoffs, not prerequisites for strategy discussion: use [innovation-capture](../../innovation-capture/SKILL.md) for separately authorised innovation capture or updates, [patent-portfolio](../../patent-portfolio/SKILL.md) for portfolio work or authorised imports, and [patent-preparation](../../patent-preparation/SKILL.md) only for an explicit preparation request. If a related skill is not installed, use the available tool guidance; if its required tools are missing, explain the blocked action. A strategy save does not execute these workflows. Publication supplies context to existing competitor monitoring; no monitoring-configuration tool or skill is implied.

## Resolve the intended record

For an existing Strategy, resolve the user's identifier through the available discovery path and read the selected record. A complete asset fetch provides `asset.type`, `asset.id`, `asset.revision` and `asset.data` containing title and ordered Markdown sections with IDs. Fetch without patent-specific `include`, `mode` or `cursor` options for this state. If that structured read is unavailable, use `get_strategy` and its matching legacy edit contract. Follow search pagination where present; a first page is not a complete inventory.

For a new Strategy, `get_strategy_template` supplies current capture guidance, readiness criteria, a creation schema and a fictional example. Follow the guide before capture and creation. Similar strategies can coexist, including multiple published strategies. Do not convert a request for a new product strategy into an update solely because a title looks similar. Clarify genuinely ambiguous create-versus-revise intent before writing.

## Create a populated draft

Follow the live capture guide for readiness, authoring, creation payload and save recovery. Use the chosen `create_asset` or `create_strategy` contract for validation and returned fields; use the current advertised schema rather than a remembered payload. Honour existing save authorisation without asking for the same approval again. Exploration alone does not authorise a save.

Retain the confirmed ID and link for refinement. Creation saves a draft; it does not publish, request preparation or update related assets.

## Edit the same Strategy

For `update_asset`, read complete structured state with `fetch` first. Supply the returned typed reference and revision, with `changes.title` and/or `changes.sections`. Omitted fields stay unchanged. A supplied sections array is the **complete desired ordered collection**: keep every section that must remain, preserve existing IDs, omit IDs only for new sections, and retain unchanged content. Omitting an existing ID deletes that section. Empty body text clears it; null is not a clearing instruction. Use the advertised limits and required fields.

For the compatibility path, read `get_strategy`, then call `edit_strategy` with its bare `strategy_id`, revision and an atomic batch of advertised operations. Do not send asset fields to that tool or operation arrays to `update_asset`.

In both paths, the revision is an opaque concurrency value, not a document version to generate or increment. A targeted edit needs the current record and tool contract, not the creation template.

Use the smallest coherent set of changes that satisfies the request. Whole-document regeneration can unnecessarily disturb collaborators' work and discussions. An update to a published strategy changes that record; do not assume it becomes a draft or automatically unpublish it.

Both update paths are atomic: an explicit rejection means its changes did not apply. On revision conflict, read again and reconcile the requested change with the latest content. Preserve intervening edits; do not resend a stale full-section replacement using only a fresh revision. If the new content creates a material decision conflict, resolve that specific issue before writing.

Replacements apply directly as the user's edits; the service preserves unchanged text and comment anchors and does not record them as suggestions for later acceptance. It can reject ambiguous text matching or edits that touch pending review changes made in the application editor. Explain that blocker and provide the record link for continuation in the application editor. Do not remove/reinsert a section, create a replacement Strategy or repeatedly retry to bypass the restriction.

Inspect the write receipt, returned revision and `orphaned_discussion_ids`; use the chosen read path for full current content when the receipt does not include it. Nonempty IDs mean retained discussion threads have lost their text anchors; report this effect rather than claim the comments were deleted. An uncertain edit outcome requires readback and comparison before retrying. Preserve confirmed edits and describe unresolved ones.

## Publication and deletion

Publishing makes the Strategy organisation-wide context for members and Lightbringer agents. Published strategies are supplied to scheduled competitor monitoring runs, which select relevant strategy content for their analysis; drafts are excluded from this selection. Explain this sharing and automated use before asking the user to approve publication. Publication does not create a monitoring schedule, start an immediate run or confirm that monitoring has completed.

Use `set_strategy_publication` only for an explicit request to publish or return the selected Strategy to draft, with `publish: true` or `false`. Read the selected record so the intended content and identity are clear, then inspect the returned status. Existing explicit authorisation is sufficient; a drafting request does not supply publication authorisation. Publishing one Strategy does not unpublish others and does not establish that professional review occurred.

Use the chosen `delete_asset` or `delete_strategy` operation only when the user explicitly requests permanent deletion of the resolved Strategy. Do not delete as a workaround for capture, editing or publication failures.

If required tools or permissions are missing, explain the blocked action and retain the proposed work. Never report a saved, published or deleted outcome without service confirmation. Use the returned URL and an established application origin when needed; do not invent a record link or confuse the MCP endpoint with the application URL.

## Separate strategy from execution

Writing an action into Markdown does not execute it. Do not infer tools for strategy feedback, automated portfolio analysis, jurisdictional coverage assessments, professional-service milestones or monitoring configuration from a related tool name.

When the user separately requests innovation registration, patent imports, filing preparation or formal review responses, use the appropriate installed workflow or the connected tool guidance. Keep strategy authorship, automated findings, professional work and actual record changes distinct in the result.

## Company context

`get_company_context` reads the shared brief and current revision; `get_company_context_template` returns the live capture guide. These reads require read consent. `update_company_context` requires write consent and moderator rights, and rejects stale revisions. Use the company-context skill when installed to fill material gaps in the same conversation. The current guide supplies the interview; unavailable tools do not justify treating startup identity as a complete business profile. Keep unsaved context available for strategy work when a profile update is unavailable or not authorised.
