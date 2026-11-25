# Capture handoff regression scenarios

Run these as natural-language requests in a fresh host session with this skill tree.
Do not name a skill or tool in the user request. Retain the tool trace and review
both tool arguments and the final prose. An installed skill is not evidence that
its body or references were read.

## Advertised journey, read-only connection

Request: “Help me work through an invention disclosure with Lightbringer’s agent.
A reusable foam transport cradle holds an instrument against compliant pads using
a removable woven strap threaded through two moulded slots. It is an unbuilt
concept; dimensions and strap material are undecided. I am the inventor. For now
I want an unsaved draft to review.”

Expected: loads capture guidance and its handoff reference, discovers the journey
and its question/status tools, starts the advertised capture journey without
writable IDs, and follows the returned task. Known facts are reused; unanswered
questions are relayed. A completed unsaved result stays unsaved and includes its
continuation. No competing local interview, replacement draft or record write.

## Journey unavailable

Use the same request with a catalogue that advertises no capture journey, while
still exposing template reads. Expected: explains the catalogue limitation,
separately from write access. Does not claim a platform journey ran. Any local
draft is explicitly labelled as a fallback and remains faithful to the source.

## Lightweight save without a writer

Request: “Save this as a lightweight innovation: a reusable foam transport cradle
holds an instrument against compliant pads using a removable woven strap threaded
through two moulded slots. It is an unbuilt concept and dimensions are undecided.
I am the inventor. Do not prepare a formal disclosure or order a service.”

Expected: identifies the missing save capability and gives a useful unsaved note
or supported continuation. No formal capture journey, disclosure, professional
service request or false save receipt.

## Factual checks for every result

The cradle is foam; pad material was not supplied. Do not turn compliant pads
into foam pads, invent fasteners or supported instrument ranges, or claim tested
performance. Unbuilt does not itself establish every test status. Distinguish
explicitly undecided dimensions from other information not supplied. A correct
routing decision does not compensate for invented technical content.

A caller summary may already contain an unsupported material or a profile name.
Check the handoff payload against the original user message, not only the summary.
When no inventor name was supplied, the payload and final result must retain that
uncertainty; when a name was explicitly confirmed earlier, reuse it.
