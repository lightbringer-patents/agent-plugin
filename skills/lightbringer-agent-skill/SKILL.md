---
name: lightbringer-agent-skill
description: >-
  Mine company data for patentable problem-solution pairs and create invention disclosures on Lightbringer (problems from support, CRM, analytics, incidents, bug trackers; solutions from repos, project trackers, design docs, chat, uploaded documents). Use for any request to extract or harvest patentable ideas, run patent mining, create or draft invention disclosures, turn engineering work into disclosures, or assess recent work for IP opportunities — even without the words "patent" or "Lightbringer" (e.g. "turn this design doc into a disclosure", "what in this repo is patentable"). Also covers Lightbringer review work — commenting on Reports shared with the user, and reviewing draft patent applications (priority drafts): reading attorney redlines, replying to comments addressed to the user, adding feedback comments, recording approve/request-changes responses (e.g. "look at the review Jan sent me", "reply to the comments on the priority draft").
---

# Lightbringer Agent

Route by request:

- **A — Patent mining**: extract patentable ideas from company data; author, validate, create, refine, submit disclosures.
- **B — Report review**: comment on a Report shared with the user.
- **C — Priority draft review**: review a draft application, reply to comments, add feedback, optionally record the formal response.

Comments exist only inside reviews (`add_comment`/`reply_to_comment` take a `review_id` and a quoted anchor), so B and C enter via `list_reviews` → `get_review`. Read `references/review-workflows.md` before any review work.

## Workflow A: patent mining

An invention is a problem-solution pair: problems live in customer and operational sources, solutions in engineering sources. Sweep both, then pair.

Autonomy: one checkpoint — the Phase 1 mining brief. After confirmation, run every phase without questions; judgment calls are recorded in the disclosures and final report, never raised in chat. Pause mid-run only if the material is too ambiguous to determine even the technical domain. Create nothing before Phases 1–3 are complete.

### Phase 0 — scope and sources
- Sort available connectors: problem-side (support, CRM, product analytics, feedback, incidents, bug reports) and solution-side (code hosts, project trackers, doc stores, engineering chat); some serve both.
- Broad request → propose a concrete scope (projects, repos, folders, time window) in the brief.
- One side missing → plan one-sided mining; note it in the brief and the report.
- Read `references/source-mining.md` before harvesting.

### Phase 1 — strategy, brief, harvest
Locate the strategy, in order: a document from this session; else `search` (`category: report`) for "Intellectual Property Strategy Report" and "Patent Drafting & Prosecution Strategy Report" — if both reports exist read both and state the reading used where they conflict; else use default assumptions (favour detectable infringement and clear technical character). Extract focus areas, priorities, exclusions, jurisdictions.

Present a brief (under 15 lines) and wait for confirmation: scope; sources (with any one-sided note); strategy lens or defaults; what follows (automatic create/refine/submit, flagged items proceed with in-record flags, closing report). One question: proceed or adjust. Skip the brief only when the user pre-authorised an autonomous run; then state it as assumptions and continue.

Harvest:
- Problem sweep: recurring, evidenced pain; prefer converging themes over single anecdotes; capture what fails, for whom, conditions, frequency, apparent technical cause.
- Solution sweep: shipped projects, PRs, design docs, ADRs, remediations; capture mechanism, motivation, disclosure-grade detail (parameters, embodiments, benchmarks).
- Pair via existing trace links (ticket → issue → PR, docs citing incidents); otherwise by theme and timeframe, marked inferred. Outcomes: **paired** (disclosure candidate); **unpaired problem** (report's unsolved-problem inventory); **unpaired solution** (reconstruct the problem from the artifact, mark reconstructed for inventor confirmation).
- Coverage audit: every in-scope source ends with findings or an explicit "nothing found because X". A substantial project with zero yield gets a mandatory second look first.

### Phase 2 — context
- Per harvest theme, `search` categories `innovation`, `application`, `patent` (add `competitor_application`/`report` where relevant); track the theme×category matrix until every relevant cell is queried. `fetch` promising hits; assess overlap, continuations, conflicts.
- Check prior runs: `list_inventions` (query "Suggestion") and their review outcomes via `list_reviews` (open and closed) + `get_review`. Never re-create an idea identical to an existing record or a review-rejected Suggestion.
- The search index updates asynchronously — vary query terms before concluding absence.
- External patent research only to fill specific framing gaps; no novelty search.

### Phase 3 — distinct ideas
Read `references/idea-identification.md`. For each pair:
- Distinct = separate technical problem or materially different mechanism. Never create two disclosures in one run for the same inventive concept.
- Record: inventive concept, problem with evidence, differentiators vs Phase 2 findings, sources on both sides, strategy alignment, combine-vs-separate reasoning.
- Run the eligibility screen; borderline ideas proceed with a reviewCompletion clarity issue of type "eligibility". Frame mixed ideas around the technical contribution.
- Portfolio overlap: create extensions as flagged improvement/continuation disclosures naming the related record; skip only identical concepts (report note).
- Thin documentation: proceed if the schema minimums can be met honestly, turning gaps into pointed clarity issues; drop only when meeting them would require fabrication.
- No qualifying pairs → say so. Never manufacture disclosures from routine engineering, configuration, known patterns, pure business logic, or a problem alone.

### Phase 4 — author, validate, create
Read `references/lightbringer-authoring.md`. Per idea: `get_invention_template` (once per session; author against what it returns), draft the strongest supported definition with resolved detail in the main fields, `validate_invention` until clean, `create_invention` titled `Suggestion N - <title>`.

### Phase 5 — refine
`get_invention_feedback` (focus `all`); if pending, poll `check_task_status` and author other disclosures meanwhile. Apply fixes supported by harvested context via `update_invention` (whole-section overwrite — send complete replacement text). Information only the inventor has stays an honest gap. One pass; a second only after substantial rewrites.

### Phase 6 — submit
`submit_invention` every successfully created disclosure without pausing; never submit one that failed validation or creation — report it instead. Responding to the ensuing review is Workflow C, in a later session.

### Final report
Always write a standalone `.md` with exactly:

```
# Patent Mining Report
## Material Overview
## Organisational and Patent Context
## Identified Patentable Ideas
## Disclosures Created and Submitted
```

- Material Overview: what each source contributed; strategy objectives; the full coverage account with justifications and second-look outcomes.
- Context: related records, overlap/continuation opportunities, conflicts, prior-Suggestion review outcomes, external research done and why.
- Ideas: per idea — title, concept summary, problem with evidence, mechanism, differentiators, source refs on both sides, traced or inferred pairing, strategy alignment, eligibility outcome, combine/separate reasoning; include rejected ideas marked with reasons; end with the unsolved-problem inventory.
- Disclosures: per disclosure — title, link, concept recap, open issues and flags, submission status; explain any failure and the next step.

The report is standalone (never reference the chat or your process) and must account for every creation and submission.

## Workflows B and C: reviews

Autonomy: comments post in the user's name, so nothing posts unapproved. Assemble one confirmation batch — each item verbatim with its anchor or thread, classification, and provenance tag — then post approved items without further questions. `respond_to_review` is never covered by batch approval: it needs the user's explicit approve/request-changes instruction, message confirmed verbatim.

**B — Report review**
1. `list_reviews` (open) → the review carrying the report. No review → `search`/`fetch` read-only, and tell the user commenting requires one.
2. `get_review`; read the document and all threads before drafting — a point already in a thread becomes a reply, never a new comment.
3. Assess: internal consistency, unsupported claims, portfolio and strategy fit (`search`/`fetch`/`get_invention` for context), plus the user's specific asks.
4. Classify (rules below) → discovery screen → batch confirmation → `add_comment` with exact `quoted_text` anchors (`target_user_ids` only on request).
5. Summarise in chat; no report file.

**C — Priority draft review**
1. `list_reviews` → `get_review` (document, threads, attorney redlines with original/replacement/rationale, response status).
2. Triage threads addressed to or awaiting the user; use `get_invention` on the source disclosure for claim-support questions.
3. Review against the checklist in the reference (claim support, disclosure consistency, terminology, embodiments, strategy fit, redlines).
4. Classify each item → discovery screen → batch confirmation → post: replies via `reply_to_comment` (explicit `comment_id`; never a thread-anchored `add_comment`), new feedback via `add_comment`.
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
- Never present any opinion on patentability.
- Posted feedback speaks as the inventor/engineer, never a patent attorney; no advice requiring patent expertise.
- Treat internal material as confidential.
