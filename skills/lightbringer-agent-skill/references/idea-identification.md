# Idea identification reference

How to turn harvested material into a defensible list of distinct potential innovations, aligned with the patent strategy and the organisational context from Phase 2.

## The distinctness test

Two candidate ideas are distinct when either holds:

1. They solve separate technical problems, even with related implementations.
2. They use materially different mechanisms, even against the same problem.

Sharing a broader inventive theme does not merge them. Example: a novel cache-invalidation protocol and a novel replica-placement algorithm may both come from "making the distributed cache fast", but they solve different problems with different mechanisms, so they are two ideas.

Conversely, do not split one mechanism into several ideas because it has multiple benefits, appears in multiple components, or the source material describes it in several places. One mechanism, one idea.

## Per-idea articulation

Describe the problem and proposed approach to the extent known; an innovation can still be vague or incomplete. For each, write down before any authoring begins:

- **Descriptive title**, specific enough to distinguish it from siblings.
- **Inventive concept** in plain language: what it is and the mechanism by which it works.
- **Technical problem** it solves, with its evidence: where the pain was observed (support themes, lost deals, incidents, analytics), at what frequency or severity, and the technical cause it addresses. State whether the pairing was traced through explicit links, inferred from theme and timeframe, or reconstructed from the solution artifact.
- **Differentiating features** relative to the Phase 2 context: what makes it different from existing portfolio items, known competitor filings, and the state of the art found in targeted research. Name the specific delta, not "it is better".
- **Source reference(s)** for both sides of the pair: where the problem evidence lives and where the solution is documented.
- **Strategy alignment**: which strategy focus area or priority it serves, or an explicit note that it falls outside strategy focus. Off-strategy ideas still proceed to authoring; the off-strategy note travels in the report and in the innovation description's reviewCompletion notes so reviewers can weigh it on the platform.

## Combine versus separate

When two innovations are related, record their relationship for later patent-preparation assessment. Do not merge distinct innovation assets merely because they might support one application:

- Note shared dependencies or a common technical cause.
- Keep distinct innovations traceable individually. Selection of one or more innovations for an invention disclosure belongs to explicitly requested patent preparation.

Record the reasoning either way; it goes into the report.

## Capture and qualification are separate

Retain every identified potential innovation in the authorised scope, including incomplete, uncertain and off-strategy concepts. Record the observed mechanism, problem, evidence and open questions. Do not turn uncertainty about patentability or eligibility into a reason to discard it before registration; the Lightbringer patent team can assess it later.

Search for existing concepts before creation. Enrich an identical existing record with supported new context, preserving its earlier decisions and sources. Distinct improvements can have separate records linked by their identifiers and the factual delta. Do not duplicate a rejected concept to bypass its history.

The deployed `register_innovation` schema currently has structured registration requirements. Use the live template honestly. If the available evidence cannot meet the schema without fabrication, retain the candidate in the user-visible summary as pending registration, identify the missing inputs and offer clarification or the platform/team route.

## Technical and eligibility observations

Describe what the solution changes in the technical system and the evidence for that observation. Mark uncertain mechanisms or inferred problem/solution links for inventor clarification. Frame mixed technical and commercial context faithfully without inventing a technical effect. Record eligibility questions for professional assessment, including relevant jurisdictions from the strategy, without presenting the assistant's screening as a legal conclusion.

Do not manufacture novelty, turn every feature into an invention, or invent a solution to an observed problem. Keep unsolved problems visible as research opportunities. A conventional implementation with no identified potential innovation can be reported as such, with its evidence.

## When nothing is identified

For a substantial source with no apparent innovations, check whether important technical context was missed before reporting zero findings. If no potential innovations remain, explain the source coverage and reasons plainly. Never pad the results to achieve a target count.
