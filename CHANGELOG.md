# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-09-17
### Fixed & Hardened
- **Concurrency & Self-Transfer Deadlock**: Fixed fatal single-lock hang on self-transfers in `cae-task-001-deadlock` (`benchmarks/tasks/cae-task-001-deadlock/transfer_service_fixed.py`). Replaced sequential lock acquisition with identity branching and absolute deadline thread joins.
- **Evaluator Resilience**: Added 15-second subprocess execution timeouts in `benchmarks/runners/evaluator.py` to prevent zombie benchmark hangs.
- **Race Condition & Validation**: Enforced non-positive order rejection (`quantity <= 0`) in `cae-task-004-race-condition`.
- **Schema Migration Normalization**: Guarded whitespace splitting and null attributes in `cae-task-005-schema-migration`.
- **Skills Production Upgrade**: Populated all 9 skills with genuine executable Python automation scripts, multi-phase checklists (>1,300 bytes), and rich sample outputs (>1,100 bytes). Enforced script presence and completeness in `scripts/validate_skills.py`.
- **Examples Suite**: Upgraded all 4 examples (`full-stack-feature`, `mcp-tool-integration`, `monorepo-agents-hierarchy`, `secure-sandbox-deployment`) with full runnable implementations, configuration manifests, and passing unit test suites (14 tests).
- **Case Studies 8-Part Expansion**: Rewrote all 3 case studies (`01-legacy-repo-modernization.md`, `02-incident-rca-under-time-pressure.md`, `03-supply-chain-vulnerability-containment.md`) to follow the rigorous 8-part engineering narrative structure with benchmark comparison tables and actionable rules for `AGENTS.md`.
- **Provenance Integrity**: Audited `sources/provenance.json` to eliminate self-referential URLs, expanded entries to 11 verified records across all taxonomy tiers, and added strict schema assertions in `tests/test_provenance.py`.
- **AI-DLC Integration**: Enforced AI-DLC block markers (`BEGIN AI-DLC:...` / `END AI-DLC:...`) in `.gitignore` and `AGENTS.md` and populated `aidlc/spaces/default/memory/project.md` with complete decision memory; `aidlc doctor` passes with 0 problems.

## [0.1.0] - 2026-09-17
### Added
- Initial open-source release of Codex Agent Engineering.
- **Core Documentation**: 16 in-depth architectural guides in `docs/` covering Codex surfaces, AGENTS.md hierarchy, sandbox policies, MCP integration, Spec-Driven Development (GitHub Spec Kit), AI-DLC lifecycle, context engineering, debugging, and testing.
- **9 Production Skills**: `repo-audit`, `deep-research`, `implementation`, `debugging`, `test-engineering`, `code-review`, `security-review`, `release-engineering`, and `documentation`.
- **10 Engineering Workflows**: `feature`, `bugfix`, `refactor`, `security-audit`, `repository-audit`, `deep-research`, `incident-response`, `testing`, `pr-review`, and `release`.
- **Reproducible Benchmark Suite v1**: 5 deterministic tasks covering deadlock, SQL injection, async resource leak, race condition, and schema migration, with runner and evaluator.
- **Experiment Registry**: 4 structured experiments (EXP-001 through EXP-004) tracking token budgeting, approval fatigue, MCP overload, and Spec Kit SDD.
- **Case Studies**: 3 real-world technical post-mortems in `case-studies/`.
- **CLI & Automation**: `cae` CLI with benchmark, test, skill validation, link checking, and maintenance scanner.
- **Full Compatibility Matrix**: Tracking Codex CLI, Spec Kit, and AI-DLC across operating systems.
