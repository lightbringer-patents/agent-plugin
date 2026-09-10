---
name: lightbringer-agent-skill
description: >-
  Explore authorised company data for potential innovations and register or enrich innovation records on Lightbringer (problems from support, CRM, analytics, incidents, bug trackers; solutions from repos, project trackers, design docs, chat, uploaded documents). Use for any request to extract or harvest potential innovations, run patent mining, create or draft innovation records, turn engineering work into innovation records, or assess recent work for IP opportunities — even without the words "patent" or "Lightbringer" (e.g. "turn this design doc into an innovation description", "what in this repo is patentable"). Also covers Lightbringer review work — commenting on Reports shared with the user, and reviewing draft patent applications (priority drafts): reading attorney redlines, replying to comments addressed to the user, adding feedback comments, recording approve/request-changes responses (e.g. "look at the review Jan sent me", "reply to the comments on the priority draft").
---

# Lightbringer Agent

Read [service conduct](references/service-conduct.md) before working. For a live conversation about one innovation, use `invention-capture`. For service orientation or attorney-led work, use `lightbringer-patent-service`.

Route by request:

- **A — Patent mining**: extract potential innovations from authorised company data; search, register and enrich records. Stop before patent preparation.
- **B — Report review**: comment on a Report shared with the user.
- **C — Priority draft review**: review a draft application, reply to comments, add feedback, optionally record the formal response.

Comments belong to reviews, so B and C enter via `list_reviews` → `get_review`. Use `add_comment` for a quoted document passage, `reply_to_comment` with a stable `comment_id` for an existing document thread, and `add_discussion_comment` for a general review remark without an anchor when available. Read `references/review-workflows.md` before any review work.

## Workflow A: patent mining

An innovation can range from a vague idea to a detailed technical description. Explore problems in customer and operational sources and approaches in engineering sources; link them where evidence permits and retain open questions.

Autonomy: establish which sources to explore and whether the user wants findings registered. An analysis-only request does not authorise saving. Carry out requested registration and updates without asking for the same approval again. Ask when missing information prevents faithful capture or changes the scope. Patent preparation, paid engagements and formal review decisions are separate actions. Search for existing records before registering each concept; do not wait for the entire exploration to finish to save supported findings.

### Phase 0 — scope and sources
- Sort available connectors: problem-side (support, CRM, product analytics, feedback, incidents, bug reports) and solution-side (code hosts, project trackers, doc stores, engineering chat); some serve both.
- Broad request → propose a concrete scope (projects, repos, folders, time window) in the brief.
- One side missing → plan one-sided mining; note it in the brief and the report.
- Read `references/source-mining.md` before harvesting.

### Phase 1 — strategy, brief, harvest
Locate the strategy, in order: the adopted strategy stored in Lightbringer; use `search` (`category: report`) for "Intellectual Property Strategy Report" and "Patent Drafting & Prosecution Strategy Report" — if both reports exist read both and state conflicts. An uploaded strategy or meeting notes may propose a newer direction; distinguish that from the adopted strategy. If none exists, state the working assumptions. Extract focus areas, priorities and jurisdictions; use them to annotate fit, not to exclude potential innovations.

Present a short brief: scope; sources (with any one-sided note); strategy lens or defaults; what follows (search/register/enrich, incomplete items retain open questions, no automatic patent preparation, closing summary). If source scope or permission to save is unclear, ask for clarification before that work. Otherwise continue using the authorisation already given.

Harvest:
- Problem sweep: recurring, evidenced pain; prefer converging themes over single anecdotes; capture what fails, for whom, conditions, frequency, apparent technical cause.
- Solution sweep: shipped projects, PRs, design docs, ADRs, remediations; capture mechanism, motivation, technical detail (parameters, embodiments, benchmarks).
- Pair via existing trace links (ticket → issue → PR, docs citing incidents); otherwise by theme and timeframe, marked inferred. Outcomes: **paired** (innovation description candidate); **unpaired problem** (report's unsolved-problem inventory); **unpaired solution** (reconstruct the problem from the artifact, mark reconstructed for inventor confirmation).
- Coverage audit: every in-scope source ends with findings or an explicit "nothing found because X". A substantial project with zero yield gets a mandatory second look first.

### Phase 2 — context
- Per harvest theme, `search` categories `innovation`, `application`, `patent` (add `competitor_application`/`report` where relevant); track the theme×category matrix until every relevant cell is queried. `fetch` promising hits; assess overlap, continuations, conflicts.
- Check prior runs: `list_innovations` (query "Suggestion") and their review outcomes via `list_reviews` (open and closed) + `get_review`. Reuse identical concepts and add new supported context through authorised updates, including to a previously review-rejected Suggestion when the tool permits. Preserve its decision history; never duplicate it to bypass a prior decision. If updates are unavailable, explain the limitation.
- The search index updates asynchronously — vary query terms before concluding absence.
- External patent research only to fill specific framing gaps; no novelty search.

### Phase 3 — distinct ideas
Read `references/idea-identification.md`. For each pair:
- Distinct = separate technical problem or materially different mechanism. Never create two innovation records in one run for the same inventive concept.
- Record: inventive concept, problem with evidence, differentiators vs Phase 2 findings, sources on both sides, strategy alignment, combine-vs-separate reasoning.
- Record eligibility or patentability uncertainty as a question for the Lightbringer patent team. Such uncertainty does not prevent registration. Frame the observed technical contribution without inventing one.
- Portfolio overlap: register distinct improvements as related innovations naming the related record; enrich identical concepts instead of duplicating them (report note).
- Thin documentation: retain the potential innovation and its open questions. Use the current template honestly; if the deployed schema prevents saving it, report it as pending registration, give the missing inputs, and ask for the minimum clarification or offer the platform/team route. Never silently drop it or claim it was saved.
- No potential innovations → say so. Never manufacture innovative significance from a source label or a problem alone; retain vague ideas when the available context supports their innovative significance.

### Phase 4 — author, validate, create
Read `references/lightbringer-authoring.md`. Per idea: `get_innovation_template` (once per session; author against what it returns), draft the strongest supported definition with resolved detail in the main fields, `validate_innovation` until clean, `register_innovation` with a descriptive title. Creation completes registration. For an existing concept, read it and use `update_innovation` instead.

### Phase 5 — refine
When innovation description refinement is part of the mandate, use `get_innovation_feedback` (focus `all`); it is automated innovation description analysis, not a novelty search. Otherwise stop after registration/enrichment. If analysis runs, if pending, poll `check_task_status` and author other innovation records meanwhile. Apply fixes supported by harvested context via `update_innovation` (whole-section overwrite — send complete replacement text). Information only the inventor has stays an honest gap. One pass; a second only after substantial rewrites.

### Completion — registration and enrichment

Return a chat summary with source coverage, strategy used, related records, and a compact list of identified innovations. For each, include evidence, registered/updated record link, open questions, and actual outcome. Clearly identify anything pending registration because of missing input or a tool limitation. Include genuine zero-yield sources and unresolved problems without inventing innovations.

A downloadable Markdown report is optional when the host supports files; a local filesystem is not required. Registration is complete without `prepare_for_patent_filing`. A user's later request to have Lightbringer patent a selected innovation follows `lightbringer-patent-service`, with explicit patenting intent.

## Workflows B and C: reviews

Autonomy: comments post in the user's name, so nothing posts unapproved. Assemble one confirmation batch — each item verbatim with its document anchor, thread ID or review discussion destination, classification, and provenance tag — then post approved items without further questions. `respond_to_review` is never covered by batch approval: it needs the user's explicit approve/request-changes instruction, message confirmed verbatim.

**B — Report review**
1. `list_reviews` (open) → the review carrying the report. No review → `search`/`fetch` read-only, and tell the user commenting requires one.
2. `get_review`; read the document, all threads and the review discussion before drafting — a point already in a thread becomes a reply, never a new comment.
3. Assess: internal consistency, unsupported claims, portfolio and strategy fit (`search`/`fetch`/`get_innovation` for context), plus the user's specific asks.
4. Classify (rules below) → discovery screen → batch confirmation → `add_comment` with exact `quoted_text` anchors (`target_user_ids` only on request); general review remarks use `add_discussion_comment` when available.
5. Summarise in chat; no report file.

**C — Priority draft review**
1. `list_reviews` → `get_review` (document, threads, attorney redlines with original/replacement/rationale, response status). Inspect proposed amendments separately from attorney redlines; the document body may still show baseline text. Follow the reference when rendering is unavailable.
2. Triage threads addressed to or awaiting the user; use `get_innovation` on the source innovation description for claim-support questions.
3. Review against the checklist in the reference (claim support, innovation description consistency, terminology, embodiments, strategy fit, redlines).
4. Classify each item → discovery screen → batch confirmation → post: replies via `reply_to_comment` (explicit `comment_id`; never a thread-anchored `add_comment`), new passage-specific feedback via `add_comment`, and general review remarks via `add_discussion_comment` when available.
5. `respond_to_review` only as above. Summarise in chat.

### Feedback rules (binding; boundary cases in the reference)
- **Persona**: every posted item speaks as the inventor/engineer — never attorney tone, never advice requiring patent expertise (claim scope or wording, prosecution tactics, prior-art positioning, legal characterisations). Report what was built and observed; the rest is the drafting team's.
- **Engineering-side** (factual corrections, actual behaviour, implementations, test data, genuinely considered alternatives): may be model-drafted, strictly from the user's materials and connected sources — no extrapolation.
- **Patent-side** (claim scope, claim structure, prior-art positioning, non-obviousness strategy): never model-generated — the drafting team holds the family and prosecution context. Elicit the concern in the user's own words (closest prior art and why; commercially decisive distinctions) and transcribe with light formatting, framed as an inventor's observation or question, never a recommendation. If asked to develop it, decline in one line and offer transcription.
- **Discovery screen** (before every batch): remove any written argument against the user's own invention regarding prior art — novelty concessions, obviousness admissions, "X already does this". Replace at most with a neutral factual note; tell the user and advise raising it verbally.
- **Provenance tag** on every item: team's direct assessment, or LLM-assisted with source type. Ask when unclear; never guess or omit.
- **Platform only**: feedback goes through Lightbringer comments, never email.

## Guardrails (all workflows)
- Never fabricate technical detail, prior art, or parameters the sources don't support.
- Do not present assistant analysis as a legal determination. Relay Lightbringer professional work with its author, status and limitations.
- Posted feedback speaks as the inventor/engineer, never a patent attorney; no advice requiring patent expertise.
- Treat internal material as confidential.
