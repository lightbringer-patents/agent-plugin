# Strategy MCP workflow

Use the schemas advertised by the connected service. Strategy reads use read consent; writes use write consent and strategy management rights, including customer moderators. `get_strategy_template` also requires strategy management rights. A tool being visible does not guarantee permission for a selected record.

## Tool and skill dependencies

Discover the tools and schemas in the current connection before offering actions. Installing this skill does not add tools or grant access; connecting the MCP service alone does not install the other skills.

| Step | Tool dependency | If unavailable or denied |
| --- | --- | --- |
| Organisation context | Startup context; `whoami` when needed context is missing or the user asks to verify it | Use supplied context and ask only material gaps. `organisation.country`, `state` and `website` are optional; older connections may return only the name. Their absence does not establish company type or filing jurisdiction. |
| Read or assess a Strategy | `get_strategy`; `list_strategies` when the record needs resolving | Explain lookup limits without claiming no strategies exist. Reading does not depend on the capture guide or management rights. |
| New capture | `get_strategy_template` | The guide requires Strategy management rights even with read consent. If unavailable, continue discussion of supplied material without inventing a capture procedure or payload. |
| Supporting evidence | `list_innovations`, `get_innovation`, `search`, `fetch`, as relevant to the brief | State source/access limits; do not require every source for every strategy or infer that absent results mean no IP exists. |
| Save or revise | `create_strategy`, or `get_strategy` plus `edit_strategy`; write consent and record permissions | Keep the proposed draft in the conversation and offer continuation in the platform. Do not promise a connector save or use a different write tool as a substitute. |
| Publication | `set_strategy_publication` and explicit publication intent | A saved draft remains a draft. Do not claim monitoring context has been updated. |

Use existing startup context first. If needed, read `whoami` once for available organisation details; do not repeatedly fetch absent optional fields. Read application-region metadata through `search` and `fetch` for filing context, keeping recorded region, planned first filing and home country distinct.

Related skills are conditional handoffs, not prerequisites for strategy discussion: use [innovation-capture](../../innovation-capture/SKILL.md) for separately authorised innovation capture or updates, [patent-portfolio](../../patent-portfolio/SKILL.md) for portfolio work or authorised imports, and [patent-preparation](../../patent-preparation/SKILL.md) only for an explicit preparation request. If a related skill is not installed, use the available tool guidance; if its required tools are missing, explain the blocked action. A strategy save does not execute these workflows. Publication supplies context to existing competitor monitoring; no monitoring-configuration tool or skill is implied.

## Resolve the intended record

For an existing Strategy, use the user's identifier or resolve it with `list_strategies`, then read `get_strategy`. Its response provides the current title, Markdown sections with identifiers, revision and link. Use this structured read for editing; a flattened `fetch` result does not supply the edit contract.

For a new Strategy, `get_strategy_template` supplies current capture guidance, readiness criteria, a creation schema and a fictional example. Follow the guide before capture and creation. Similar strategies can coexist, including multiple published strategies. Do not convert a request for a new product strategy into an update solely because a title looks similar. Clarify genuinely ambiguous create-versus-revise intent before writing.

## Create a populated draft

Follow the live capture guide for readiness, authoring, creation payload and save recovery. Use the advertised `create_strategy` contract for validation and returned fields; use the current schema rather than a remembered payload. Honour existing save authorisation without asking for the same approval again. Exploration alone does not authorise a save.

Retain the confirmed ID and link for refinement. Creation saves a draft; it does not publish, request preparation or update related assets.

## Edit the same Strategy

Read `get_strategy` before editing. Call `edit_strategy` with the selected `strategy_id`, the revision from that read and an atomic batch of operations. The revision is an opaque concurrency value, not a document version to generate or increment.

Use the advertised operation schemas for complete replacement content, section identifiers and ordering. A targeted edit needs the current record and tool contract, not the creation template.

Use the smallest coherent set of changes that satisfies the request. Whole-document regeneration can unnecessarily disturb collaborators' work and discussions. An update to a published strategy changes that record; do not assume it becomes a draft or automatically unpublish it.

The batch is atomic: an explicit rejection means its changes did not apply. On revision conflict, read again and reconcile the requested change with the latest content. Preserve intervening edits; do not resend a stale full-section replacement using only a fresh revision. If the new content creates a material decision conflict, resolve that specific issue before writing.

Replacements apply directly as the user's edits; the service preserves unchanged text and comment anchors and does not record them as suggestions for later acceptance. It can reject ambiguous text matching or edits that touch pending review changes made in the application editor. Explain that blocker and provide the record link for continuation in the application editor. Do not remove/reinsert a section, create a replacement Strategy or repeatedly retry to bypass the restriction.

Inspect the returned content, revision and `orphaned_discussion_ids`. Nonempty IDs mean retained discussion threads have lost their text anchors; report this effect rather than claim the comments were deleted. An uncertain edit outcome requires readback and comparison before retrying. Preserve confirmed edits and describe unresolved ones.

## Publication and deletion

Publishing makes the Strategy organisation-wide context for members and Lightbringer agents. Published strategies are supplied to scheduled competitor monitoring runs, which select relevant strategy content for their analysis; drafts are excluded from this selection. Explain this sharing and automated use before asking the user to approve publication. Publication does not create a monitoring schedule, start an immediate run or confirm that monitoring has completed.

Use `set_strategy_publication` only for an explicit request to publish or return the selected Strategy to draft, with `publish: true` or `false`. Read the selected record so the intended content and identity are clear, then inspect the returned status. Existing explicit authorisation is sufficient; a drafting request does not supply publication authorisation. Publishing one Strategy does not unpublish others and does not establish that professional review occurred.

Use `delete_strategy` only when the user explicitly requests permanent deletion of the resolved Strategy. Do not delete as a workaround for capture, editing or publication failures.

If required tools or permissions are missing, explain the blocked action and retain the proposed work. Never report a saved, published or deleted outcome without service confirmation. Use the returned URL and an established application origin when needed; do not invent a record link or confuse the MCP endpoint with the application URL.

## Separate strategy from execution

Writing an action into Markdown does not execute it. Do not infer tools for strategy feedback, automated portfolio analysis, jurisdictional coverage assessments, professional-service milestones or monitoring configuration from a related tool name.

When the user separately requests innovation registration, patent imports, filing preparation or formal review responses, use the appropriate installed workflow or the connected tool guidance. Keep strategy authorship, automated findings, professional work and actual record changes distinct in the result.
