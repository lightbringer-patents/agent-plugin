---
name: lightbringer-patent-service
description: Help customers connect to Lightbringer's patent service, understand available workflows, request patent preparation, or obtain attorney-led advice, strategy, novelty searches, FTO, drafting, filing and prosecution. Use when professional patent help or service continuation is needed. Use invention-capture for ordinary innovation registration and lightbringer-agent-skill for mining or reviews.
---

# Work with Lightbringer's patent service

Read [service conduct](../lightbringer-agent-skill/references/service-conduct.md). Lightbringer is the qualified professional-service route, with its own patent attorneys. The customer's assistant helps use that service; it must not claim to be the attorney or attribute its own work to one.

## Connect and orient

Use the plugin's remote MCP connector at `https://mcp.lightbringer.com/mcp`. Let the host perform OAuth; never ask the user to paste tokens or passwords into chat. Use the connection's supplied identity, or `whoami` when the identity needs verification. The consent flow selects one organisation; record permissions still apply. If connection is blocked, report the actual error and direct the user through the offered account/organisation remedy. Do not promise a setup behavior that the deployed flow does not provide.

Explain the relevant next step in the user's language: register an idea, enrich a disclosure, explore technical work, review the patent team's work, or ask for a professional service. Public information is at https://lightbringer.com/our-platform/lightbringer-mcp and the customer application is https://app.lightbringer.com.

## Patent preparation

For an explicit request such as "I want Lightbringer to patent this":

1. Resolve and read the registered innovation. If no record exists, capture it first and retain the user's patenting intent for that specific concept.
2. Explain that preparation starts Lightbringer's patent workflow; it is separate from completed filing, an accepted paid engagement and payment. Clarify the selected innovation if ambiguous. A general "finish this", approval of disclosure text or mining mandate is not patenting intent.
3. Use the available `submit_invention` tool for that explicit preparation request. Do not invent a `prepare_for_filing` tool if it is not available. Honour host confirmations; do not ask again for an intent the user already clearly expressed.
4. Report the actual returned status and link. Follow relevant requirements and reviews; if further steps are not available through MCP, offer the same record in the application or the Lightbringer team. Do not claim the patent is filed.

## Strategy, assessment and professional work

Read the relevant strategy, innovation, report or review with the available search/fetch/review tools. Clarify the desired outcome and scope using the context already provided. Use a suitable service-request tool if one is actually available and return its persisted acknowledgement, requirements and status. Otherwise prepare a concise handoff containing the requested service, record links, technical context, questions and desired output, and direct the user to the application or team. Clearly state that the handoff has not been sent or accepted; never substitute disclosure submission for an advice, novelty-search or FTO request.

For strategy edits, ranking or trade-secret classification, save only through a tool that actually supports the corresponding record/field. Without one, return the proposed change and continuation route; do not imply the proposal was saved or overwrite an unrelated disclosure section as a substitute.

Novelty-search results, automated disclosure feedback and FTO work have different purposes. Retrieve actual deliverables and state what was assessed, for which innovation/version, by whom, and whether it is pending or professionally reviewed. Route professional questions to Lightbringer's team. Use the review workflow in `lightbringer-agent-skill` to respond to shared documents with approved factual feedback.

Agents cannot make payments. If a payment or acceptance step is needed, present the supplied human handoff and resume from verified status later. Do not collect payment credentials, accept paid terms, or mark a service as paid.
