# Lightbringer disclosure authoring reference

How to author a submit-ready invention disclosure against the Lightbringer authoring contract. Always fetch the live template with `Lightbringer:get_invention_template` before drafting; this file explains how to use what it returns, and records the constraints observed at the time of writing so you can budget content before the call returns. If the live template disagrees with anything here, the live template wins.

## The pipeline per disclosure

```
get_invention_template  (once per session)
        v
draft definition JSON
        v
validate_invention  --errors-->  fix and re-validate
        v (clean)
create_invention
        v
get_invention_feedback (focus: all)   [may be async; poll via check_task_status]
        v
update_invention (full section replacements, only where fixable from context)
        v
submit_invention (pre-authorised by the confirmed mining brief)
```

## Schema shape and observed constraints (v1)

Top-level required fields: `version` (const 1), `title`, `problem`, `invention`, `furtherDetails`, `reviewCompletion`. Optional: `priorArt`, `illustrationSuggestions`. `additionalProperties` is false everywhere, so never add extra keys.

| Field | Constraint | Notes |
|---|---|---|
| `title` | 1 to 100 chars | Prefix with `Suggestion N - `. Budget the prefix into the 100 chars. |
| `problem.description` | 200 to 3000 chars | Complete problem narrative, submission-grade. |
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

Every "selection object" has the same shape: `item` (short label, max 300 chars), `rationale` (why it belongs in the final disclosure, max 2000), optional `definition` (clarifying explanation, max 2000). Write rationales that justify the selection for this invention, not generic descriptions of the label.

## Writing each part well

**Mapping harvested evidence onto the schema.** The disclosure's two halves draw from the two harvest sweeps. Problem-side evidence (support themes, lost-deal reasons, analytics, incidents) feeds `problem.description`, the `problems` list, and `contexts`; quantified pain (ticket volumes, affected segments, error rates) makes the problem description concrete and evidences commercial relevance. Engineering evidence of why the problem occurs feeds `technicalCauses`. Solution-side evidence (design docs, PRs, ADRs) feeds `invention.description`, `solution`, `technicalSolution`, and `furtherDetails`. Keep customer vocabulary in the problem side where it is vivid and accurate, but translate it into technical failure modes; "checkout feels slow" becomes a described latency source with its cause.

**Problem section.** The description must stand alone; a reader with no access to the source material should understand what hurts and why. `technicalCauses` is the load-bearing part: it is what the technical solution must answer. Derive causes from the harvested engineering material (architecture constraints, failure modes discussed in issues, measured bottlenecks), not from marketing language. When the problem was reconstructed from the solution artifact rather than traced from problem sources, keep the description faithful to what the artifact supports and record the confirmation need as a clarity issue in reviewCompletion.

**Invention section.** `solution` names the invention-level concept; `technicalSolution` explains the mechanism that addresses the identified causes. Prefer causal technical explanation over benefit language. A test that works: could a competent engineer sketch the system from `invention.description` plus `technicalSolution`? If not, it is too vague.

**furtherDetails.** This is for structured depth, not a restatement of the summary. Mine the sources for alternate embodiments, configurations, parameter ranges, fallback behaviour, prototype or benchmark results, and equivalent implementations. Engineering sources are usually rich here (PR descriptions, design-doc alternatives sections, load-test numbers). Capture resolved detail here rather than deferring it to open issues.

**priorArt.** Include only when prior art is actually known from the current context: Phase 2 portfolio findings, targeted external research results, or references cited in the source material itself. Prefer concrete references over generic "existing systems typically..." filler. When included, explain both what the prior art does and why it falls short. When nothing concrete is known, omit the object entirely; do not pad.

**illustrationSuggestions.** Write for the inventor as recipient, in plain technical language. Name a concrete deliverable and say what it should show, e.g. "Sequence diagram of the cache-invalidation handshake, showing the replica, the coordinator, and the version-vector exchange on write". Match the type to the domain: architecture and data-flow diagrams for software, cross-sections and exploded views for mechanical, reaction schemes for chemistry. These populate disclosure tips only; they do not attach files.

**reviewCompletion.** Two modes:

- `NO_OPEN_ISSUES`: use only when the disclosure is genuinely ready without inventor follow-up.
- `OPEN_ISSUES_REMAIN` with `clarityIssues`: the honest default for mined disclosures, since source material rarely covers everything an attorney needs. Each clarity issue needs a `type` (e.g. parameter range, boundary behavior, embodiment), a `label` naming the specific gap, and a `description` saying exactly what is missing and why it matters.

Good residual issues: undefined thresholds, vague relative terms needing operational definitions, missing failure or fallback behaviour, missing concrete embodiments. Three flag types from earlier phases also live here: an issue of type "eligibility" carrying the subject-matter screen's borderline reasoning, an issue of type "problem confirmation" when the problem was reconstructed from the solution artifact and the inventor should confirm the framing, and pointed detail-recruitment issues for thin-but-real ideas, each naming exactly what the inventor must supply. For improvement or continuation disclosures, name the related portfolio record and the specific delta in the reviewCompletion notes and, where known prior art exists, in the priorArt section. Bad residual issues: things already answered elsewhere in the payload, information you could have resolved from the sources, or speculative nice-to-haves. Author first, record only the genuine remainder.

## Tool-use specifics

- `create_invention` takes `{ definition: <the JSON object> }`.
- `validate_invention` takes the same shape; run it before every create, and again after substantial edits if re-creating.
- `update_invention` takes `invention_id` and a `sections` map with keys from: `problem`, `solution`, `details`, `priorArt`, `shortcomings`. It overwrites, so send complete replacement text for the sections you touch. Note these section names differ from the authoring schema's field names; they address the rendered disclosure sections.
- `get_invention_feedback` supports `focus` of `clarity`, `problem`, `completeness`, or `all`. Responses may return pending with ticket identifiers; poll with `Lightbringer:check_task_status` and interleave other work while waiting.
- `submit_invention` takes `invention_id` and is the only step that changes review status. Call it for every successfully created and refined disclosure as part of the standard run; never submit anything that failed validation or creation, and always account for every submission in the final report.
- Drawings cannot be attached through this path. If the sources contain relevant diagrams or the inventor has drawings, tell the user to upload them manually in the disclosure UI after creation.

## Common validation failures to avoid

- Descriptions under the 200-char minimums (usually a symptom of a thin idea; consider whether it should have survived Phase 3).
- Missing `rationale` on a selection object.
- Extra properties from pasting template comments into the payload.
- `reviewCompletion` with `OPEN_ISSUES_REMAIN` but no `clarityIssues` array.
- Titles over 100 chars once the `Suggestion N - ` prefix is added.
