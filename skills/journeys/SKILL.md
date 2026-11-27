---
name: journeys
description: Find, start and follow Lightbringer journeys, in which Lightbringer's agent carries out a piece of work from start to finish and reports its outcome. Use when the connection offers start_journey and the user's goal may match a journey that it names, before working through the request step by step with another workflow. Direct requests to capture, import, prepare or review use their own workflow when no journey fits.
---

# Lightbringer journeys

A journey is work that Lightbringer's agent carries out in a conversation of its own. The agent reads the platform data it needs, asks for what it cannot find and reports an outcome. Your part is to choose the journey, give the inputs you already know, wait, deal with its questions and relay the outcome. Do not do the journey's work yourself, and do not write your own version of its result. Follow the [service conduct](references/service-conduct.md) guidance.

The description of `start_journey` names the available journeys. For each one, the description tells what it is for, what it reads, what it delivers and what it saves. The input schema of `start_journey` contains their inputs and describes each input. The description and the input schema can differ between connections, so read both in each conversation.

## Choose a journey

Direct record CRUD follows its asset workflow without a guided journey. Explicit
customer-side source exploration gathers the authorised context first; a journey
cannot read private external material merely because a link was supplied. Guided
disclosure capture may start immediately with the facts already available. Keep
these choices distinct from a professional-service request.

When `start_journey` is offered and the user's goal may fit a journey, check its description before you choose another workflow. Compare the goal with each journey that the description names: what it is for, what it reads and what it delivers. If one fits, use it. If two fit, choose the closer one, or ask one short question when the choice changes the result. If none fits, continue with the relevant workflow and do not mention journeys.

If `start_journey` is not offered, or the service says that a journey is not available, continue with the other workflows. Do not describe a journey that the connection cannot start. If the description of `start_journey` names no journey, for example because the connection still holds an older definition, start none and continue with the relevant workflow; do not look for a separate list of journeys.

Start a journey only when the connection also offers `answer_agent` and a `get_task_status` whose input includes `wait_seconds`. Without them, this connection cannot answer the journey's questions or read its result. In that case, do not start the journey; continue with the relevant workflow instead. Check this before every start, because hosts can make individual tools and tool updates available at different times.

## Start it

In the input schema of `start_journey`, find the inputs that the journey uses. Give each of these inputs that you already know from the conversation, by its name, in the user's words. Leave out the inputs you do not know; the agent asks for them when it needs them. Do not interview the user before you start. Never ask the user for anything that the description says the journey reads: Lightbringer reads it itself.

When the input of `start_journey` includes `writable_ids`, give it only for documents or reports that the user clearly named or chose for the journey to change, and only on a connection that can write. Otherwise leave it out; the agent asks for access when it needs it. If the service refuses `writable_ids` because the connection cannot write, nothing was started: start once more without it. A connection that holds an earlier definition can still show `writable_ids` when the service no longer takes it. The run then starts with no records attached, and the agent asks for access when it needs it. Do not tell the user that a record was attached unless the task confirms it.

Tell the user in one or two sentences what the journey does and what it delivers, as the description says. Include what the description says about Lightbringer credits. Then call `start_journey` with the journey's id (`journey`) and the `inputs`. If it refuses an input, its message names the inputs that the journey takes; correct the call once. If it says that the journey is not available, continue with the relevant workflow.

`start_journey` returns a conversation task. Keep its `task_id`; every later call uses it.

## Wait

While the task is `running`, call `get_task_status` with the `task_id`. It waits for a change, up to `wait_seconds`, and returns early when the agent asks, finishes or stops. Call it again while the task is still running. When `activity` shows a new step, give the user a short update; do not repeat an unchanged one.

When a result includes `next_step`, it states the next action for the conversation; follow it.

If your reply ends while the task is still `running`, tell the user that the agent continues to work. The user sees new progress only when you read the task again.

When the user sends a new message about a different subject while the task is `running` or `awaiting_input`, do these steps in this sequence:

1. Call `get_task_status` with the `task_id` and `wait_seconds` set to `0`. This call does not wait.
2. Reply to the user's message.
3. Go back to the journey. If the task is still `running`, call `get_task_status` again as above. If it is `awaiting_input`, go back to its open questions. The journey stays paused until `answer_agent` sends the answers. If the task has a different status, follow the Outcome section.

If the user does not want to wait, explain that the work continues in Lightbringer, give the task's `url`, and say that they can come back to it later. Use `cancel_task` only when the user asks to stop the work.

## Questions

A task that is `awaiting_input` has `questions`, and they are for you first. Before you ask the user anything, answer every question that you can answer from this conversation and from what you already know about the user's work. Then ask the user only the rest, as written, with their options and any recommended option. A question that starts with `For the user:` is for the user only: ask it as written, even when you think you know the answer. Do not ask the user a question that you can answer, and do not guess an answer to fill a gap.

Never answer for the user a question that asks them to agree to spend Lightbringer credits, to start charged work, or to let the agent save or change a record. Ask the user that question as written, and send only the answer they give.

Send all answers in one `answer_agent` call: `selected_options` with the option labels exactly as listed, `free_text` with the answer in your words or the user's, or `skip` when neither of you can answer. If an answer is refused because the question already has a different answer, tell the user which answer counts. When you next report to the user, tell them briefly which questions you answered for them and how. Then wait again.

## Outcome

The journey has finished when the task's `journey.outcome` is not null.

- Relay the agent's result: its `last_message` and any `outputs` with their links. Keep its content and attribution; shorten it only when the user asks. When the result says how to deliver a report, the next item applies instead.
- A finished task can carry text beside its data that says how to deliver the result; follow that text. When it says that the run saved a report and the connection advertises `show_report`, call `show_report` with the `report:<id>` that the text names. After the view shows the report, do not repeat the report, its findings or its link in chat; add only what the text tells you to add. Do not show the same report again when the view already shows it in this chat. When `show_report` is not advertised, or the view does not show, give the report as text with the line and the report link that the text gives. When the text says that the report was not saved, say so with the line it gives and give the report in chat. A successful tool call alone does not prove that the view showed; without a reported display problem, do not repeat the report.
- If `outcome.state` is `reached`, say that the journey is complete. If it is `not_reached`, say which `done` items were not met, with their notes.
- For each `coverage` source whose state is `couldnt_check`, tell the user that Lightbringer could not check it, and why. Do not present it as empty. `nothing_found` means that the source was checked and had nothing.
- If the result says that nothing was saved, for example on a read-only connection, say so, and give the link it provides to continue in Lightbringer.

If the delivery text names a tool that this connection does not advertise, use the text or link fallback that it gives. Do not call a tool that is not advertised.

Other states:

- `completed` with no `journey.outcome`: the agent stopped without reporting that the journey finished. Relay `last_message`, say that the journey is not complete, and offer to continue with `ask_agent` when it is offered; otherwise offer to start the journey again.
- `needs_attention`: relay `last_message`, if there is one, and give the `url`.
- `cancelled`: say that the journey was stopped.

## After the outcome

For follow-up work on the same result, continue the conversation with `ask_agent` when it is offered, or use the relevant workflow. On a connection without `ask_agent`, a finished journey is over: start the journey again for a new result. To open a saved report again later, use `show_report` with its `report:<id>` when it is advertised; this read saves nothing.

Journeys also work on read-only connections. There, the journey's agent cannot save anything; continue a finished journey with `ask_agent` only when the connection offers it.

## Finish

Report only what the task confirms. A started journey is not a finished one. An outcome the agent reports is not a professional opinion or a completed service request.

If useful assistance leaves a material customer problem unresolved, follow the [unresolved-needs guidance](references/unresolved-needs.md). Keep helping; reporting is not a prerequisite and requires approval of the exact report and recipient.
