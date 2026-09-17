# repo-audit Checklist & Verification Protocol

## Phase 1: Environment & Topography Reconnaissance
- [ ] Record OS, CPU architecture, and available shell environments (pwsh, bash, sh).
- [ ] Inspect git status, remote branches, submodules, and uncommitted modifications.
- [ ] Map repository directory hierarchy down to depth 3, cataloging core namespaces.
- [ ] Identify primary language runtimes, package managers (pip, npm, cargo), and build systems.

## Phase 2: Architecture & Entry Points
- [ ] Locate primary application entry points (`main.py`, `index.ts`, `server.go`, `cli.py`).
- [ ] Trace public API boundary, routing tables, and interface contracts.
- [ ] Identify persistence layers, data schemas, database migrations, and caching tiers.
- [ ] Catalog third-party services, RPC boundaries, and asynchronous queues.

## Phase 3: Testing & Quality Posture
- [ ] Locate automated test suites, test runners, and fixture trees.
- [ ] Verify test execution locally and record test pass rate and duration baseline.
- [ ] Inspect static analysis configuration (linters, typecheckers, code formatters).
- [ ] Inspect CI/CD pipeline definitions in `.github/workflows/` or equivalent.

## Phase 4: Security & Hygiene Audit
- [ ] Scan for committed credentials, plaintext secrets, API keys, or private certificates.
- [ ] Audit dependency manifests for pinned versions and known vulnerable packages.
- [ ] Check OSS governance assets (`LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
- [ ] Validate sandbox safety: identify file writing boundaries and network egress requirements.

## Phase 5: Synthesis & Action Plan
- [ ] Draft executive summary with architectural health rating (Healthy / Moderate Debt / High Risk).
- [ ] Catalog concrete technical debt items with file path citations.
- [ ] Formulate sequenced remediation roadmap with estimated intervention effort.
