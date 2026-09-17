# Example: Model Context Protocol (MCP) Tool Integration

This example demonstrates how to integrate a database inspection MCP server into OpenAI Codex workflows while enforcing strict read-only sandbox boundaries.

## Architecture
- `codex.config.toml`: Project-level configuration mounting the MCP server via `[mcp_servers.sqlite]`.
- `mcp_server_sqlite.py`: Lightweight Model Context Protocol server exposing database schema inspection and safe read-only SQL querying.
- `test_mcp_sqlite.py`: Test suite verifying safe schema discovery, query execution, and security rejection of write queries.

## Running Tests
```bash
python -m pytest examples/mcp-tool-integration/test_mcp_sqlite.py -v
```
