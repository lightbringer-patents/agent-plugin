---
name: innovation-capture
description: Identify, register and enrich Lightbringer innovations from a conversation, an inventor interview or authorised technical sources. Use for guided invention-disclosure capture with Lightbringer's agent, including an unsaved read-only draft, saving an idea, updating an innovation, adding an illustration, extracting innovations from documents or engineering work, and patent mining. Exploration alone does not authorise saving; patent-preparation requests and document reviews are separate workflows.
---

# Innovation capture

Identify innovations and, when requested, register or enrich traceable records. An innovation can be a vague idea or a detailed technical description; it does not need to be patent-ready. Read [service conduct](references/service-conduct.md).

Start from the user's actual messages and authorised source material. A summary or arguments supplied by the calling assistant are a proposed interpretation, not additional evidence. Compare them with the original before using them: remove any added component properties, inventor names or performance claims. If the original is unavailable, keep that attribution uncertainty explicit instead of treating the summary as confirmed facts.

## Choose the path first

Choose from the user's requested effect before looking up a template or starting an interview:

- **Guided capture with Lightbringer's agent:** read [capture handoff](references/capture-handoff.md) now. Discover the connected `start_journey`, `answer_agent` and `get_task_status` definitions, using the host's tool discovery when definitions are deferred. If `start_journey` advertises `invention-capture`, start that journey with the supplied facts and requested outcome. Read-only access and a request for an unsaved draft do not make the journey unavailable. Omit `writable_ids` on a read-only connection. Do not substitute a locally written draft, a template interview or a strategy search for this handoff.
- **Direct save, read, edit or delete:** read [direct workflow](references/direct-workflow.md) and use the advertised shared asset tools. Do not turn a simple save into a guided interview.
- **Source exploration:** gather evidence on the user's side first, following [source exploration](references/source-exploration.md). Exploration does not authorise saving.

After starting a journey, follow `journeys` when installed: poll its returned task, relay its questions and reuse known factual answers. Keep following the same task until it needs the user's answer or returns a result. Report an unsaved result as unsaved, retaining its continuation link. Do not independently redraft the invention while the journey runs.

Only fall back to the [direct workflow](references/direct-workflow.md) when discovery establishes that the journey or its required question/status tools are unavailable, or a returned refusal prevents starting it. State that specific limitation; do not infer it from the absence of asset-write tools. If the user specifically wants Lightbringer's agent, explain the available continuation instead of claiming a local draft fulfils that request.

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
