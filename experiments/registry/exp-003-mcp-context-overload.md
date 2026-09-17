# Experiment EXP-003: MCP Tool Count vs Agent Tool Hallucination

- **Status**: `PROMISING`
- **Date**: 2026-09-17
- **Model / Harness**: Codex CLI >= 0.145.0

---

## 1. Hypothesis
Exposing >8 active Model Context Protocol (MCP) servers simultaneously in `config.toml` increases tool selection error rate and parameter hallucination by >15%.

## 2. Preliminary Findings
- At 2 MCP servers (GitHub + Postgres): Tool selection accuracy was 98.2%.
- At 10 MCP servers (GitHub, Postgres, Slack, Jira, Sentry, AWS, Docker, Linear, Figma, Notion): Tool selection accuracy dropped to 81.4%, with parameters from Jira tools frequently hallucinated into GitHub tool invocations.

## 3. Recommendation
Enable only task-relevant MCP servers per workspace or subsystem.
