# Idea identification reference

How to turn harvested material into a defensible list of distinct patentable ideas, aligned with the patent strategy and the organisational context from Phase 2.

## The distinctness test

Two candidate ideas are distinct when either holds:

1. They solve separate technical problems, even with related implementations.
2. They use materially different mechanisms, even against the same problem.

Sharing a broader inventive theme does not merge them. Example: a novel cache-invalidation protocol and a novel replica-placement algorithm may both come from "making the distributed cache fast", but they solve different problems with different mechanisms, so they are two ideas.

Conversely, do not split one mechanism into several ideas because it has multiple benefits, appears in multiple components, or the source material describes it in several places. One mechanism, one idea.

## Per-idea articulation

Every idea is a problem-solution pair. For each, write down before any authoring begins:

- **Descriptive title**, specific enough to distinguish it from siblings.
- **Inventive concept** in plain language: what it is and the mechanism by which it works.
- **Technical problem** it solves, with its evidence: where the pain was observed (support themes, lost deals, incidents, analytics), at what frequency or severity, and the technical cause it addresses. State whether the pairing was traced through explicit links, inferred from theme and timeframe, or reconstructed from the solution artifact.
- **Differentiating features** relative to the Phase 2 context: what makes it different from existing portfolio items, known competitor filings, and the state of the art found in targeted research. Name the specific delta, not "it is better".
- **Source reference(s)** for both sides of the pair: where the problem evidence lives and where the solution is documented.
- **Strategy alignment**: which strategy focus area or filing priority it serves, or an explicit note that it falls outside strategy focus. Off-strategy ideas still proceed to authoring; the off-strategy note travels in the report and in the disclosure's reviewCompletion notes so reviewers can weigh it on the platform.

## Combine versus separate

When two distinct ideas are tightly coupled, consider whether they belong in one filing:

- Combine when one is only useful with the other or when they share the same technical cause.
- Keep separate when each stands alone commercially or technically, when they would have different infringement targets, when they sit in different strategy focus areas, or when one is much stronger and would be diluted by the other.

Record the reasoning either way; it goes into the report.

## Quality thresholds

An idea must clear all of these to proceed to authoring:

- It is a genuine pair: a mechanism exists that addresses the problem. An evidenced problem with no solution is not a disclosure candidate; route it to the unsolved-problem inventory instead. A mechanism with only a reconstructed problem may proceed, flagged for inventor confirmation of the problem framing.
- The mechanism is understood well enough to explain causally (problem, cause, technical solution). "Something clever happens in the scheduler" fails.
- The schema minimums (a 200-plus character problem description, a 200-plus character invention description, a 200-plus character furtherDetails) can be met honestly from the sources. Thin-but-real ideas pass this threshold: author what the sources support and record every gap as a pointed reviewCompletion clarity issue naming exactly what the inventor must supply, so the disclosure recruits its own missing detail on-platform. Go back and harvest deeper before judging, and drop only when the minimums cannot be met without fabrication; never pad.
- It is not identical in inventive concept to an existing Lightbringer record found in Phase 2 (including Suggestion records from previous runs). Overlap short of identity is not a drop: create the idea as an explicit improvement or continuation disclosure that names the related record and states the specific delta, recorded in the reviewCompletion notes and prior art section so attorneys can merge or convert on-platform. Identical concepts are skipped with a report note.
- Its technical character is genuine. Pure business methods, presentation choices, and conventional applications of known patterns fail. Customer demand is evidence of value, not of technical character; a heavily requested feature implemented conventionally still fails this test.
- It passes, or is flagged as borderline under, the subject-matter eligibility screen below.

## Subject-matter eligibility screen

Apply this screen to every idea before authoring. It is a triage filter, not a legal opinion: the skill flags and frames, attorneys decide. Never silently drop a borderline idea, and never raise it as a question in chat; a borderline idea proceeds to authoring with its status and the screen's reasoning recorded as a reviewCompletion clarity issue of type "eligibility" inside the disclosure, and in the report, so it can be triaged on the platform.

Categories excluded "as such" in most jurisdictions (EPC Art. 52 and equivalents; the US draws a similar line around abstract ideas): mathematical methods, business methods, schemes and rules for mental acts or games, presentations of information, and computer programs as such. An idea whose sole novelty sits inside one of these categories fails the screen regardless of how clever the implementation is.

Software is not excluded. A computer-implemented invention passes when it produces a further technical effect beyond the ordinary running of a program on a computer. Indicators that it does:

- It controls or measures a physical process, machine, or device.
- It improves the functioning of the computer or network itself: memory use, throughput, latency, energy consumption, bandwidth, storage efficiency.
- It provides a security, cryptographic, or fault-tolerance mechanism.
- It improves data transmission, compression, or encoding.
- Its design is driven by technical considerations of the system's internals (cache behaviour, concurrency, hardware constraints), not only by the meaning of the data being processed.

Indicators that it does not: the novelty lies entirely in business logic, pricing, matchmaking, workflow automation, or organisational rules, merely executed on generic hardware; the contribution is what information is shown or how it is arranged for a human; a mathematical result is applied with no technical implementation beyond running it on a computer.

Most real ideas mix technical and non-technical aspects. For those, frame the idea around its technical contribution: identify the technical problem and technical effect, and let the business benefit be a consequence rather than the invention. If no technical contribution can be honestly identified after this attempt, the idea fails the screen.

If the patent strategy specifies target jurisdictions, apply that lens: an EPO-only strategy makes the technical-effect test decisive, while a US-inclusive strategy warrants an abstract-idea note for borderline software ideas. Record the screen's outcome per idea; it goes into the report alongside the other articulation fields.

## When nothing qualifies

A zero-yield outcome from a substantial source is suspicious before it is acceptable: apply the yield prior and take a second, deeper pass through the source-mining tactics before concluding. If a source, or the entire harvest, still yields no qualifying ideas after that, report it plainly with the reasons (e.g. "the work is a conventional application of known techniques; the novelty is in product scope, not mechanism"). 
