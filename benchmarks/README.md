# Codex Agent Engineering (CAE) Benchmark Suite v1

A deterministic, reproducible benchmark framework designed to evaluate coding agents on real-world engineering failures: **concurrency deadlocks, SQL injection, async resource leaks, race conditions, and schema migration regressions.**

---

## 1. Why Existing Benchmarks Are Insufficient
General coding benchmarks (like HumanEval) test isolated synthetic functions. Even SWE-bench, while groundbreaking, focuses primarily on general Python issues where test execution and environment setup can take hours.

**CAE Benchmarks** test specific architectural and reliability failure modes:
1. Concurrency and Deadlock Prevention.
2. Security Vulnerabilities and Injection Defense without Breaking Legitimate Inputs.
3. Resource Lifecycle Leaks (Async I/O and Sockets).
4. Critical Race Conditions under Multi-Threaded Stress.
5. Backward-Compatible API and Schema Evolutions.

---

## 2. Benchmark Tasks Overview

| Task ID | Domain | Challenge | Pass Condition |
| :--- | :--- | :--- | :--- |
| **`cae-task-001-deadlock`** | Concurrency | Cross-account fund transfer lock inversion. | 20 concurrent threads complete transfers without deadlock. |
| **`cae-task-002-sql-injection`** | Security | Unescaped SQL search string concatenation. | Blocks `' OR 1=1 --` injection while allowing `'` in legitimate searches (e.g., `O'Reilly`). |
| **`cae-task-003-async-leak`** | Reliability | Unclosed async resource handle during stream exception. | `MockResource.active_instances == 0` even when exceptions abort streaming. |
| **`cae-task-004-race-condition`** | Concurrency | Non-atomic inventory read-modify-write. | 50 concurrent orders do not oversell initial stock of 20. |
| **`cae-task-005-schema-migration`** | Data Eng | Upgrading `full_name` to `first_name`/`last_name`. | Seamlessly parses both legacy and new payloads while raising on missing fields. |

---

## 3. Running the Benchmark

```bash
# Run the reference suite (Golden implementations)
python benchmarks/runners/runner.py reference

# Run the buggy baseline (Verifying tests catch the bugs)
python benchmarks/runners/runner.py buggy

# Run via CAE CLI
python scripts/cae_cli.py benchmark run
```
