---
name: innovation-capture
description: Identify, register and enrich Lightbringer innovations from a conversation, an inventor interview or authorised technical sources. Use for saving an idea, updating an innovation, extracting innovations from documents or engineering work, and patent mining. Exploration alone does not authorise saving; patent-preparation requests and document reviews are separate workflows.
---

# Innovation capture

Identify innovations and, when requested, register or enrich traceable records. An innovation can be a vague idea or a detailed technical description; it does not need to be patent-ready. Read [service conduct](references/service-conduct.md).

## Scope and context

Use the connected organisation and the user's existing technical context. Establish which sources are in scope and whether the user wants analysis, registration or an update. Carry out requested saves without asking for the same approval again. Clarify an ambiguous record, source scope or requested change before acting. An exploration-only request does not authorise saving findings.

Use the adopted IP strategy when available. Retrieve relevant strategy reports through `search` and `fetch`; distinguish proposed changes in uploaded documents or meeting notes from the adopted strategy. Record fit and uncertainty without discarding innovations for low alignment or uncertain patentability.

## Gather supported context

Adapt to the request; a conversation can lead to source exploration and back again.

- **Conversation or inventor interview:** reuse what the user already supplied. Ask focused questions about missing context, one theme at a time: the idea, problem, proposed approach, implementation, observed benefit and evidence. Separate facts, inferences and open questions.
- **Source exploration or patent mining:** read [source exploration](references/source-exploration.md). Investigate the authorised material, trace supporting evidence and retain identified innovations even when incomplete. Do not require a broad mining exercise for a single idea.

## Match, register or enrich

1. Search for the same concept with `search` and `list_innovations`; read likely matches with `get_innovation` or `fetch`. Compare the idea and mechanism, not just titles. Reuse an existing record, including a previously rejected one when factual enrichment is relevant and permitted. Preserve decisions and sources; never create a duplicate to bypass a restriction.
2. For a new record, retrieve `get_innovation_template` and read [authoring guidance](references/lightbringer-authoring.md). Draft from supported context and validate with `validate_innovation`. Save with `register_innovation` only when registration is authorised. If the schema cannot represent the available information honestly, retain the innovation in the summary as pending registration and identify the missing inputs.
3. For an existing record, read its latest content and use `update_innovation` with complete replacement text for the sections being changed. Preserve earlier supported content. Follow the tool's section names; they differ from the registration payload fields.
4. If refinement is requested, use `get_innovation_feedback`. This is automated analysis of the description, not a novelty search or professional assessment. For pending analysis, use `check_task_status`. Apply authorised improvements supported by the evidence; leave remaining gaps explicit.

## Completion

Return a chat summary of findings and actual outcomes. Include saved record IDs/links, the evidence used, related records and remaining questions. For exploration, state source coverage and distinguish identified innovations, unresolved problems and sources with no findings. Clearly separate analysis-only findings and failed or pending saves from registered records. A file is optional; local filesystem access is not required. Drawing descriptions do not establish that files were uploaded.

Registration or enrichment completes this workflow. For an explicit request to have Lightbringer prepare a selected innovation for patent filing, continue with `patent-preparation` when installed, retaining the user's stated intent. If that skill is unavailable, follow the connected `prepare_for_patent_filing` instructions for that separate request. For review comments or decisions, use `patent-review` when installed or the connected review guidance.
