# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-09-17
### Fixed & Hardened
- **Agent Evaluation Architecture**: Implemented `benchmarks/agents/` (`BaseBenchmarkAgent`, `VanillaCodexAgent`, `CaeCodexAgent`) and `benchmarks/runners/agent_runner.py` to execute fair double-track agent comparisons in isolated workspaces with automated diff and log capture.
- **Truthful Evidence Standards**: Completely eliminated fabricated "0% vs 100%" agent benchmark claims in documentation; clearly distinguished deterministic reference passes (100%), buggy defect detection (100%), and unestablished agent comparisons. Implemented automated skip protocol (`AGENT_EVAL_SKIPPED`) when the local environment lacks `codex`.
- **Benchmark Task Hardening**: Added `task.json` hardened metadata, `README.md`, `expected_behavior.md`, and adversarial test suites to all 5 tasks (`cae-task-001` through `cae-task-005`). Supported `--iterations N` and flakiness aggregation in `benchmarks/runners/runner.py`.
- **Automated Report Generation**: Created `scripts/generate_benchmark_report.py` to dynamically compile `benchmarks/results/summary.md` directly from machine-readable benchmark runs.
- **Skill Contract Decoupling**: Created `docs/skills/contract.md` explicitly separating the Codex-Native discovery layer from the CAE Quality & Rigor Layer.
- **Skills Projection Synchronization**: Implemented `scripts/check_skill_sync.py` to project canonical `skills/` into `.agents/skills/` and ensure synchronization.
- **Provenance Taxonomy Hardening**: Updated `sources/provenance.json` with strict `verification_status` (`VERIFIED`, `REPRODUCIBLE`, `COMMUNITY_REPORTED`, `EXPERIMENTAL`, `UNVERIFIED`) and `claim_scope` fields, verified by `tests/test_provenance.py`.
- **Config Safety & Sandboxing**: Created `.codex/config.example.toml` documenting sandbox modes, network access, approval policies, and headless writable roots; removed machine-specific AWS profiles and unrestricted network permissions from shipped defaults.
- **Comprehensive CI Matrix**: Enhanced `.github/workflows/ci.yml` to validate core tests, example tests, reference benchmarks, buggy detection, skill schemas, skill sync, link integrity, and automated release audit.
- **Security & Boundary Test Suite**: Added `tests/test_security.py` covering high-entropy secret scans, temporary directory escape defense, shell=True injection checks, and path traversal protection.
- **Robustness & Failure Tests**: Added `tests/test_robustness_and_failures.py` covering missing executables, missing files, malformed JSON, subprocess timeouts, and empty filters.
- **Automated OSS Release Audit**: Created `scripts/oss_release_audit.py` enforcing 12 non-negotiable release criteria; verified status `OSS_RELEASE_STATUS = PASS`.

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
