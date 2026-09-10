---
name: patent-preparation
description: Request Lightbringer's preparation of a selected innovation for patent filing and explain the returned status and next steps. Use when the user explicitly wants Lightbringer to patent an innovation or start patent preparation. Registration, general patent-service questions and review responses are separate workflows.
---

# Patent preparation

Record the user's request for Lightbringer to prepare a selected innovation for patent filing. Completion means the service confirms that preparation was requested. Read [service conduct](references/service-conduct.md).

## Identify the innovation

Use the connected organisation and resolve the selected record with `list_innovations` or `search`; read it with `get_innovation`. Clarify an ambiguous selection. If the innovation is not registered, use `innovation-capture` when installed, retaining the user's patenting intent for that concept. If capture guidance is unavailable, follow `get_innovation_template` and call `register_innovation` with supported content as part of the requested preparation. Registration validates before saving: report any missing inputs or validation errors before attempting preparation. Successful registration can include non-blocking warnings; report them without re-registering the record.

Refinement is optional. Offer it only when the user asks for it or the service reports a blocking requirement. Do not require automated feedback, a completeness interview or revisions before recording an explicit preparation request. For requested refinement or a service-reported blocker, carry the record ID and relevant gaps into the capture workflow, preserving the user's preparation intent. Do not invent technical detail or register a duplicate.

## Record the preparation request

1. Establish explicit intent to have Lightbringer prepare this innovation for patent filing. A request to finish a description, explore sources or register findings is not that intent. Do not ask for the same decision again when the user has already expressed it clearly.
2. Explain that the action requests Lightbringer's patent-preparation workflow and triggers notification emails to the assigned specialist and inventor. Call `request_patent_preparation` with the selected record identifier, using the connected tool schema.
3. Report the actual returned status and record link: `submitted=true` means preparation was newly requested; `alreadySubmitted=true` means it was already requested and the call made no new request. Neither confirms completed preparation or email delivery. State any requirements or next action supplied by the service. If the tool is unavailable or the request fails, explain that preparation has not been confirmed and offer the same record in the Lightbringer application or a continuation with the team.

## Completion and continuation

A recorded preparation request does not establish that a separate invention disclosure was created, a paid engagement was accepted or a patent was filed. Report those outcomes only if the service explicitly confirms them. Payment and acceptance steps require a human handoff.

For a subsequent review from the patent team, use `patent-review` when installed or the connected review guidance. General advice, strategy, novelty assessments and other professional-service requests are outside this workflow; use the service's available instructions and continuation routes.
