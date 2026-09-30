# Strategy MCP workflow

Use the schemas advertised by the connected service. Strategy reads use read consent; writes use write consent and strategy management rights, including customer moderators. `get_strategy_template` also requires strategy management rights. A tool being visible does not guarantee permission for a selected record.

## Resolve the intended record

For an existing Strategy, use the user's identifier or resolve it with `list_strategies`, then read `get_strategy`. Its response provides the current title, Markdown sections with identifiers, revision and link. Use this structured read for editing; a flattened `fetch` result does not supply the edit contract.

For a new Strategy, `get_strategy_template` supplies current capture guidance, readiness criteria, a creation schema and a fictional example. Follow the guide before capture and creation. Similar strategies can coexist, including multiple published strategies. Do not convert a request for a new product strategy into an update solely because a title looks similar. Clarify genuinely ambiguous create-versus-revise intent before writing.

## Create a populated draft

`create_strategy` takes a title and an ordered array of sections containing `title` and Markdown `content`. Use substantive, nonempty bodies and the current guide's schema. Do not send invented section IDs, publication settings or extra fields. Creation validates before saving and returns the saved ID, reference, draft status, URL and revision.

Summarise the proposed direction and remaining uncertainties as the guide describes. Honour an existing instruction to draft or save; do not ask for duplicate confirmation. Analysis or exploration alone does not authorise saving. If nothing can support an objective and scope, explain the missing basis instead of saving boilerplate.

- **Explicit validation rejection:** nothing was created. Correct the indicated fields using supported facts and retry when the correction is clear. Schema validation is not a legal or professional quality assessment.
- **Timeout, transport failure or unclear success receipt:** the save may have happened. Inspect `list_strategies` and likely records with `get_strategy` before any retry. Compare available content and identifiers; title similarity alone is insufficient. If the outcome remains ambiguous, retain the unsaved/uncertain work and explain the limitation rather than risk a duplicate.
- **Successful creation:** retain the returned ID and link for refinement. A warning does not justify creating a second record.

Creation completes with `DRAFT`. It does not publish, request preparation or update related assets.

## Edit the same Strategy

Read `get_strategy` before editing. Call `edit_strategy` with the selected `strategy_id`, the revision from that read and an atomic batch of operations. The revision is an opaque concurrency value, not a document version to generate or increment.

| Operation | Use |
| --- | --- |
| `replace_section` | Supply the observed `section_id` and the complete replacement `content`, `title`, or both. Preserve unaffected text, Markdown, links and attachment references. It is not a quoted-substring patch. |
| `insert_section` | Supply `section: {title, content}` and an optional position `index`; the service assigns the new identifier. Read returned identifiers before later addressing the new section. |
| `delete_section` | Remove a selected section only when that removal follows the requested change. At least one section must remain. |
| `reorder_sections` | Include every current section identifier exactly once in `section_ids`. |
| `rename` | Supply the new strategy `title`. |

Use the smallest coherent set of changes that satisfies the request. Whole-document regeneration can unnecessarily disturb collaborators' work and discussions. An update to a published strategy changes that record; do not assume it becomes a draft or automatically unpublish it.

The batch is atomic: an explicit rejection means its changes did not apply. On revision conflict, read again and reconcile the requested change with the latest content. Preserve intervening edits; do not resend a stale full-section replacement using only a fresh revision. If the new content creates a material decision conflict, resolve that specific issue before writing.

The service preserves unchanged text and comment anchors and tracks replacements. It can reject ambiguous text matching or edits that touch pending review changes. Explain that blocker and provide the record link for continuation in the application editor. Do not remove/reinsert a section, create a replacement Strategy or repeatedly retry to bypass the restriction.

Inspect the returned content, revision and `orphaned_discussion_ids`. Nonempty IDs mean retained discussion threads have lost their text anchors; report this effect rather than claim the comments were deleted. An uncertain edit outcome requires readback and comparison before retrying. Preserve confirmed edits and describe unresolved ones.

## Publication and deletion

Use `set_strategy_publication` only for an explicit request to publish or return the selected Strategy to draft, with `publish: true` or `false`. Read the selected record so the intended content and identity are clear, then inspect the returned status. Existing explicit authorisation is sufficient; a drafting request does not supply publication authorisation. Publishing one Strategy does not unpublish others and does not establish that professional review occurred.

Use `delete_strategy` only when the user explicitly requests permanent deletion of the resolved Strategy. Do not delete as a workaround for capture, editing or publication failures.

If required tools or permissions are missing, explain the blocked action and retain the proposed work. Never report a saved, published or deleted outcome without service confirmation. Use the returned URL and an established application origin when needed; do not invent a record link or confuse the MCP endpoint with the application URL.

## Separate strategy from execution

Writing an action into Markdown does not execute it. Do not infer tools for strategy feedback, automated portfolio analysis, jurisdictional coverage assessments, professional-service milestones or monitoring configuration from a related tool name.

When the user separately requests innovation registration, patent imports, filing preparation or formal review responses, use the appropriate installed workflow or the connected tool guidance. Keep strategy authorship, automated findings, professional work and actual record changes distinct in the result.
