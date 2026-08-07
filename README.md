# Lightbringer Agent Plugin

Patent and invention-management workflows for the [Lightbringer](https://lightbringer.com) platform, packaged as an [Agent Plugin](https://agent-plugins.org) (specification v1.0.0).

## What it includes

- **Lightbringer MCP connector** (`mcp.json`) — remote MCP server at `https://mcp.lightbringer.com/mcp` (Streamable HTTP) providing tools to create, read, search, validate, update, and submit invention disclosures, run patent-analysis feedback, and comment on and respond to reviews.
- **lightbringer-agent-skill** (`skills/`) — an [Agent Skill](https://agentskills.io) that mines company data for patentable problem-solution pairs, authors and submits invention disclosures, and handles Lightbringer review work (Report comments and priority-draft reviews).

## Authentication

The connector uses OAuth 2.1. The server advertises its authorization server via RFC 9728 protected-resource metadata (`/.well-known/oauth-protected-resource`); on first use, clients prompt you to sign in to Lightbringer. Supported scopes are `mcp:read` and `mcp:write`.

## Usage

Ask things like "run patent mining on our recent work", "turn this design doc into a disclosure", or "reply to the comments on the priority draft".

## Relationship to other packages

This repository is the **source of truth for `lightbringer-agent-skill`**. The [claude-plugin](https://github.com/lightbringer-patents/claude-plugin) repository packages the same connector and skill in Claude's plugin format and mirrors the `skills/` tree from here — make skill changes in this repo first, then copy them over.

## Layout

```
plugin.json   Agent Plugins manifest
mcp.json      MCP server declaration
skills/       Agent Skills (lightbringer-agent-skill)
```
