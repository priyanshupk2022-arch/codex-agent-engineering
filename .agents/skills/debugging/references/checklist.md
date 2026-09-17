# debugging Checklist & Root Cause Analysis Protocol

## Phase 1: Symptom Capture & Isolation
- [ ] Record exact error message, stack trace, exit code, and environment variables.
- [ ] Determine whether bug is deterministic, intermittent (race condition), or environmental.
- [ ] Check recent commit logs (`git log -n 10 --oneline`) to identify potential regressors.
- [ ] Formulate minimal reproduction command using `repro_runner.py`.

## Phase 2: Root Cause Hypothesis & Tracing
- [ ] Formulate testable hypothesis: "Under condition X, component Y fails because of Z."
- [ ] Inspect relevant source files without modifying code yet.
- [ ] Trace state transitions leading up to the failure point.
- [ ] For concurrency issues: map lock acquisition ordering and shared mutable state.
- [ ] For async issues: check unawaited coroutines, event loop starvation, or unclosed resources.

## Phase 3: Minimal Reproduction Test
- [ ] Author an isolated characterization test that deterministically reproduces the failure.
- [ ] Verify test fails against current buggy code (exit code non-zero).
- [ ] Confirm failure reason in test log matches the reported production symptom.

## Phase 4: Root Cause Remediation
- [ ] Implement the narrowest surgical fix that addresses the root cause directly.
- [ ] Avoid superficial symptom masking (e.g. adding `time.sleep()`, swallowing exceptions, or catching broad `Exception`).
- [ ] Verify the minimal reproduction test now passes (exit code 0).

## Phase 5: Regression & Side-Effect Verification
- [ ] Run `repro_runner.py` for 10 iterations to confirm resolution is robust and non-flaky.
- [ ] Run the full existing test suite to ensure no regressions were introduced.
- [ ] Document findings in Root Cause Analysis (RCA) post-mortem.
