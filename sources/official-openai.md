# Official OpenAI Codex & Platform References

This document catalogs official OpenAI documentation, specifications, and primary source materials concerning the Codex CLI, AGENTS.md, runtime models, configuration schemas, and execution sandboxes.

## 1. OpenAI Codex CLI & Core Primitives
- **Source Identifier**: `OFFICIAL-CODEX-001`
- **Component**: Codex CLI Architecture & Execution Loop
- **Source URL**: https://github.com/openai/codex
- **Version Tested**: Codex CLI >= 0.145.0
- **Retrieved At**: 2026-09-17
- **Confidence**: 1.0 (Official Specification)
- **Key Facts**:
  - The Codex CLI operates as an interactive and non-interactive terminal coding agent.
  - Native configuration is loaded hierarchically from `~/.codex/config.toml` (global user defaults) and `.codex/config.toml` (project-scoped settings).
  - Terminal commands are routed through an OS-enforced execution sandbox.

## 2. AGENTS.md Hierarchy & Precedence
- **Source Identifier**: `OFFICIAL-AGENTS-001`
- **Component**: Agent Instruction Standard
- **Source URL**: https://github.com/openai/codex/blob/main/docs/AGENTS.md
- **Retrieved At**: 2026-09-17
- **Confidence**: 1.0 (Official Standard)
- **Key Facts**:
  - `AGENTS.md` acts as a deterministic instruction file for coding agents, specifying build, test, and contribution conventions.
  - Directory Traversal: Codex walks from the project root down to the current working directory, concatenating instructions where deeper directories take precedence for conflicting directives.
  - User Overrides: `AGENTS.override.md` takes local precedence over standard `AGENTS.md` without polluting version-controlled files.
  - Global Instructions: `~/.codex/AGENTS.md` provides global user directives that apply across all workspaces.

## 3. Sandbox Boundaries & Approval Policies
- **Source Identifier**: `OFFICIAL-SANDBOX-001`
- **Component**: Security & Isolation Engine
- **Source URL**: https://platform.openai.com/docs/codex/security
- **Retrieved At**: 2026-09-17
- **Confidence**: 1.0 (Official Specification)
- **Key Facts**:
  - Sandbox Modes:
    - `read-only`: Filesystem modifications and outbound network calls are blocked.
    - `workspace-write` (Default): Filesystem writes are strictly restricted to the project root. Subprocess network access is restricted to configured allowlists.
    - `danger-full-access`: Unrestricted host execution (disables container isolation).
  - Approval Policies:
    - `on-request`: Prompts developer confirmation when operations exceed declared safe parameters.
    - `untrusted`: Every side-effect command requires explicit human acknowledgement.
    - `never`: Prompts are suppressed (used in CI/CD autonomous runners).

## 4. Model Context Protocol (MCP) Integration
- **Source Identifier**: `OFFICIAL-MCP-001`
- **Component**: Extensible Tool & Resource Integration
- **Source URL**: https://modelcontextprotocol.io
- **Retrieved At**: 2026-09-17
- **Confidence**: 1.0 (Open Standard / Official Support)
- **Key Facts**:
  - Configured in `config.toml` under `[mcp_servers.<name>]`.
  - Supports `stdio` and `sse` transports with environment variable passing.
  - Tool invocations through MCP are subject to sandbox approval rules.
