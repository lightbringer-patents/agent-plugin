---
name: novelty-exploration
description: Explore whether a technical idea has appeared in patents. Use when someone asks whether their solution is new, whether someone has already patented it, or wants related competitor patents. Clarify the problem and technical mechanism, search public publications, and import relevant findings into Lightbringer when authorised. No existing patent portfolio is required; this is preliminary exploration, not a legal novelty or freedom-to-operate assessment.
---

# Novelty exploration

Help the user get to the core of a technical solution, find related patent publications and retain useful evidence in Lightbringer. The result is a clearer technical explanation, an evidence-backed shortlist and focused questions for further investigation. Work from the conversation or authorised source material; an existing innovation record, patent portfolio or completed disclosure is not a prerequisite.

## Offer innovation capture first

Encourage the user to describe and register the invention in Lightbringer before a deeper exploration. Explain that the guided capture workflow helps articulate the technical solution and keeps a reusable description in their workspace. Present this as an option: “We can first capture your invention in Lightbringer to give the search a clear technical starting point, or do a small exploration here from what you have already described.”

If the user chooses capture, use the bundled [innovation-capture skill](../innovation-capture/SKILL.md) and its current platform guidance, then resume exploration from the supported description. Reuse an existing innovation when available; do not register a duplicate. Honour an existing registration instruction without asking again. If the user prefers a quick exploration, continue with the lightweight questions below without requiring registration, a capture template or a complete disclosure. Describing an idea in conversation does not itself authorise saving it, and registration does not request patent preparation.

## Understand the problem and mechanism

Reuse what the user has already explained. Ask a few focused questions at a time, guided by the gaps that would change the search:

- What technical problem arises, under what conditions, and why do existing approaches fall short?
- How does the proposed solution work: which components, inputs, processing steps and interactions produce the result?
- Which part does the user think differs from conventional approaches? Is the difference in a component, a sequence, a relationship or a combination?
- What technical effect follows from that difference, and what observations or measurements support it?

Turn a broad goal such as improving efficiency or using AI into a concrete causal explanation: **problem → mechanism → technical effect**. Separate essential features from optional implementations and distinguish the user's facts from hypotheses or missing details. Reflect the explanation back in concise language so the user can correct it. Do not invent an implementation to make the idea sound distinctive or require a full registration interview before searching.

When “already patented” is ambiguous, distinguish exploring earlier technical disclosures from asking whether the user can sell a product. If the concern is commercial use, retain the relevant product and market questions for professional follow-up; preliminary technical comparisons do not answer freedom to operate. Continue useful exploration within that scope.

## Search related and competitor patents

Translate the mechanism into simple search terms: components, operations, technical effects and alternative terminology. Start with the most informative feature combinations, inspect the results, then narrow or broaden based on what they reveal. Search individual features as well as their interaction; a matching product category alone is weak evidence of the same solution.

Use the connected `search_public_patents` tool for public publications. Use simple keywords in `query`, supported company names in `assignee`, or a complete `publicationNumber` on its own. Follow the advertised schema; do not invent Boolean, quoted-phrase or provider-specific syntax. Follow `nextPage` within the agreed search scope and retain truncation, unvisited pages and provider failures as coverage limits.

Search named competitors and relevant applicants found in the results, using supported filing-name variants. Do not restrict the search to known competitors: useful technical disclosures can come from other industries, universities or unfamiliar applicants. Keep uncertain company matches explicit; publication metadata does not verify current ownership.

Use generic technical terms in external queries. Do not send confidential documents or undisclosed implementation details to external search services without authorisation covering that disclosure. Where that would be needed, agree a narrower query or obtain the missing authorisation.

Keep a compact record of queries, names searched and promising complete publication numbers. Stop when there is a useful shortlist and further similar searches add little, or when the agreed scope is reached. A zero-result query is a reason to revisit terminology, not evidence that the idea is novel. State that patent searches alone leave non-patent literature and other unsearched sources uncovered.

## Compare the technical substance

For each promising publication, explain which feature or interaction makes it relevant. Distinguish title/abstract matches from comparisons supported by actual passages in the description or claims. Read accessible patent text before making detailed comparisons; if only a summary is available, label the finding preliminary. Use available read tools or source access; do not silently import records merely to obtain text.

Present a small comparison when useful: publication and source link, matching mechanism, apparent differences, evidence location and open questions. Avoid counting related publications as independent technical approaches when their relationship is established; do not infer a family solely from similar titles.

Keep each publication's evidence separate. Features scattered across different documents do not establish that one document discloses the whole proposed solution. Similarity, a publication date, a grant or a provider status flag alone does not establish novelty, patentability, infringement or permission to operate. Use wording such as “related disclosure”, “apparent difference” and “not found in the material searched”, tied to the actual evidence.

## Import relevant findings

Offer to save the selected publications as competitor references, explaining their relevance. A search-only request does not authorise imports. Honour an existing instruction to search and import relevant findings within its agreed scope without asking again; otherwise obtain authorisation for the proposed selection.

Import competitor references directly with the connected tools:

1. Establish the destination organisation from available connection context or `whoami` when needed. Resolve each selected publication to its complete number, including country and kind code, using `search_public_patents` if necessary.
2. Call `import_patent` with that `publicationNumber` and `purpose: competitor`. Include `competitorCompanyName` only when supported by the evidence and accepted by the advertised schema. Use sequential calls or small batches within rate limits, keeping each result so interrupted work can resume.
3. Retain the returned `documentId`, `url`, status, receipt and warnings. `imported` confirms a save; `already_imported` returns an existing record without refreshing its content. Receipt `complete` means processing completed; `partial` means saved with limitations; `incomplete` means saved but processing did not finish, not necessarily that work is still running. A null receipt means completion details are unavailable.
4. Use `fetch` with the returned record identity for readback; saved-document search can lag behind an import. Refine the technical comparison from the available text, retaining warnings about missing text, PDFs or images. If readback fails, preserve the confirmed save and mark verification and any unsupported comparison incomplete.

For an application or purpose conflict, inspect the existing record identified by the error when available. Report whether it meets the user's goal without claiming the requested import succeeded. The import tool cannot replace a publication or change its existing purpose; do not alter identifiers or purpose to bypass a conflict. Leave unresolved items explicit and continue the rest of the authorised selection.

A timeout can occur after a save. Retry the same publication and purpose a bounded number of times, respecting any advised delay, to retrieve the outcome. Stop on persistent failures or errors requiring changed input or access. Repeating an import does not repair missing content or assets. Do not call `refresh_patent_family` for competitor references; that operation applies to saved own patents.

Use only tools available in the connection. If import access is unavailable, retain a linked shortlist in chat and explain what remains unsaved. Importing a patent does not register the user's invention, request patent preparation, order professional work or verify legal status.

## Finish with the next useful step

Summarise the technical core, closest findings, supported similarities and differences, search coverage and unresolved questions. Include the confirmed imported record links and actionable warnings, separately from unsaved candidates. Do not declare an idea new because the search did not find its exact wording.

If the exploration clarified an invention the user wants to retain, offer to capture or enrich it through `innovation-capture`, preserving an earlier choice to keep the work in chat. Exploration alone does not authorise that save.

When a full novelty search or freedom-to-operate assessment is needed, explain that Lightbringer offers these services and that arranging them requires contacting Lightbringer sales. Offer to prepare a concise brief with the technical solution, relevant publications, open questions and, for FTO, the intended products and markets. Direct the user to Lightbringer sales to agree the scope and engagement; do not represent patent imports, innovation registration or `request_patent_preparation` as ordering these services. A brief is not a completed assessment, sales contact or confirmed service request. Automated innovation-description feedback is not a substitute for either service.
