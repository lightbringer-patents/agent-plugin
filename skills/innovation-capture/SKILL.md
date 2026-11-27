---
name: innovation-capture
description: Identify, register and enrich Lightbringer innovations from a conversation, an inventor interview or authorised technical sources. Use for lightweight idea saves, direct or guided invention-disclosure authoring toward patenting, including an unsaved read-only draft, updating an innovation, adding an illustration, extracting innovations from documents or engineering work, and patent mining. Exploration alone does not authorise saving; patent-preparation requests and document reviews are separate workflows.
---

# Innovation capture

Identify innovations and, when requested, register or enrich traceable records. An innovation can be a vague idea or a detailed technical description; it does not need to be patent-ready. Read [service conduct](references/service-conduct.md).

Start from the user's actual messages and authorised source material. A summary or arguments supplied by the calling assistant are a proposed interpretation, not additional evidence. Compare them with the original before using them: remove any added component properties, inventor names or performance claims. If the original is unavailable, keep that attribution uncertainty explicit instead of treating the summary as confirmed facts.

## Choose the path first

Choose the intended saved result on each new request, before looking up a template or starting an interview. Follow clear intent without another selection question. When the result is ambiguous, ask: “Would you like to save this idea for later, or develop an invention disclosure toward patenting?” An earlier save or interview does not determine the path for a later request.

The three capture paths are:

- **Lightweight innovation / idea:** read [direct workflow](references/direct-workflow.md) and save through `create_asset` with `type: innovation` when authorised. Preserve available detail and unknowns. Do not retrieve the disclosure template or start a disclosure interview or journey for a simple idea save. Use attributed excerpts of the original technical description, with inventor statements, status and open questions organised separately; do not replace those excerpts with a rewritten problem-and-solution narrative.
- **Invention disclosure through guided capture:** for a disclosure toward patenting, recommend the `invention-capture` journey for guided detail capture when available. Read [capture handoff](references/capture-handoff.md). Discover `start_journey`, `answer_agent` and `get_task_status`, using host tool discovery when definitions are deferred. Start only when the journey and required tools are advertised, carrying the supplied facts and requested outcome. Read-only access and a request for an unsaved draft do not make the journey unavailable. Omit `writable_ids` on a read-only connection.
- **Invention disclosure through direct authoring:** when the user prefers the current assistant, or the journey is unavailable, read [direct workflow](references/direct-workflow.md), retrieve `get_innovation_template`, and author the disclosure here. When saving is authorised, use `create_asset` with `type: invention_disclosure`. For selected saved innovations, include the completed `definition` and `sourceInnovations` together. The journey and direct authoring produce the same kind of disclosure; direct authoring remains a valid choice even when the journey is available.

For an existing record's read, targeted edit or deletion, use [direct workflow](references/direct-workflow.md) without restarting capture. For source exploration, read [source exploration](references/source-exploration.md) before accessing the requested sources, including when capture already happened in this conversation. Follow its context and existing-record checks before reporting findings; exploration does not authorise saving or choosing a disclosure instead of an idea.

After starting a journey, follow `journeys` when installed: poll its returned task, relay its questions and reuse known factual answers. Continue the same task until it needs the user's answer or returns a result. Report an unsaved result as unsaved, retaining its continuation link. Do not run a competing interview, draft or save a second disclosure. Recover an uncertain start or save before considering another path; switching writers is not a retry strategy.

When the journey is unavailable, state the specific missing capability and continue direct authoring if it fulfils the user's request. A refusal or permission limit does not authorise bypassing it through another path. If the user specifically requires Lightbringer's agent, explain the available continuation instead of claiming a local draft fulfils that request. Saving a disclosure does not request patent preparation; service submission remains a separate authorised action.

In every path, use only supplied or retrieved facts. Plausible mechanisms, materials, dimensions, performance claims and embodiments are not established facts. Leave them as specific open questions; do not add them to make a draft look complete. Before presenting or saving a draft, compare each technical sentence with its source: keep a material or property attached to the exact component it describes. For example, a metal housing with a flexible liner does not establish the liner's material. Keep proposed effects distinct from demonstrated performance, and distinguish "not supplied" from a choice the user explicitly says is undecided. Correct unsupported additions before presenting the draft, rather than claiming that a plausible paraphrase contains only supplied facts. Keep source-handling instructions and commentary about the capture process out of the invention prose.

## Verify before handing off or replying

Compare the payload or draft against the original user message, not your own
skill-call summary. Preserve the material assigned to each component; keep any
unmentioned material unknown. An account/profile name is not a confirmed inventor
name. If the user says only “I am the inventor”, carry that statement without
adding a name or inferring a complete inventor list. Reuse an explicitly confirmed
name or inventor list from the invention conversation.

For example, if the original says “I'm the sole inventor” and a caller summary
adds the signed-in person's name, the handoff must say “The user states they are
the sole inventor; their name has not been confirmed for this invention.” Do not
send the added name as confirmed context. If the user earlier said “Ada is the
sole inventor”, retain Ada without asking again.

For a journey result, report its actual saved/unsaved state and include the
returned continuation link. For example: “This is an unsaved draft. Continue the
same capture using this conversation link.” Link to the actual returned URL; never
construct one. Keep remaining factual questions distinct from permissions or
capability limits. A read-only result cannot meet a save criterion.

For direct record work, complete the readback and reporting checks in
[direct workflow](references/direct-workflow.md). No save receipt means no saved
record. Do not offer a different storage destination unless the user wants it.
