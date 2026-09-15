# Lightbringer Agent Plugin

Work with [Lightbringer's patent service](https://lightbringer.com) from your AI assistant. Lightbringer has qualified patent attorneys on its team providing advice, strategy assessment, novelty searches, FTO, drafting, filing and prosecution through professional engagements.

## Included

Version 1.1.0 targets the released innovation interface in Altair 4.7.0 and Phaenix 12.5.0. The live MCP tool catalog and prompts were verified on 2026-09-15. Update existing installations to use the renamed tools and these three workflow skills. Host-directory publication is separate from the repository release; see [distribution and validation](DISTRIBUTION.md).

- **MCP connector:** `https://mcp.lightbringer.com/mcp`, with OAuth and organisation-scoped access.
- **innovation-capture:** identify, register and enrich innovations from a conversation, inventor interview or authorised source exploration.
- **patent-preparation:** request preparation of a selected innovation for patent filing and report the confirmed status and next steps. Refinement is optional; an explicit request does not require an automated feedback or revision cycle.
- **patent-review:** read and respond to Lightbringer report and patent-draft reviews, including comments, discussion and formal responses.

**Register first; prepare for patent filing when requested.** The current `register_innovation` tool saves an innovation description and completes registration. `request_patent_preparation` separately requests patent preparation. Capturing an idea or completing its innovation description does not request filing. Agents cannot make payments.

The current server requires an innovation description payload for registration. `register_innovation` validates and saves in one request; validation errors leave nothing registered, while success returns the saved ID/link and any non-blocking warnings. A separate validation call is not required. Skills retain incomplete candidates and explain missing inputs when that schema prevents saving. Connection and general service orientation come from MCP instructions and this guide. Use available service routes for professional work; a prepared handoff is not a completed service order. Automated innovation description feedback is distinct from novelty search and attorney review.

Automated feedback and professional service requests have separate lifecycles. `start_innovation_feedback` returns one `task_id`; `get_task_status(task_id)` returns the same status/progress/results contract. Poll while `queued` or `running`; stop at `succeeded`, `partially_succeeded` or `failed`, preserving successful findings and explaining per-analysis errors. `request_patent_preparation` returns an innovation ID/link and `outcome: requested | already_requested`, with no task ID. It does not confirm completed preparation or filing. There is currently no MCP endpoint for tracking professional-service milestones.

Tasks and findings expire 30 days after creation; reading does not consume them or extend retention. Use `list_tasks`, optionally filtered by `invention_id`, to recover a lost task ID in the connected organisation. Follow `next_cursor` even if access filtering returns an empty page; listing reports recorded status without polling. `delete_task` permanently removes the user’s task and findings when requested, in any execution state, with write consent. Deletion does not cancel the analysis, delete the innovation or withdraw a service request.

## Connect and use

The connector uses OAuth 2.1 (Authorization Code + PKCE, S256) with Dynamic Client Registration. The server advertises its authorization server via RFC 9728 protected-resource metadata (`/.well-known/oauth-protected-resource`); on first use, clients prompt you to sign in to Lightbringer. Supported scopes are `mcp:read` and `mcp:write`.

Install the skills-plus-MCP plugin through a supported host distribution channel, then complete the host's OAuth flow. Select the Lightbringer organisation you want to connect; existing record permissions still apply. Never paste passwords or access tokens into chat. If connection is blocked, follow the account or organisation remedy shown by the host.

Try:

- “Register the technical approach we just developed in Lightbringer. Keep open questions and do not request patent preparation.”
- “Explore this project's technical work using our IP strategy. Register or enrich the potential innovations.”
- “Add this implementation detail to our existing innovation.”
- “I want Lightbringer to patent this registered innovation.”
- “Help me respond to our Lightbringer patent team's review.”

## Packaging and publication

This is the canonical `skills/` source. [claude-plugin](https://github.com/lightbringer-patents/claude-plugin) mirrors the complete tree with Anthropic-specific metadata. Edit shared skills here first and verify both packages before release.

`plugin.json`, `mcp.json` and `skills/` form the portable package. A GitHub release does not itself publish skills in a host directory. See [distribution and validation](DISTRIBUTION.md) for OpenAI and Anthropic publication routes.
