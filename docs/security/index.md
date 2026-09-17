# Coding-Agent Threat Modeling & Hardening

Autonomous coding agents introduce novel security risks: malicious prompt injection in open-source dependencies, unauthorized command execution, and accidental secret exfiltration.

---

## 1. The Agent Threat Landscape

```
External Threat Vectors:
├── Prompt Injection via untrusted issues, PR descriptions, or comments
├── Poisoned Dependencies (typosquatting, malicious post-install hooks)
└── Malicious Repositories (payloads disguised as test fixtures)

Execution Risk Vectors:
├── Arbitrary Shell Execution (destructive rm, system modification)
├── Outbound Exfiltration (curling local tokens to external webhooks)
└── Sandbox Escape (exploiting mounted docker sockets or host paths)
```

---

## 2. Mandatory Hardening Rules

1. **Enforce Sandbox Confinement**:
   - Keep `mode = "workspace-write"` in `.codex/config.toml`.
   - Never run Codex with `danger-full-access` on public untrusted codebases.

2. **Strict Approval on Network Calls**:
   - Restrict outbound network calls during testing.
   - Use mock servers or recorded VCR cassettes for HTTP testing.

3. **Secret Hygiene**:
   - Ensure `.env`, `.pem`, and credentials files are listed in `.gitignore`.
   - Implement pre-commit hooks to detect API keys and tokens before commits are created.
