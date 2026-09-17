# CAE Benchmark Suite v1: Empirical Evaluation Summary

> **Evidence-Safe Report**: Generated automatically from machine-readable benchmark execution artifacts.

## 1. Environment & Provenance Metadata

- **Generated At**: `2026-09-17 06:10:42 UTC`
- **Git Commit SHA**: `10311efcf1664044878df8ed534fe2175f0aeda1`
- **Operating System**: `Windows 11`
- **Python Version**: `3.14.3`
- **Codex CLI**: `Not Installed (Local environment lacks 'codex' in PATH)`
- **Benchmark Version**: `1.0.0`
- **Evaluated Iterations**: `1`

---

## 2. Evaluation Tiers Summary

| Evaluation Layer | Status | Result / Detection Rate | Notes |
| :--- | :--- | :--- | :--- |
| **Reference Implementation Suite** | **VERIFIED** | **100.0% (5/5)** | 100% pass on current deterministic reference suite |
| **Buggy Defect Detection** | **VERIFIED** | **100.0% (5/5)** | 100% defect detection across buggy failure modes |
| **Agent Comparison (Vanilla vs CAE)** | **NOT YET ESTABLISHED** | **N/A (Requires Codex CLI)** | The local environment does not have the OpenAI Codex CLI installed. Per Rule #1, results are not fabricated. |

---

## 3. Reference Suite Latency & Flakiness Statistics

| Metric | Reference Suite | Buggy Baseline |
| :--- | :--- | :--- |
| **Pass Rate** | 100.0% | 0.0% |
| **Failure Rate** | 0.0% | 100.0% |
| **Flake Rate** | 0.0% | 0.0% |
| **Mean Duration** | 1.343s | 2.516s |
| **Median Duration** | 1.335s | 1.525s |
| **P95 Duration** | 1.373s | 6.593s |
| **Iterations** | 1 | 1 |

---

## 4. Detailed Task-by-Task Specification

### Task: `cae-task-001-deadlock` — Concurrency Lock Inversion Deadlock
- **Reference Execution**: PASS (1.363s)
- **Patch Status**: `CORRECT`
- **Deterministic Verification**: Verified against pytest harness with adversarial tests.

### Task: `cae-task-002-sql-injection` — SQL Injection in Product Search
- **Reference Execution**: PASS (1.323s)
- **Patch Status**: `CORRECT`
- **Deterministic Verification**: Verified against pytest harness with adversarial tests.

### Task: `cae-task-003-async-leak` — Unclosed Resource Leak in Async Stream
- **Reference Execution**: PASS (1.335s)
- **Patch Status**: `CORRECT`
- **Deterministic Verification**: Verified against pytest harness with adversarial tests.

### Task: `cae-task-004-race-condition` — Inventory Oversell Race Condition
- **Reference Execution**: PASS (1.373s)
- **Patch Status**: `CORRECT`
- **Deterministic Verification**: Verified against pytest harness with adversarial tests.

### Task: `cae-task-005-schema-migration` — Backward-Compatible Schema Parser
- **Reference Execution**: PASS (1.322s)
- **Patch Status**: `CORRECT`
- **Deterministic Verification**: Verified against pytest harness with adversarial tests.

---

## 5. Reproduction Instructions

To independently reproduce these benchmark figures on your local machine:

```bash
# 1. Run the verified reference suite
python benchmarks/runners/runner.py reference

# 2. Run the buggy baseline detection suite
python benchmarks/runners/runner.py buggy

# 3. Re-generate this summary report directly from executable code
python scripts/generate_benchmark_report.py
```
