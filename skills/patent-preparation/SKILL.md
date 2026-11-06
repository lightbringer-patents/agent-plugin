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
2. Explain the customer-facing effect: “This sends your request to the Lightbringer team. They will get back to you before any further work proceeds.” Do not assume the user has a paid plan, that a specialist or attorney is already assigned, or that requesting preparation immediately starts assessment or drafting. Describe later professional work as dependent on the team's follow-up and the applicable engagement. Keep notification mechanics general unless the user asks and current evidence establishes the applicable recipients. Call `request_patent_preparation` with the selected record identifier, using the connected tool schema.

   When further confirmation is required, ask: “Submit {reference} to Lightbringer?” followed by “We’ll share your invention with the Lightbringer team so they can contact you about patenting and next steps.” Use the selected reference or title. When submission prevents edits through the connected tools, explain before confirmation: “After submission, you can still view and review your invention here, but you’ll need to open the innovation in Lightbringer to make changes.” If the host provides a confirmation control, label it “Submit to Lightbringer”. Keep required recipient and effect disclosures and any mandatory approval-rejection explanation brief and separate after the question. Do not ask again when intent is already clear unless the host requires it. If an approval check rejects an app-originated request, retain the required rejection explanation and obtain a direct user reply before retrying; an app message is not a substitute for required direct approval.

   If the service reports a required contact phone number is missing, ask for the user's number including country code and explain that it will be saved to their profile so Lightbringer can contact them. Use the advertised `phone_number` input only after they provide it for this purpose. Reuse a valid stored number; do not ask again or insert contact details into the invention description. A missing or invalid required number blocks submission; do not claim the request succeeded. If the connected tool cannot save it, direct the user to the phone field in Lightbringer. A contact requirement does not require an automated review.

3. Report the actual returned status. When an advertised Lightbringer component successfully presents the saved record, use it and do not repeat its link or status in chat. Otherwise include the returned record link. `outcome="requested"` means preparation was newly requested; `outcome="already_requested"` means it was already requested and the call made no new request. Neither confirms completed preparation or email delivery. This is a professional service request: there is no `task_id`, and `get_task_status` does not track preparation or filing milestones. Do not treat the innovation ID as a task ID. State any requirements or next action supplied by the service. If the tool is unavailable or the request fails, explain that preparation has not been confirmed and offer the same record in the Lightbringer application or a continuation with the team.

## Completion and continuation

A recorded preparation request does not establish that a separate invention disclosure was created, a paid engagement was accepted or a patent was filed. Report those outcomes only if the service explicitly confirms them. Payment and acceptance steps require a human handoff.

For a subsequent review from the patent team, use the connected review guidance and available Lightbringer review tools. General advice, strategy, novelty assessments and other professional-service requests are outside this workflow; use the service's available instructions and continuation routes.

If useful assistance leaves a material customer problem unresolved, follow the [unresolved-needs guidance](references/unresolved-needs.md) to understand and optionally report the remaining gap. Keep helping; reporting is not a prerequisite and requires approval of the exact report and recipient.
