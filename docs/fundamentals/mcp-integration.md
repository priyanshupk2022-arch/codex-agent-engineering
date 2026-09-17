# Model Context Protocol (MCP) Integration

The Model Context Protocol (MCP) provides an open standard for connecting Codex to external tools, databases, web services, and observability platforms without proprietary plugins.

---

## 1. Configuring MCP Servers in Codex

MCP servers are defined inside `.codex/config.toml` (project-scoped) or `~/.codex/config.toml` (developer-scoped):

```toml
[mcp_servers.postgres]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:password@localhost:5432/app_dev"]

[mcp_servers.github]
command = "docker"
args = ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "mcp/github"]
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_TOKEN}" }
```

---

## 2. Architectural Boundaries: MCP vs Native Tools

Do **NOT** use MCP to wrap commands that Codex can already execute natively through its terminal sandbox (e.g., running `git` or `pytest`).

### When to use MCP:
- Reading live production or staging database schemas.
- Interacting with issue trackers (GitHub Issues, Jira).
- Querying remote vector search or enterprise documentation indices.
- Accessing browser automation tools (Playwright / Puppeteer) via controlled protocol.

### Security Boundary:
MCP tool calls execute outside the model's direct sandbox unless routed through the Codex client. Never expose raw arbitrary shell execution via an MCP tool.
