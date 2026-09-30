# Pinned portable manifest schemas

Downloaded 2026-09-30 from the canonical Agent Plugins 1.0.0 schema URLs:

- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

These files are used offline by `scripts/validate_submission.py`; they do not enter
release ZIPs. To update, review the upstream schema diff, replace the exact bytes,
update the hashes below, and run the validator and tests. OpenAI extension fields
are checked separately against the linked OpenAI submission documentation.

- `plugin.schema.json`: `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`
- `mcp.schema.json`: `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb`
