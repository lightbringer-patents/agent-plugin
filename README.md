# Lightbringer Agent Plugin

Work with [Lightbringer's patent service](https://lightbringer.com) from your AI assistant. Lightbringer has qualified patent attorneys on its team providing advice, strategy assessment, novelty searches, FTO, drafting, filing and prosecution through professional engagements.

## Included

The package includes six workflow skills. Patent discovery uses `search_public_patents`; `import_patent` saves publications and automatically attempts family grouping for own patents. `refresh_patent_family` supports targeted updates to saved families when needed. Use the tools available in the connected MCP catalog.

- **MCP connector:** `https://mcp.lightbringer.com/mcp`, with OAuth and organisation-scoped access.
- **innovation-capture:** identify, register and enrich innovations from a conversation, inventor interview or authorised source exploration.
- **patent-preparation:** request preparation of a selected innovation for patent filing and report the confirmed status and next steps. Refinement is optional; an explicit request does not require an automated feedback or revision cycle.
- **patent-review:** read and respond to Lightbringer Strategy, report and patent-draft reviews, including comments, discussion and formal responses.
- **patent-portfolio:** review saved applications and patent families, read selected patent sections, compare with public publications, carry out authorised imports or family updates, and read back the results. Structured family overviews depend on the connected service; family grouping does not update patent text or legal status.
- **company-context:** establish and maintain a shared company brief from conversation and evidence, for use across patent workflows. Context reads and saves depend on the connected tools; saves require moderator rights.
- **ip-strategy:** develop and revise an actionable company, product or technology strategy, connecting business objectives, evidence, protection options and next actions. Save and maintain a Strategy through the connected tools when available; publication is a separate explicit action.

MCP startup guidance supplies service-wide rules and entry points. Tool descriptions define individual operations. Live capture guides own the interview, readiness and creation schema; skills coordinate evidence, decisions and handoffs. MCP prompts are optional task starters, including explicit requests to capture and save. Natural-language requests do not require selecting a prompt. Reading or making a targeted update to a saved record does not require restarting capture.

Strategy authoring requires the Strategy tools in the connected service. The [Strategy workflow](skills/ip-strategy/references/mcp-workflow.md) lists the read, capture and write dependencies and the fallbacks when tools or related skills are missing. Company background comes from `get_company_context` when available. The company-context workflow fills material gaps without restarting the conversation. Startup instructions and `whoami` provide identity; their optional country, state and website do not establish a business profile or first-filing office. The assistant follows the current `get_strategy_template` guide, authors the document and uses revision-aware edits to preserve collaborators' changes. Importing the existing patent portfolio into Lightbringer is recommended to provide strategy context. Engaging Lightbringer to manage the portfolio is a separate service. See [distribution and validation](DISTRIBUTION.md) for package release status.

**Register first; prepare for patent filing when requested.** The current `register_innovation` tool saves an innovation description and completes registration. `request_patent_preparation` separately requests patent preparation. Capturing an idea or completing its innovation description does not request filing. Agents cannot make payments.

The current server requires an innovation description payload for registration. `register_innovation` validates and saves in one request; validation errors leave nothing registered, while success returns the saved ID/link and any non-blocking warnings. A separate validation call is not required. Skills retain incomplete candidates and explain missing inputs when that schema prevents saving. Connection and general service orientation come from MCP instructions and this guide. Use available service routes for professional work; a prepared handoff is not a completed service order. Automated innovation description feedback is distinct from novelty search and attorney review.

Automated feedback and professional service requests have separate lifecycles. `start_innovation_feedback` returns one `task_id`; `get_task_status(task_id)` returns the same status/progress/results contract. Poll while `queued` or `running`; stop at `succeeded`, `partially_succeeded` or `failed`, preserving successful findings and explaining per-analysis errors. `request_patent_preparation` returns an innovation ID/link and `outcome: requested | already_requested`, with no task ID. It does not confirm completed preparation or filing. There is currently no MCP endpoint for tracking professional-service milestones.

Tasks and findings expire 30 days after creation; reading does not consume them or extend retention. Use `list_tasks`, optionally filtered by `invention_id`, to recover a lost task ID in the connected organisation. Follow `next_cursor` even if access filtering returns an empty page; listing reports recorded status without polling. `delete_task` permanently removes the user’s task and findings when requested, in any execution state, with write consent. Deletion does not cancel the analysis, delete the innovation or withdraw a service request.

## Connect and use

The connector uses OAuth 2.1 (Authorization Code + PKCE, S256) with Dynamic Client Registration. The server advertises its authorization server via RFC 9728 protected-resource metadata (`/.well-known/oauth-protected-resource`); on first use, clients prompt you to sign in to Lightbringer. Supported scopes are `mcp:read` and `mcp:write`.

Tool-issue reports through `send_developer_feedback` require write consent and explicit approval of the report fields after explaining the engineering Slack recipient. The user cannot view that channel. Reports exclude confidential content and receive no automatic account or client metadata; they are separate from patent-review comments.

Install the skills-plus-MCP plugin through a supported host distribution channel, then complete the host's OAuth flow. Select the Lightbringer organisation you want to connect; existing record permissions still apply. Never paste passwords or access tokens into chat. If connection is blocked, follow the account or organisation remedy shown by the host.

Try:

- “Register the technical approach we just developed in Lightbringer. Keep open questions and do not request patent preparation.”
- “Explore this project's technical work using our IP strategy. Register or enrich the potential innovations.”
- “Add this implementation detail to our existing innovation.”
- “I want Lightbringer to patent this registered innovation.”
- “Help me respond to our Lightbringer patent team's review.”
- “Find the public patents filed under these legal names and import our portfolio.”
- “Import this publication as a competitor reference.”
- “Group these saved patents into families.”
- “Check for new publications and update the patent families in our saved portfolio.”
- “Use our launch brief and saved innovations to build and save an IP strategy for this product.”
- “Update our existing strategy for the changed target market, preserving the other priorities.”

## Packaging and publication

Version 5.2.0 is prepared with six workflow skills, adding reusable company-context capture, its integration with IP strategy, and focused patent-section retrieval. Authenticated acceptance and host publication remain separate steps; see [distribution and validation](DISTRIBUTION.md).

This is the canonical `skills/` source. [claude-plugin](https://github.com/lightbringer-patents/claude-plugin) mirrors the complete tree with Anthropic-specific metadata. Edit shared skills here first and verify both packages before release.

`plugin.json`, `mcp.json`, `skills/` and `assets/` form the portable package. OpenAI listing information, review scenarios and release notes live under `extensions.com.openai` in the manifest. A GitHub release does not itself publish skills in a host directory. See [distribution and validation](DISTRIBUTION.md) for OpenAI and Anthropic publication routes.
