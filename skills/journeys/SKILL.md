---
name: journeys
description: Find, start and follow Lightbringer journeys, in which Lightbringer's agent carries out a piece of work from start to finish and reports its outcome. Use when the connection offers list_journeys and the user's goal may match a listed journey, before working through the request step by step with another workflow. Direct requests to capture, import, prepare or review use their own workflow when no journey fits.
---

# Lightbringer journeys

A journey is work that Lightbringer's agent carries out in a conversation of its own. The agent reads the platform data it needs, asks for what it cannot find and reports an outcome. Your part is to choose the journey, give the inputs you already know, wait, deal with its questions and relay the outcome. Do not do the journey's work yourself, and do not write your own version of its result. Follow the [service conduct](references/service-conduct.md) guidance.

The available journeys, their inputs and what each delivers come from `list_journeys`. They can differ between users and connections, so read the list in each conversation.

## Choose a journey

When `list_journeys` is offered and the user's goal may fit a journey, call it before you choose another workflow. Compare the goal with each journey's `when_to_use` and `examples`. If one fits, use it. If two fit, choose the closer one, or ask one short question when the choice changes the result. If none fits, continue with the relevant workflow and do not mention journeys.

If `list_journeys` or `start_journey` is not offered, or the service says that journeys are not available, continue with the other workflows. Do not describe a journey that the connection cannot start.

## Start it

Give each input in the journey's `inputs` that you already know from the conversation, by its `name`, in the user's words. Leave out the inputs you do not know; the agent asks for them when it needs them. Do not interview the user before you start. Never ask the user for anything listed in `reads`: Lightbringer reads it itself.

Tell the user in one or two sentences what the journey does and what it delivers (`outcome.description`). Then call `start_journey` with the journey's id (`journey`) and the `inputs`. If it refuses an input, its message names the inputs that the journey takes; correct the call once. If it does not know the journey, read `list_journeys` again.

`start_journey` returns a conversation task. Keep its `task_id`; every later call uses it.

## Wait

While the task is `running`, call `get_task_status` with the `task_id`. It waits for a change, up to `wait_seconds`, and returns early when the agent asks, finishes or stops. Call it again while the task is still running. When `activity` changes, give the user a short update; do not repeat an unchanged one.

If the user does not want to wait, explain that the work continues in Lightbringer, give the task's `url`, and say that they can come back to it later. Use `cancel_task` only when the user asks to stop the work.

## Questions

A task that is `awaiting_input` has `questions`, and they are for you first. Before you ask the user anything, answer every question that you can answer from this conversation and from what you already know about the user's work. Then ask the user only the rest, as written, with their options and any recommended option. A question that starts with `For the user:` is for the user only: ask it as written, even when you think you know the answer. Do not ask the user a question that you can answer, and do not guess an answer to fill a gap.

Send all answers in one `answer_agent` call: `selected_options` with the option labels exactly as listed, `free_text` with the answer in your words or the user's, or `skip` when neither of you can answer. If an answer is refused because the question already has a different answer, tell the user which answer counts. When you next report to the user, tell them briefly which questions you answered for them and how. Then wait again.

## Outcome

The journey has finished when the task's `journey.outcome` is present.

- Relay the agent's result: its `last_message` and any `outputs` with their links. Keep its content and attribution; shorten it only when the user asks.
- If `outcome.state` is `reached`, say that the journey is complete. If it is `not_reached`, say which `done` items were not met, with their notes.
- For each `coverage` source whose state is `couldnt_check`, tell the user that Lightbringer could not check it, and why. Do not present it as empty. `nothing_found` means that the source was checked and had nothing.
- If the result says that nothing was saved, for example on a read-only connection, say so, and give the link it provides to continue in Lightbringer.

Other states:

- `completed` with no `journey.outcome`: the agent stopped without reporting that the journey finished. Relay `last_message`, say that the journey is not complete, and offer to continue.
- `needs_attention`: relay the reason and give the `url`.
- `cancelled`: say that the journey was stopped.

## After the outcome

For follow-up work on the same result, continue the conversation with `ask_agent` when it is offered, or use the relevant workflow. On a connection without `ask_agent`, a finished journey is over: start the journey again for a new result.

Journeys also work on read-only connections. There, the journey's agent cannot save anything, and `ask_agent` is not offered.

## Finish

Report only what the task confirms. A started journey is not a finished one. An outcome the agent reports is not a professional opinion or a completed service request.

If useful assistance leaves a material customer problem unresolved, follow the [unresolved-needs guidance](references/unresolved-needs.md). Keep helping; reporting is not a prerequisite and requires approval of the exact report and recipient.
