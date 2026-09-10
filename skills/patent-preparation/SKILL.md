---
name: patent-preparation
description: Request Lightbringer's preparation of a selected innovation for patent filing and explain the returned status and next steps. Use when the user explicitly wants Lightbringer to patent an innovation or start patent preparation. Registration, general patent-service questions and review responses are separate workflows.
---

# Patent preparation

Record the user's request for Lightbringer to prepare a selected innovation for patent filing. Completion means the service confirms that preparation was requested. Read [service conduct](references/service-conduct.md).

## Identify the innovation

Use the connected organisation and resolve the selected record with `list_innovations` or `search`; read it with `get_innovation`. Clarify an ambiguous selection. If the innovation is not registered, use `innovation-capture` when installed, retaining the user's patenting intent for that concept. If capture guidance is unavailable, follow `get_innovation_template`, validate supported content with `validate_innovation`, and register with `register_innovation` as part of the requested preparation. Report any missing inputs or failed save before attempting preparation.

If enrichment is needed, carry the record ID and relevant gaps into the capture workflow. Do not require speculative improvements or invent technical detail as a prerequisite to the user's request.

## Record the preparation request

1. Establish explicit intent to have Lightbringer prepare this innovation for patent filing. A request to finish a description, explore sources or register findings is not that intent. Do not ask for the same decision again when the user has already expressed it clearly.
2. Explain that the action starts Lightbringer's patent-preparation workflow. Call `prepare_for_patent_filing` with the selected record identifier, using the connected tool schema.
3. Report the actual returned status and record link. State any requirements or next action supplied by the service. If the tool is unavailable or the request fails, explain that preparation has not been confirmed and offer the same record in the Lightbringer application or a continuation with the team.

## Completion and continuation

A recorded preparation request does not establish that a separate invention disclosure was created, a paid engagement was accepted or a patent was filed. Report those outcomes only if the service explicitly confirms them. Payment and acceptance steps require a human handoff.

For a subsequent review from the patent team, use `patent-review` when installed or the connected review guidance. General advice, strategy, novelty assessments and other professional-service requests are outside this workflow; use the service's available instructions and continuation routes.
