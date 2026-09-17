# Workflow: Repository Structural & Health Audit Workflow

## 1. Input Specification
Repository root path, target architectural guidelines.

## 2. Context Ingestion
Root structure, build configurations, package manifests, CI workflows, documentation.

## 3. Ordered Actions
1. Topography Scan: Map folder hierarchy, line counts, language distributions.
2. Build & Test Health: Test build commands, test runner execution, and lint rules.
3. Dependency Health: Identify outdated, duplicate, or unmaintained packages.
4. Documentation & Hygiene: Check for README, CONTRIBUTING, LICENSE, SECURITY, and AGENTS.md.
5. Remediation Roadmap: Generate prioritized health report with immediate, short-term, and long-term improvements.

## 4. Required Tools & Surfaces
Directory inspection tools (fd/tree), package managers, git log analysis.

## 5. Constraints & Invariants
Read-only operation. Do not modify files or install new dependencies.

## 6. Output & Deliverables
REPO_HEALTH_AUDIT.md containing quantitative health score and prioritized checklist.

## 7. Verification Protocol
Every cited finding must reference an actual file and verifiable defect in the repo.

## 8. Failure Handling & Recovery
For massive monorepos, segment audit by package directory to prevent context window saturation.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex will get lost in large repos without structured phased directory sampling.
