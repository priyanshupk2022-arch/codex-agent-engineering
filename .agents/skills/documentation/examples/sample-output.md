# Sample Documentation: Codex Sandbox Boundary Configuration Guide

**Document ID**: `docs/fundamentals/sandbox-and-approvals.md`  
**Audience**: Staff Engineers & Platform Architects  
**Author**: CAE Technical Writing Specialist  
**Standard**: Full Conformance to CAE Documentation Style  

---

## 1. Overview
The OpenAI Codex CLI executes commands within an OS-level execution sandbox designed to prevent accidental host modification and data exfiltration. This guide outlines how to configure sandbox containment levels and approval policies for both interactive and headless CI environments.

---

## 2. Sandbox Modes Comparison

| Mode | Filesystem Access | Network Access | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **`read-only`** | Strictly read-only | Blocked | Code exploration, security audits, PR review |
| **`workspace-write`** | Read/write in project root only | Whitelisted hosts only | Standard development (Default) |
| **`danger-full-access`** | Unrestricted host access | Unrestricted | Isolated containerized CI runners |

---

## 3. Configuration Example (`.codex/config.toml`)
```toml
[sandbox]
mode = "workspace-write"
allowed_network_hosts = [
  "github.com",
  "pypi.org",
  "registry.npmjs.org"
]

[approval]
policy = "on-request"
```
