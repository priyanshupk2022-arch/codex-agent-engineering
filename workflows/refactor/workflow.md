# Workflow: Large Refactor & Modernization Workflow

## 1. Input Specification
Refactoring goal (e.g. migrate from callback to async, decouple monolithic module), target boundaries.

## 2. Context Ingestion
Complete subsystem dependency graph, test coverage reports, public API contracts.

## 3. Ordered Actions
1. Invariant Locking: Ensure extensive test coverage exists over the target subsystem before modifying code.
2. Interface Extraction: Introduce abstract interfaces or adapter wrappers to preserve existing call sites.
3. Incremental Migration: Migrate internal implementation in atomic, bisectable commits.
4. Deprecation & Cleanup: Remove obsolete code paths after all callers are verified.
5. Benchmark Verification: Verify performance metrics (memory, latency) did not degrade.

## 4. Required Tools & Surfaces
AST search tools, language server / type checker, regression test runner, benchmark suite.

## 5. Constraints & Invariants
Zero functional changes during refactoring; behavior must remain identical. Public APIs must remain backward compatible.

## 6. Output & Deliverables
Clean refactored codebase with improved maintainability and identical behavioral contracts.

## 7. Verification Protocol
All existing test suites pass without modification; zero breaking changes to public exports.

## 8. Failure Handling & Recovery
If regression occurs during multi-step refactoring, use git bisect to isolate the exact commit causing divergence.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Never use vanilla Codex for large multi-file refactors; unconstrained edits will inevitably introduce subtle behavioral drift.
