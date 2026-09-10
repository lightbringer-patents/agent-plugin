# Source exploration

An innovation can range from a vague idea to a detailed technical description. Explore problems in customer and operational sources and approaches in engineering sources; link them where evidence permits and retain open questions.

Autonomy: establish which sources to explore and whether the user wants findings registered. An analysis-only request does not authorise saving. Carry out requested registration and updates without asking for the same approval again. Ask when missing information prevents faithful capture or changes the scope. Patent preparation, paid engagements and formal review decisions are separate actions. Search for existing records before registering each concept; do not wait for the entire exploration to finish to save supported findings.

### Phase 0 — scope and sources

- Sort available connectors: problem-side (support, CRM, product analytics, feedback, incidents, bug reports) and solution-side (code hosts, project trackers, doc stores, engineering chat); some serve both.
- Broad request → propose a concrete scope (projects, repos, folders, time window) in the brief.
- One side missing → plan one-sided mining; note it in the brief and the summary.
- Read [source-specific guidance](source-mining.md) before harvesting.

### Phase 1 — strategy, brief, harvest

Locate the strategy, in order: the adopted strategy stored in Lightbringer; use `search` (`category: report`) for "Intellectual Property Strategy Report" and "Patent Drafting & Prosecution Strategy Report" — if both reports exist read both and state conflicts. An uploaded strategy or meeting notes may propose a newer direction; distinguish that from the adopted strategy. If none exists, state the working assumptions. Extract focus areas, priorities and jurisdictions; use them to annotate fit, not to exclude potential innovations.

Present a short brief: scope; sources (with any one-sided note); strategy lens or defaults; what follows (analysis, or requested registration/enrichment, with open questions and a closing summary). If source scope or permission to save is unclear, ask for clarification before that work. Otherwise continue using the authorisation already given.

Harvest:
- Problem sweep: recurring, evidenced pain; prefer converging themes over single anecdotes; capture what fails, for whom, conditions, frequency, apparent technical cause.
- Solution sweep: shipped projects, PRs, design docs, ADRs, remediations; capture mechanism, motivation, technical detail (parameters, embodiments, benchmarks).
- Pair via existing trace links (ticket → issue → PR, docs citing incidents); otherwise by theme and timeframe, marked inferred. Outcomes: **paired** (innovation description candidate); **unpaired problem** (summary's unresolved problems); **unpaired solution** (reconstruct the problem from the artifact, mark reconstructed for inventor confirmation).
- Coverage audit: every in-scope source ends with findings or an explicit "nothing found because X". A substantial project with zero yield gets a mandatory second look first.

### Phase 2 — context

- Per harvest theme, `search` categories `innovation`, `application`, `patent` (add `competitor_application`/`report` where relevant); track the theme×category matrix until every relevant cell is queried. `fetch` promising hits; assess overlap, continuations, conflicts.
- Check prior runs: `list_innovations` with relevant concept terms and their review outcomes via `list_reviews` (open and closed) + `get_review`. Reuse identical concepts and add new supported context through authorised updates, including to a previously rejected innovation when the tool permits. Preserve its decision history; never duplicate it to bypass a prior decision. If updates are unavailable, explain the limitation.
- The search index updates asynchronously — vary query terms before concluding absence.
- External patent research only to fill specific framing gaps; no novelty search.

### Phase 3 — distinct ideas

Read [idea identification](idea-identification.md). For each pair:
- Distinct = separate technical problem or materially different mechanism. Never create two innovation records in one run for the same inventive concept.
- Record: inventive concept, problem with evidence, differentiators vs Phase 2 findings, sources on both sides, strategy alignment, combine-vs-separate reasoning.
- Record eligibility or patentability uncertainty as a question for the Lightbringer patent team. Such uncertainty does not prevent registration. Frame the observed technical contribution without inventing one.
- Portfolio overlap: register distinct improvements as related innovations naming the related record; enrich identical concepts instead of duplicating them (summary note).
- Thin documentation: retain the potential innovation and its open questions. Use the current template honestly; if the deployed schema prevents saving it, report it as pending registration, give the missing inputs, and ask for the minimum clarification or offer the platform/team route. Never silently drop it or claim it was saved.
- No potential innovations → say so. Never manufacture innovative significance from a source label or a problem alone; retain vague ideas when the available context supports their innovative significance.

### Phase 4 — author, validate, create

Only when saving is authorised, read [authoring guidance](lightbringer-authoring.md). For analysis-only requests, proceed to the completion summary without registering or updating records. Per idea: `get_innovation_template` (once per session; author against what it returns), draft the strongest supported definition with resolved detail in the main fields, `validate_innovation` until clean, `register_innovation` with a descriptive title. Creation completes registration. For an existing concept, read it and use `update_innovation` instead.

### Phase 5 — refine

When innovation description refinement is part of the mandate, use `get_innovation_feedback` (focus `all`); it is automated innovation description analysis, not a novelty search. Otherwise stop after registration/enrichment. If analysis runs, if pending, poll `check_task_status` and author other innovation records meanwhile. Apply fixes supported by harvested context via `update_innovation` (whole-section overwrite — send complete replacement text). Information only the inventor has stays an honest gap. One pass; a second only after substantial rewrites.

### Completion — registration and enrichment

Return a chat summary with source coverage, strategy used, related records, and a compact list of identified innovations. For each, include evidence, registered/updated record link when saved, open questions, and actual outcome. Mark analysis-only findings as not registered. Clearly identify anything pending registration because of missing input or a tool limitation. Include genuine zero-yield sources and unresolved problems without inventing innovations.

A downloadable Markdown report is optional when the host supports files; a local filesystem is not required. Registration is complete without `prepare_for_patent_filing`. A user's later request to have Lightbringer patent a selected innovation follows `patent-preparation`, with explicit patenting intent.

