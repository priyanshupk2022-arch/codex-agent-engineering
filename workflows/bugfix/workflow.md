# Workflow: Bugfix & Root-Cause Remediation Workflow

## 1. Input Specification
Bug report, error log, stack trace, and reproduction environment details.

## 2. Context Ingestion
Faulty module source code, recent git commit history (git log -n 5), test configurations.

## 3. Ordered Actions
1. Triage: Parse error logs and identify failure conditions.
2. Reproduction Test: Author a deterministic failing test reproducing the exact failure.
3. Root Cause Isolation: Trace data flow to locate logical defect or race condition.
4. Minimal Patch: Apply surgical fix addressing the root defect.
5. Regression Run: Run full repository test suite to guarantee zero collateral damage.
6. Commit: Author conventional commit message: 'fix(scope): describe defect and root cause'.

## 4. Required Tools & Surfaces
Git bisect, debugger/test runner, surgical editor, log inspector.

## 5. Constraints & Invariants
Never mask bugs with catch-all exceptions or increased timeouts. Do not modify existing test assertions.

## 6. Output & Deliverables
Minimal patch, new regression test case, Root Cause Analysis (RCA) note.

## 7. Verification Protocol
Reproduction test fails on unpatched code and passes on patched code; full suite passes.

## 8. Failure Handling & Recovery
If patch causes secondary test failures, analyze shared state dependencies and re-evaluate solution bounds.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: For simple typos or obvious syntax errors, a single vanilla Codex prompt is sufficient without a formal reproduction harness.
