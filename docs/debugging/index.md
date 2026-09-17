# Systematic Root-Cause Debugging

Guessing is banned. In Codex Agent Engineering, debugging follows a deterministic four-phase triangulation loop inspired by the **Reflexion** framework.

---

## 1. The 4-Phase Triangulation Loop

```
Phase 1: REPRODUCE (Create minimal reproducible test case)
           │
           ▼
Phase 2: ISOLATE (Trace exact failure boundary via logs/stack traces)
           │
           ▼
Phase 3: HYPOTHESIZE & FIX (Address the underlying root cause, not symptoms)
           │
           ▼
Phase 4: REGRESSION TEST (Verify fix passes and existing tests remain green)
```

---

## 2. Root Cause vs Symptom Patching

| Anti-Pattern (Symptom Patching) | Correct Engineering (Root-Cause Fix) |
| :--- | :--- |
| Wrapping a failing block in `try: ... except Exception: pass` | Diagnosing why `None` was passed and handling the null state explicitly. |
| Increasing a timeout from 5s to 30s to pass a flaky test | Identifying resource contention, deadlocks, or missing async awaits. |
| Hardcoding expected values in test assertions to match incorrect output | Fixing the calculation logic in the core service. |
| Deleting or skipping a failing test | Investigating the behavioral regression the test caught. |

---

## 3. Deterministic Reproduction Protocol

Before touching implementation code:
1. Write a standalone reproduction script or a failing unit test.
2. Run the test to confirm it fails with the exact reported error.
3. Apply the minimal fix.
4. Re-run the test to confirm it now passes (Exit code 0).
5. Run the entire test suite to guarantee zero collateral damage.
