# Skill: debugging

## Overview
Systematic root-cause diagnosis and remediation of software failures.

## When to Use
When encountering broken tests, runtime crashes, memory leaks, or concurrency bugs.

## Inputs
Failure symptom, stack trace, error logs, and minimal reproduction steps.

## Workflow
1. Deterministic Reproduction: Create minimal automated test reproducing the exact failure.
2. Execution Path Tracing: Trace variables, call stacks, and async execution order leading to the failure point.
3. Root Cause Identification: Distinguish underlying design flaw from surface symptoms.
4. Remediation: Apply minimal, targeted fix addressing the root cause.
5. Regression Proof: Verify reproduction test passes and full test suite passes.

## Outputs & Deliverables
Remediation patch, regression test case, and Root Cause Analysis (RCA) note.

## Constraints & Guardrails
Never suppress errors with blanket try/except or timeouts. Never alter test assertions merely to make them pass.

## Verification Protocol
Reproduction test fails before fix and passes after fix; full regression suite exits with code 0.

## Common Failure Modes & Recovery
Heisenbugs / intermittent concurrency failures -> isolate timing dependencies with stress runners or simulated latency.
