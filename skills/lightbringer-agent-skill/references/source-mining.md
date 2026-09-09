# Source mining reference

An invention is a problem-solution pair, and the two halves live in different systems. Problems surface in customer-facing and operational data; solutions live in engineering artifacts. This reference covers where to find each half, what the signal looks like, and how to pair them. The skill is source-agnostic: inventory the connectors available in the session, sort them into problem-side and solution-side, and apply the matching sections. When one side has no connector, tell the user rather than silently mining one-sided.

## General principles

For every finding, record a source reference precise enough to relocate it (ticket ID, issue ID, PR number, document title and section, thread permalink, dashboard query). Traceability is required in the final report, feeds the pairing step, and lets inventors verify claims later.

Ignore as non-inventive on the solution side: routine CRUD and glue code, configuration, dependency upgrades, well-known design patterns applied conventionally, pure business rules, UI styling, and anything whose novelty is organisational rather than technical. The test: does the contribution change how a technical system works, or only what it is used for? Only the former can anchor a disclosure. Treat this as exploration guidance, not a patentability determination. Carry uncertain potential innovations forward with the supporting evidence and open questions; avoid silent rejection based on strategy fit or disclosure completeness.

## Problem-side sources

The goal of the problem sweep is evidenced, recurring, technical pain. Convergence is the quality bar: the same friction appearing independently in several channels is a real problem; a single anecdote is not. Quantify where the source allows (ticket volume, affected accounts, error rates, drop-off percentages), because that evidence later strengthens the disclosure's problem description and demonstrates commercial relevance.

**Support and helpdesk platforms (Zendesk, Intercom, and similar).** The most honest problem signal available: customers report what they care enough to interrupt their day over, in their own words. Cluster tickets into themes rather than reading individually; look for repeated failure modes, workarounds customers invent, and complaints that persist across releases. Beware vocabulary spread: the same pain appears as "slow", "takes forever", "spinning", "timed out". Note ticket volumes and trends per theme.

**CRM and sales data (HubSpot, Salesforce, and similar).** Lost-deal reasons, competitor displacement notes, and recurring objections reveal capability gaps and performance problems that prospects consider disqualifying. Feature-gap objections that engineering later closed are prime pairing candidates. Call transcripts and deal notes carry the customer's framing of the problem, useful verbatim context for the problem description.

**Product analytics (Mixpanel, Amplitude, and similar).** Funnel drop-offs, abandoned flows, latency-correlated churn, and error-event spikes reveal problems customers never report. Analytics rarely states the technical cause, so treat it as corroborating evidence attached to themes found elsewhere, or as a pointer for where to look in engineering sources.

**Issue trackers, bug side (Linear, Jira).** Bug reports, incident follow-ups, and performance complaints filed internally. These are often the first formalisation of a customer-reported problem and usually carry the trace links onward to the solution (assignee, project, linked PR), which makes them the best bridge between the two sweeps.

**Incident and support channels in chat (Slack).** Incident channels capture problems at their rawest, including the technical cause discovered in real time. Post-incident threads often state the constraint that made the obvious fix impossible, which is exactly the setup for an inventive mechanism.

**Surveys, NPS verbatims, reviews.** Secondary corroboration for themes found elsewhere. Useful for frequency and severity evidence; rarely sufficient alone.

## Solution-side sources

The goal of the solution sweep is causally understood mechanisms. The strongest targets are documents where engineers explain why, not just what: friction points, performance walls, "we tried X, it failed, so we built Y" narratives.

**Code hosts (GitHub and similar).** Design docs, RFCs, and ADRs in the repo (often under `docs/`, `rfcs/`, `adr/`) are the richest single source: they state problem, alternatives considered, and chosen mechanism. Next best are PR descriptions for large or long-lived branches, especially with benchmarks, then READMEs explaining novel algorithms, then long-form code comments. Do not read code exhaustively; read documents about the code, dipping into implementation only to confirm details needed for furtherDetails (parameters, data structures, protocol steps). If no GitHub connector is present, public repos are reachable via the GitHub REST API from the sandbox (api.github.com); for private repos, ask the user to connect GitHub or provide the documents directly.

**Issue trackers, project side (Linear, Jira).** Completed projects, epics, and their milestone or project documents contain design rationale for shipped work. For Linear: `Linear:list_projects` to find in-scope projects, `Linear:list_documents` and `Linear:get_document` for project docs, `Linear:list_issues` filtered to the project, `Linear:get_issue` and `Linear:list_comments` on promising hits for design debates. Prefer completed or shipped work; speculative backlog items rarely support a full disclosure.

**Document stores (Google Drive, Notion, Confluence).** Design documents and technical specs, especially with "Alternatives considered" sections (rejected alternatives sharpen differentiating features). Post-mortems are doubly valuable: the incident section is problem-side evidence and the remediation section frequently contains a novel mechanism, pre-paired in one document. Experiment writeups and benchmark reports feed furtherDetails with validation data. Search by scoped folder or project name first; broad keyword sweeps produce noise.

**Engineering chat (Slack).** Secondary source; use it to enrich candidates found elsewhere rather than as a primary sweep, unless the user points at specific channels. Design debates and "we can't do X so we did Y" threads add mechanism detail and reveal the constraints that make a solution non-obvious. Never quote private messages in the report; paraphrase and cite the thread.

**Uploaded files.** Treat uploaded technical documents, papers, and specs as first-class solution-side (and sometimes problem-side) sources; read them fully. Compare an uploaded strategy with the adopted strategy in Lightbringer. Do not silently replace the stored strategy; identify conflicts and proposed changes.

## Pairing the sweeps

Organisations already maintain the links; follow them before inferring anything:

1. **Explicit trace links**: support tickets escalated to tracker issues, issues referenced in PR descriptions and commit messages, project docs citing the motivating incident or customer, changelog entries naming the fixed complaint, post-mortems containing both halves. A traced pair is the strongest candidate.
2. **Thematic and temporal inference**: when links are absent, match problem themes to solution artifacts by topic and timeframe (the project shipped shortly after the complaint spike, the design doc names the symptom). Mark these pairs as inferred; the inventor confirms them later.
3. **Reverse pairing**: for a notable mechanism with no documented motivation, work backwards. Read the artifact's own framing, nearby discussion, and the state of the problem sources just before the work started. Reconstruct the problem, mark it reconstructed.

Classify every finding as paired, unpaired problem, or unpaired solution, per the Phase 1 rules in SKILL.md. Unpaired problems go to the unsolved-problem inventory in the report; unpaired solutions proceed with a reconstructed problem and an inventor-confirmation note.

## Mapping the pair onto the disclosure

Keep the two evidence streams distinct in your notes, because they populate different halves of the Lightbringer schema. Problem-side evidence feeds the problem description, the problems list, and the contexts (operating environments where the pain occurs). Engineering evidence of why the problem happens feeds technicalCauses. Solution-side evidence feeds the invention description, solution, technicalSolution, and furtherDetails. See the authoring reference for detail.

## Assembling the harvest

Maintain a coverage ledger from the start of the sweeps: every in-scope source (project, repo, folder, channel, document set) gets an entry, filled with findings as they accumulate or with an explicit "nothing found because X" justification once the source is exhausted. The ledger is the definition of done for both sweeps: an in-scope source without a completed entry means the sweep is unfinished, so exhaustiveness is a checkable state rather than a feeling of thoroughness. A substantial completed engineering project normally yields at least one candidate mechanism; if one yields nothing, take a second, deeper pass (project docs, PR descriptions, linked threads) before writing its justification. The ledger feeds the coverage audit in SKILL.md and the coverage account in the final report, where per-source yield numbers accumulate across runs into a picture of which sources and project types are worth mining hardest.

Produce structured notes in three lists: problem themes (what fails, for whom, under what conditions, frequency or severity, apparent technical cause, source references), solution mechanisms (how it works causally, motivation, implementation detail, source references), and pairs (problem theme + mechanism + pairing basis: traced, inferred, or reconstructed). These notes feed Phase 2 search queries and Phase 3 identification, and condense into the Material Overview section of the final report.
