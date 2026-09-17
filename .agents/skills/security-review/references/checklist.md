# security-review Checklist & Threat Modeling Protocol

## Phase 1: Authentication & Secrets Management
- [ ] Zero committed credentials, private keys, API tokens, or session secrets.
- [ ] Secrets retrieved strictly via environment variables or secret managers.
- [ ] Production and staging credentials strictly separated.
- [ ] `.gitignore` contains rules for `.env*`, `*.pem`, `*.key`, and credentials.

## Phase 2: Injection & Untrusted Input Defenses
- [ ] All database queries parameterized; zero string formatting in SQL statements (CWE-89).
- [ ] Command execution audited: zero `shell=True` on untrusted user strings (CWE-78).
- [ ] HTML/XML rendering properly escaped to prevent Cross-Site Scripting (CWE-79).
- [ ] File path inputs validated against directory traversal (`../`) attacks (CWE-22).

## Phase 3: Agent Sandbox & Approval Boundaries
- [ ] Codex sandbox set to `mode = "workspace-write"` or `"read-only"`.
- [ ] Destructive commands (`rm -rf`, `drop table`, `git push --force`) require human approval.
- [ ] MCP tool invocations validated for parameter boundary compliance.
- [ ] Network outbound egress limited to verified package registries.

## Phase 4: Dependency Vulnerability Audit
- [ ] Dependency lockfiles committed and verified with checksums.
- [ ] Vulnerability audit run via `pip audit` or `npm audit`.
- [ ] No vulnerable or deprecated cryptographic algorithms in use (e.g. MD5 for password hashing).
