# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

- Contract-first Spec-Driven Development using GitHub Spec Kit ($speckit-specify, $speckit-plan, $speckit-tasks, $speckit-implement).
- Stage-gated AI-DLC lifecycle with explicit verification gates at each phase transition.
- Surgical, minimal diffs targeting only explicitly scoped files.

## Walking Skeleton

- Benchmark runner (`benchmarks/runners/runner.py`) executing isolated Python verification tasks via `TaskEvaluator`.
- Unified CLI (`scripts/cae_cli.py`) exposing benchmark, test, skill validation, and health checks.

## Testing Posture

- Strict 4-Tier verification: Unit test suite (`tests/`), Benchmark suite (`benchmarks/tasks/`), Markdown link integrity (`check_links.py`), and Skill schema conformance (`validate_skills.py`).
- 100% test pass rate required prior to commit or conclusion.

## Change Control

- Mode: strict. All production edits require automated verification evidence.

## Deployment

- Local pip editable installation (`pip install -e .`) providing `cae` executable.
- GitHub Actions CI matrix testing Python 3.11, 3.12, 3.13, and 3.14.

## Code Style

- Standard Python 3 PEP 8 style, strict typing where applicable, explicit exception handling.
- Deterministic locking and concurrency order to prevent deadlocks and race conditions.

## Tech Stack

- Python 3.10+
- OpenAI Codex CLI >= 0.145.0
- GitHub Spec Kit (specify 0.16+)
- AI-DLC 2.9+
- Pytest >= 7.0 & pytest-asyncio

## Decided

- DECIDED: Use dedicated temporary directory isolation for benchmark task evaluation (Stage inception, 2026-09-17)
- DECIDED: Enforce provenance linking for all architectural patterns in sources/provenance.json (Stage inception, 2026-09-17)

## Scope Overrides

- None. Standard root repository boundary applies.

## Forbidden

- NEVER commit code without executing local test suites and verifying exit code 0.
- NEVER fabricate, manually inflate, or publish unverified benchmark metrics.
- NEVER claim unsupported OpenAI endorsement or undocumented platform behavior.
- NEVER place multi-step operational runbooks directly into root AGENTS.md when a specialized Skill is appropriate.

## Mandated

- ALWAYS cite external or empirical provenance in sources/provenance.json when introducing new patterns.
- ALWAYS enforce the smallest appropriate Codex surface (Prompt vs AGENTS.md vs Skill vs Plugin vs MCP).
- ALWAYS run `cae doctor` and `pytest` before concluding any turn or releasing a version.

## Corrections

- NEVER omit thread join timeouts or rely on sequential timeouts in multi-threaded concurrency tests.
- ALWAYS normalize whitespace and handle None values in schema migration parsers.
