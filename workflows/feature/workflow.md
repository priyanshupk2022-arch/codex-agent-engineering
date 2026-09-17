# Workflow: Feature Implementation Workflow

## 1. Input Specification
Feature specification, acceptance criteria, wireframes or API schemas.

## 2. Context Ingestion
Relevant domain models, route handlers, existing test fixtures, database migration status.

## 3. Ordered Actions
1. Scaffold Spec: Generate feature specification and task breakdown using GitHub Spec Kit ($speckit-specify, $speckit-tasks).
2. Interface Contract Design: Define Pydantic/TypeScript schemas and function signatures.
3. Test Authoring: Write failing integration and unit tests covering positive and negative paths.
4. Core Implementation: Implement business logic in minimal, reviewable units (<50 lines diff per step).
5. Static Analysis & Lint: Run linter, type-checker, and formatting tools.
6. Integration Verification: Execute end-to-end and regression test suites.
7. Documentation Update: Update API documentation and user guides to reflect feature.

## 4. Required Tools & Surfaces
Terminal shell, file editor (surgical replace), test runner (pytest/jest), type checker (mypy/tsc).

## 5. Constraints & Invariants
Do not touch unrelated modules. Do not introduce unapproved third-party dependencies. Zero test regressions allowed.

## 6. Output & Deliverables
Tested, documented feature commit or pull request with full test evidence.

## 7. Verification Protocol
100% test pass rate on new tests; zero regressions on existing suites; linter/type-check exit 0.

## 8. Failure Handling & Recovery
If integration test fails, trace error to root cause. If architectural issue, revert to clean git state and refine spec.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: For small, single-file additive features (<20 lines), vanilla Codex interactive prompt is faster and avoids specification overhead.
