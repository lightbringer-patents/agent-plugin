---
name: invention-capture
description: Register a potential innovation from an ongoing technical conversation, interview an inventor, or enrich an existing Lightbringer innovation with new context. Use for "save this idea", "register this innovation", or "update our disclosure". For broad source mining use lightbringer-agent-skill; capture alone does not request patent filing.
---

# Innovation capture and enrichment

Read [service conduct](../lightbringer-agent-skill/references/service-conduct.md). The desired outcome is a saved, traceable record the inventor can enrich over time; patent selection is a later decision.

1. Identify the concept and the user's authority to register or update it. Reuse the technical context already present and the connected organisation identity. Resolve ambiguity about organisation or source scope before saving; do not repeatedly ask permission for a capture the user already requested.
2. Search Lightbringer for the same concept using `search` and `list_inventions`; fetch likely matches. Compare mechanisms and problems, not just titles. Reuse an existing record, including a previously rejected one where new context is relevant and editing is permitted. Preserve prior decisions; do not create a duplicate to bypass a restriction.
3. Retrieve relevant IP strategy reports with `search`/`fetch` when available. Annotate fit without using strategy as a registration gate. Uploaded or meeting-derived strategy may be a proposed change rather than the adopted strategy.
4. For a new record, call `get_invention_template` and read [authoring guidance](../lightbringer-agent-skill/references/lightbringer-authoring.md). Follow the live interactive capture guidance. Ask only for missing facts, one technical theme at a time: the problem, mechanism, implementation, observed benefit and source evidence. Separate facts, inferences and open questions. Potential patentability is not a prerequisite for capture.
5. Validate a supported payload with `validate_invention`, then save with `create_invention`. For existing records, read the latest disclosure and use `update_invention` with complete replacement sections that preserve earlier content. Never guess schema keys. If the current full-disclosure schema cannot represent an incomplete idea honestly, explain that it remains pending registration and ask for the minimum missing context or offer the platform/team route.
6. Return the actual record ID/link, what was registered or enriched, and remaining questions. Creation completes registration even if the platform uses a draft label. Do not call `submit_invention` as a completion step.

Disclosure feedback can help later refinement when requested. It is automated analysis, not a novelty search. If the user explicitly asks Lightbringer to patent the innovation, use `lightbringer-patent-service` for the separate preparation action.

The summary works directly in chat. Offer a file only when supported or requested. Do not assume access to local files or that drawings were uploaded simply because their descriptions were saved.
