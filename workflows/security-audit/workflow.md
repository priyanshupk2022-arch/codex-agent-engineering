# Workflow: Security Audit & Vulnerability Assessment Workflow

## 1. Input Specification
Target codebase, threat model scope, compliance guidelines (OWASP, CWE).

## 2. Context Ingestion
Authentication middlewares, database query layers, file upload handlers, dependency manifests.

## 3. Ordered Actions
1. Surface Mapping: Catalog all external input entry points (REST, GraphQL, CLI, env vars).
2. Injection Audit: Inspect SQL, command execution, and template rendering for unparameterized inputs.
3. Authentication & Authorization Check: Audit permission checks on every sensitive endpoint.
4. Dependency Audit: Scan package manifests for CVEs and unmaintained libraries.
5. Local PoC Testing: Develop safe local test cases proving or disproving potential vulnerabilities.
6. Remediation Proposal: Author patches using parameterized APIs and principle of least privilege.

## 4. Required Tools & Surfaces
Security scanners (semgrep/bandit/npm audit), git grep, test runner, AST parsers.

## 5. Constraints & Invariants
Strict read-only execution during scanning. Do not trigger external network attacks or send payloads to production systems.

## 6. Output & Deliverables
SECURITY_AUDIT_REPORT.md with findings categorized by CVSS, reproduction PoCs, and remediations.

## 7. Verification Protocol
All proposed remediations must be verified by re-running local exploit test to prove closure.

## 8. Failure Handling & Recovery
If vulnerability remediation breaks legitimate functionality, consult product spec to introduce backward-compatible security guards.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex cannot perform thorough security audits due to lack of systematic checklists and hallucination of non-existent CVEs.
