# Workflow: Test Engineering & Coverage Hardening Workflow

## 1. Input Specification
Target module or package, coverage goals, known flaky test list.

## 2. Context Ingestion
Module source code, existing tests, mock frameworks, CI execution logs.

## 3. Ordered Actions
1. Coverage Analysis: Run pytest-cov / c8 to identify untested critical paths and branches.
2. Boundary Exploration: Define edge-case inputs: nulls, zero lengths, maximum integer values, unicode characters.
3. Parametric Test Authoring: Implement table-driven tests for high test density.
4. Concurrency & Stress Testing: Add multi-threaded or async race condition tests.
5. Flakiness Verification: Execute test suite across 10-20 iterations to detect intermittent timing issues.

## 4. Required Tools & Surfaces
Pytest / Jest, coverage profiler, stress runner, mock libraries.

## 5. Constraints & Invariants
Tests must be completely deterministic and run without internet connectivity. No tautological assertions.

## 6. Output & Deliverables
New test files, updated test fixtures, improved coverage metrics.

## 7. Verification Protocol
Coverage target achieved; zero flaky tests detected across repeated runs.

## 8. Failure Handling & Recovery
If a test flakes, isolate whether issue is timing, unclosed state, or global variable pollution.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex frequently writes shallow tests asserting trivial assertions; testing workflow enforces boundary matrices and stress loops.
