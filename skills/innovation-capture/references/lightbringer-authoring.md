# Lightbringer innovation authoring reference

How to author a supported innovation record against the Lightbringer authoring contract. Fetch the live template with `get_innovation_template` before drafting. Its schema and field constraints govern the registration payload. Use the guidance below to organize supported content. Registration and preparation remain separate actions; template completeness never authorises patent preparation.

## The pipeline per innovation description

```
get_innovation_template  (once per session)
        v
draft definition JSON
        v
register_innovation  --validation errors, not saved-->  fix supported fields and retry
        v (saved, possibly with warnings)
registration complete — return the saved record link and warnings

Optional refinement, when requested:
start_innovation_feedback (focus: all)   [one task_id; poll get_task_status(task_id) while queued/running]
        v
update_innovation (full section replacements, only where fixable from context)
        v
registration/enrichment complete — return the saved record link

Separate explicit patenting intent only: request_patent_preparation → patent preparation requested
```

## Schema shape and observed constraints (v1)

Top-level required fields: `version` (const 1), `title`, `problem`, `invention`, `furtherDetails`, `reviewCompletion`. Optional: `priorArt`, `illustrationSuggestions`. `additionalProperties` is false everywhere, so never add extra keys.

| Field | Constraint | Notes |
|---|---|---|
| `title` | 1 to 100 chars | Use a descriptive title; preserve existing titles when enriching a record. |
| `problem.description` | 200 to 3000 chars | Supported problem narrative; record remaining uncertainties. |
| `problem.technologyField` | single selection object | One resolved field, not a list. |
| `problem.problems` | array, min 1 | Concrete problem statements. |
| `problem.technicalCauses` | array, min 1 | Why the problems occur, technically. |
| `invention.description` | 200 to 3000 chars | What it does and how it works. |
| `invention.inventionType` | single selection object | e.g. "System with coordinated control method". |
| `invention.contexts` | array, min 1 | Operating environments and scenarios. |
| `invention.solution` | single selection object | The invention-level concept. |
| `invention.technicalSolution` | single selection object | The mechanism that addresses the causes. |
| `furtherDetails` | 200 to 10000 chars | Embodiments, variants, parameters, validation data. |
| `priorArt.summary` | 100 to 2000 chars | Optional; omit the whole object if not warranted. |
| `priorArt.shortcomings` | 100 to 2000 chars | Optional within priorArt. |
| `illustrationSuggestions` | array, min 1 if present | Inventor-facing drawing suggestions. |

Every "selection object" has the same shape: `item` (short label, max 300 chars), `rationale` (why it belongs in the final innovation description, max 2000), optional `definition` (clarifying explanation, max 2000). Write rationales that justify the selection for this invention, not generic descriptions of the label.

## Writing each part well

**Mapping harvested evidence onto the schema.** The innovation description's two halves draw from the two harvest sweeps. Problem-side evidence (support themes, lost-deal reasons, analytics, incidents) feeds `problem.description`, the `problems` list, and `contexts`; quantified pain (ticket volumes, affected segments, error rates) makes the problem description concrete and evidences commercial relevance. Engineering evidence of why the problem occurs feeds `technicalCauses`. Solution-side evidence (design docs, PRs, ADRs) feeds `invention.description`, `solution`, `technicalSolution`, and `furtherDetails`. Keep customer vocabulary in the problem side where it is vivid and accurate, but translate it into technical failure modes; "checkout feels slow" becomes a described latency source with its cause.

**Problem section.** The description must stand alone; a reader with no access to the source material should understand what hurts and why. `technicalCauses` is the load-bearing part: it is what the technical solution must answer. Derive causes from the harvested engineering material (architecture constraints, failure modes discussed in issues, measured bottlenecks), not from marketing language. When the problem was reconstructed from the solution artifact rather than traced from problem sources, keep the description faithful to what the artifact supports and record the confirmation need as a clarity issue in reviewCompletion.

**Invention section.** `solution` names the invention-level concept; `technicalSolution` explains the mechanism that addresses the identified causes. Prefer causal technical explanation over benefit language. A test that works: could a competent engineer sketch the system from `invention.description` plus `technicalSolution`? If not, it is too vague.

**furtherDetails.** This is for structured depth, not a restatement of the summary. Mine the sources for alternate embodiments, configurations, parameter ranges, fallback behaviour, prototype or benchmark results, and equivalent implementations. Engineering sources are usually rich here (PR descriptions, design-doc alternatives sections, load-test numbers). Capture resolved detail here rather than deferring it to open issues.

**priorArt.** Include only when prior art is actually known from the current context: portfolio findings, targeted external research results, or references cited in the source material itself. Prefer concrete references over generic "existing systems typically..." filler. When included, explain both what the prior art does and why it falls short. When nothing concrete is known, omit the object entirely; do not pad.

**illustrationSuggestions.** Write for the inventor as recipient, in plain technical language. Name a concrete deliverable and say what it should show, e.g. "Sequence diagram of the cache-invalidation handshake, showing the replica, the coordinator, and the version-vector exchange on write". Match the type to the domain: architecture and data-flow diagrams for software, cross-sections and exploded views for mechanical, reaction schemes for chemistry. These populate innovation description tips only; they do not attach files.

**reviewCompletion.** Two modes:

- `NO_OPEN_ISSUES`: use only when the innovation description is genuinely ready without inventor follow-up.
- `OPEN_ISSUES_REMAIN` with `clarityIssues`: the honest default for mined innovation records, since source material rarely covers everything an attorney needs. Each clarity issue needs a `type` (e.g. parameter range, boundary behavior, embodiment), a `label` naming the specific gap, and a `description` saying exactly what is missing and why it matters.

Good residual issues: undefined thresholds, vague relative terms needing operational definitions, missing failure or fallback behaviour, missing concrete embodiments. Three flag types from earlier phases also live here: an issue of type "eligibility" carrying the subject-matter screen's borderline reasoning, an issue of type "problem confirmation" when the problem was reconstructed from the solution artifact and the inventor should confirm the framing, and pointed detail-recruitment issues for thin-but-real ideas, each naming exactly what the inventor must supply. For related innovations, name the related portfolio record and the specific delta in the reviewCompletion notes and, where known prior art exists, in the priorArt section. Bad residual issues: things already answered elsewhere in the payload, information you could have resolved from the sources, or speculative nice-to-haves. Author first, record only the genuine remainder.

## Tool-use specifics

- `register_innovation` takes `{ definition: <the JSON object> }` and validates before creating the record. Call it only when saving is authorised; it is not a validation-only preview. Validation errors mean nothing was registered: correct the reported fields from supported context before retrying. A successful result contains the saved ID/link and may contain non-blocking `warnings`; report them without retrying registration.
- `update_innovation` takes `invention_id` and a `sections` map with keys from: `problem`, `solution`, `details`, `priorArt`, `shortcomings`. It overwrites, so send complete replacement text for the sections you touch. Note these section names differ from the authoring schema's field names; they address the rendered innovation description sections. Check each section's `applied`/`error` outcome and read back with `get_innovation` when needed. Do not re-register an existing record to validate its changes.
- `start_innovation_feedback` supports `focus` of `clarity`, `problem`, `completeness`, or `all`. The response contains one `task_id`, a `status`, `progress` counts and per-analysis `results`. Poll `get_task_status(task_id)` while `queued` or `running`; both tools return the same contract. `succeeded`, `partially_succeeded` and `failed` are terminal: retain available findings and explain any per-analysis errors. Interleave other work while waiting. Ending the wait does not cancel analysis. This task is unrelated to preparation or filing milestones.
- `request_patent_preparation` takes `invention_id` and records a patent-preparation request. Automated feedback and revisions are optional, not prerequisites to an explicit request. It is not required for registration. Use only for explicit intent to have Lightbringer patent the selected innovation; report the actual returned status without claiming filing or payment.
- Drawings cannot be attached through this path. If the sources contain relevant diagrams or the inventor has drawings, tell the user to upload them manually in the innovation description UI after creation.

## Common validation failures to avoid

- Descriptions under the current minimums: gather missing context without padding; if saving remains impossible, retain the candidate in the user-visible pending-registration summary.
- Missing `rationale` on a selection object.
- Extra properties from pasting template comments into the payload.
- `reviewCompletion` with `OPEN_ISSUES_REMAIN` but no `clarityIssues` array.
- Titles over the live template limit.

## Interactive capture and current limitations

Follow the live template's interactive capture guidance when the inventor is present; use autonomous capture guidance for authorised source mining. Ask focused questions about the mechanism and evidence, not a long generic questionnaire. Preserve honest open questions. Current tools may require a structured registration payload even when the user's goal is lightweight registration: explain this limitation and never fabricate fields to make validation pass.
