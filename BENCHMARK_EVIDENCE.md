# CAE Empirical Benchmark Evidence Ledger (BENCHMARK_EVIDENCE.md)

This ledger records the exact, reproducible execution artifacts and evidence captured from local verification runs of the **Codex Agent Engineering Framework**.

---

## 1. Execution Environment & Provenance Metadata

| Parameter | Recorded Value |
| :--- | :--- |
| **Audit Timestamp** | `2026-09-17 05:43:00 UTC` |
| **Base Commit SHA** | `9c6648e59a7c4ae1baa6efbe92d3b4d6e318ef22` |
| **Operating System** | `Windows 11 (win32)` |
| **Python Version** | `3.14.3` |
| **Pytest Version** | `9.1.1` |
| **Codex CLI Availability** | `Not Installed (Agent evaluation skipped per Rule #1)` |
| **Benchmark Suite Version** | `1.0.0` |
| **Audit Status** | `OSS_RELEASE_STATUS = PASS (12/12 gates)` |

---

## 2. Command Execution & Exact Results

### Command 1: Core Test Suite
```bash
python -m pytest tests/ -v
```
- **Exit Code**: `0`
- **Result**: `22 passed in 18.25s`
- **Coverage**:
  - `test_adapter.py`: 2 tests passed (initialization & nonexistent executable handling)
  - `test_cli.py`: 2 tests passed (CLI commands & validation)
  - `test_evaluator.py`: 2 tests passed (reference & buggy batch evaluations)
  - `test_metric_collector.py`: 1 test passed (aggregation & summary calculation)
  - `test_provenance.py`: 1 test passed (11 records with verification_status & claim_scope)
  - `test_skills_schema.py`: 1 test passed (schema conformance across all skills)
  - `test_workflows_integrity.py`: 1 test passed (all 10 workflows define vanilla comparison)
  - `test_security.py`: 5 tests passed (zero secrets, temp workspace isolation, shell=False, config boundaries, path traversal defense)
  - `test_robustness_and_failures.py`: 7 tests passed (missing binary, agent skip, missing task file, malformed JSON, subprocess timeout, filter empty, skill sync diff)

### Command 2: Deterministic Reference Suite (Multi-Iteration Flakiness Check)
```bash
python benchmarks/runners/runner.py reference --iterations 2
```
- **Exit Code**: `0`
- **Tasks**: 5
- **Iterations**: 2
- **Pass Rate**: `100.0% (10/10 runs passing)`
- **Flake Rate**: `0.0%`
- **Mean Duration**: `1.420s`
- **Median Duration**: `1.414s`
- **P95 Duration**: `1.479s`
- **Evidence Artifact**: `benchmarks/results/latest-reference.json`

### Command 3: Buggy Baseline Defect Detection
```bash
python benchmarks/runners/runner.py buggy
```
- **Exit Code**: `0`
- **Tasks**: 5
- **Detection Rate**: `100.0% (5/5 defects detected)`
- **Failure Breakdown**:
  - `cae-task-001-deadlock`: Deadlock detected on reciprocal transfers and self-transfers (4 failures).
  - `cae-task-002-sql-injection`: SQL injection detected via `' OR 1=1 --` and syntax crash on `O'Reilly` (4 failures).
  - `cae-task-003-async-leak`: Socket leak detected on mid-stream exception (3 failures, 3 teardown errors).
  - `cae-task-004-race-condition`: TOCTOU oversell detected; stock dropped to -13 (3 failures).
  - `cae-task-005-schema-migration`: KeyError detected on modern and legacy payloads (7 failures).
- **Evidence Artifact**: `benchmarks/results/latest-buggy.json`

### Command 4: Live Agent Evaluation Layer
```bash
python benchmarks/runners/agent_runner.py
```
- **Exit Code**: `0`
- **Status**: `AGENT_EVAL_SKIPPED`
- **Skip Reason**: `Codex CLI executable ('codex') not found in system PATH. Live agent evaluation requires OpenAI Codex CLI.`
- **Integrity Rule**: Per Rule #1 and Phase 14 instructions, zero-shot and agent comparison percentages are marked `AGENT_EVAL_SKIPPED` rather than fabricated from static reference files.
- **Evidence Artifact**: `benchmarks/results/runs/run-20260917-053405-f70ce3/metadata.json`

### Command 5: Skills Schema & Contract Validation
```bash
python scripts/validate_skills.py
```
- **Exit Code**: `0`
- **Result**: `9/9 skills pass CAE Quality Contract`
- **Verified Skills**:
  1. `code-review`: SKILL.md + review_diff.py + checklist.md + sample-output.md
  2. `debugging`: SKILL.md + repro_runner.py + checklist.md + sample-output.md
  3. `deep-research`: SKILL.md + verify_sources.py + checklist.md + sample-output.md
  4. `documentation`: SKILL.md + doc_lint.py + checklist.md + sample-output.md
  5. `implementation`: SKILL.md + check_diff_scope.py + checklist.md + sample-output.md
  6. `release-engineering`: SKILL.md + check_release_readiness.py + checklist.md + sample-output.md
  7. `repo-audit`: SKILL.md + audit_repo.py + checklist.md + sample-output.md
  8. `security-review`: SKILL.md + scan_secrets.py + checklist.md + sample-output.md
  9. `test-engineering`: SKILL.md + verify_test_coverage.py + checklist.md + sample-output.md

### Command 6: Skills Projection Synchronization
```bash
python scripts/check_skill_sync.py
```
- **Exit Code**: `0`
- **Result**: `All 9 canonical skills in skills/ match .agents/skills/ byte-for-byte`

### Command 7: Internal Markdown Link Resolution
```bash
python scripts/check_links.py
```
- **Exit Code**: `0`
- **Result**: `114 markdown files checked; 0 broken relative links`

### Command 8: Automated OSS Release Audit Gate
```bash
python scripts/oss_release_audit.py
```
- **Exit Code**: `0`
- **Result**: `OSS_RELEASE_STATUS = PASS (12/12 gates passed)`
- **Gates Verified**:
  - `license`: PASS (Valid MIT License)
  - `repository_metadata`: PASS (pyproject.toml package metadata)
  - `required_docs`: PASS (All 9 governance documents present)
  - `skills_integrity`: PASS (9/9 skills valid)
  - `skills_sync`: PASS (Projection synchronized)
  - `provenance_integrity`: PASS (11 records with verification_status and claim_scope)
  - `internal_links`: PASS (All markdown links resolve)
  - `ci_configuration`: PASS (Comprehensive CI matrix)
  - `benchmark_integrity`: PASS (All 5 tasks meet specification)
  - `secrets_scan`: PASS (Zero secrets or credentials found)
  - `benchmark_freshness`: PASS (Summary is fresh with provenance headers)
  - `unit_tests`: PASS (100% test suite passing)
- **Evidence Artifact**: `benchmarks/results/oss_release_audit.json`

---

## 3. Known Limitations & Boundary Disclaimers

1. **Codex CLI Availability**: Automated agent evaluation requires the user or runner environment to have the OpenAI Codex CLI installed. When absent, the framework cleanly marks agent evaluation as skipped.
2. **Language Scope**: Current deterministic tasks test Python failure modes; TypeScript and Rust benchmark tasks are scheduled for v0.2.0.
3. **Model Telemetry Variance**: Fine-grained token breakdown depends on model provider headers; Bedrock backends omit per-turn token logging without dedicated proxy instrumentation.
