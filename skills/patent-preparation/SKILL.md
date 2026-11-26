---
name: patent-preparation
description: Prepare an invention disclosure from a saved innovation when supported, continue that preparation, or record an explicit request for Lightbringer's patent service. Use for preparing an innovation for patenting, refining its preparation draft or submitting a selected disclosure. Drafting and service submission are separate outcomes; registration, general advice and review responses use their own workflows.
---

# Patent preparation

Establish whether the user wants a draft to review or wants to submit a disclosure to the Lightbringer team. Reuse an already clear decision. A request to prepare a saved innovation as a draft does not authorise service submission. Read [service conduct](references/service-conduct.md).

## Draft from a selected innovation

When `start_journey` advertises `invention-capture` and `answer_agent` and
`get_task_status` are available, prefer that shared guided-capture procedure for
requested preparation. Pass the selected source references, existing disclosure
when known, supported evidence and established answers using only advertised
inputs. Follow `journeys` when installed, and continue the same task for corrections.
Do not create a separate disclosure or conduct a competing interview while it runs.
Direct targeted edits still use the shared asset tools. The steps below are the
direct-authoring compatibility path when the journey is unavailable; they do not
establish that platform-agent capture occurred.

1. Find the selected innovation and fetch its saved text, relationships and attachment inventory. Read the supporting files needed to understand the invention. If there is already a linked disclosure for this work, open it and continue from its saved sections. Ask which draft the user means if the relationship is ambiguous.
2. Retrieve `get_innovation_template`. Author the complete definition in the current conversation using the source's technical account and relevant file contents. Follow the template's field guidance. Preserve measurements, qualifications, and the distinction between tested results and open questions. Reuse inventor and public-disclosure facts already given. Contributor names alone do not confirm inventorship. If the user supplies or corrects a public-disclosure fact during preparation, retain it on the linked innovation using the current revision. An explicit statement of no disclosure or sale belongs in its saved text even when there is no date. Ask only for a material missing fact that the template requires or to resolve conflicting evidence. If an honest definition cannot yet be registered, keep the work in the conversation until it can.
3. Register once with the `create_asset` `invention_disclosure` variant, sending the completed definition and the selected source references together: `type: invention_disclosure` and `asset.data` containing `definition` and `sourceInnovations`. Supply the canonical references returned for the selected innovations. This saves the authored sections, links the sources and carries over supporting files and drawings. It leaves the patent decision on each source as recorded. Source references alone create an unfilled draft. If that variant is not advertised or does not accept source references, explain the limitation and provide the source link for continuation in Lightbringer.
4. Fetch the saved disclosure with the advertised asset, attachment and inventor read options. Verify its authored sections, source links, inventor names and expected files and drawings. Report the draft link, any registration warnings and genuine open questions. If the result was uncertain or the source is already incorporated, inspect its related disclosures before any further write. Continue later edits on the same draft using its current revision. If the user explicitly wants to continue an existing Lightbringer drafting conversation, resume that conversation using its task ID when available.

Draft registration does not request professional services. Use the following path only on an explicit submission request.

## Identify the disclosure for a service request

Use the connected organisation and resolve the selected record with `search` in its `innovation` category; read it with `fetch` and `include_asset: true`. If that category or read is not advertised, explain the limitation and offer the Lightbringer link. Once a disclosure is submitted for drafting, `search` lists it under `application`, not `innovation`; for a repeated request, reuse the ID already resolved or `fetch` it directly instead of searching again. Clarify an ambiguous selection. If the innovation is not registered, use `innovation-capture` when installed, retaining the user's patenting intent for that concept. If capture guidance is unavailable, follow `get_innovation_template` and save supported content with the `create_asset` `invention_disclosure` variant as part of the requested preparation. Registration validates before saving: report any missing inputs or validation errors before attempting preparation. Successful registration can include non-blocking warnings; report them without re-registering the record.

Refinement is optional. Offer it only when the user asks for it or the service reports a blocking requirement. Do not require automated feedback, a completeness interview or revisions before recording an explicit preparation request. For requested refinement or a service-reported blocker, carry the record ID and relevant gaps into the capture workflow, preserving the user's preparation intent. Do not invent technical detail or register a duplicate.

## Record the preparation request

1. Establish explicit intent to have Lightbringer prepare this innovation for patent filing. A request to finish a description, explore sources or register findings is not that intent. Do not ask for the same decision again when the user has already expressed it clearly.
2. Explain the customer-facing effect: “This sends your request to the Lightbringer team. They will get back to you before any further work proceeds.” Do not assume the user has a paid plan, that a specialist or attorney is already assigned, or that requesting preparation immediately starts assessment or drafting. Describe later professional work as dependent on the team's follow-up and the applicable engagement. Keep notification mechanics general unless the user asks and current evidence establishes the applicable recipients. Call `request_patent_preparation` with the selected record identifier, using the connected tool schema. Pass the record ID without the `document:` prefix that `search` and `fetch` show; every version of the tool accepts that form.

   Before calling the submission tool, explain: “After submission, you can still view and review your invention here, but you’ll need to open the innovation in Lightbringer to make changes.” Include this consequence even when the user has already clearly approved submission; explaining it does not require asking for the same approval again. If it was already explained for this submission, do not repeat it.

   When further confirmation is required, ask: “Submit {reference} to Lightbringer?” followed by “We’ll share your invention with the Lightbringer team so they can contact you about patenting and next steps.” Use the selected reference or title and include the editing consequence before the user confirms. If the host provides a confirmation control, label it “Submit to Lightbringer”. Keep required recipient and effect disclosures and any mandatory approval-rejection explanation brief and separate after the question. Do not ask again when intent is already clear unless the host requires it. If an approval check rejects an app-originated request, retain the required rejection explanation and obtain a direct user reply before retrying; an app message is not a substitute for required direct approval.

   If the service reports a required contact phone number is missing, ask for the user's number including country code and explain that it will be saved to their profile so Lightbringer can contact them. Use the advertised `phone_number` input only after they provide it for this purpose. Reuse a valid stored number; do not ask again or insert contact details into the invention description. A missing or invalid required number blocks submission; do not claim the request succeeded. If the connected tool cannot save it, direct the user to the phone field in Lightbringer. A contact requirement does not require an automated review.

3. Report the actual returned status. When an advertised Lightbringer component successfully presents the saved record, use it and do not repeat its link or status in chat. Otherwise include the returned record link. `outcome="requested"` means preparation was newly requested; `outcome="already_requested"` means it was already requested and the call made no new request. Neither confirms completed preparation or email delivery. This is a professional service request: there is no `task_id`, and `get_task_status` does not track preparation or filing milestones. Do not treat the innovation ID as a task ID. State any requirements or next action supplied by the service. If the tool is unavailable or the request fails, explain that preparation has not been confirmed and offer the same record in the Lightbringer application or a continuation with the team.

## Completion and continuation

A recorded preparation request does not establish that a separate invention disclosure was created, a paid engagement was accepted or a patent was filed. Report those outcomes only if the service explicitly confirms them. Payment and acceptance steps require a human handoff.

For a subsequent review from the patent team, use `patent-review` when installed, otherwise the connected review guidance and available Lightbringer review tools. General advice, strategy, novelty assessments and other professional-service requests are outside this workflow; use the service's available instructions and continuation routes.

If useful assistance leaves a material customer problem unresolved, follow the [unresolved-needs guidance](references/unresolved-needs.md) to understand and optionally report the remaining gap. Keep helping; reporting is not a prerequisite and requires approval of the exact report and recipient.
