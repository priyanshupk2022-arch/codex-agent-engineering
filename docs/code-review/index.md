# Multi-Axis Automated Code Review

Automated code review provides independent verification before code merges into protected branches. CAE establishes a 5-axis review framework.

---

## 1. The 5 Review Axes

1. **Correctness & Logic**:
   - Does the implementation solve the stated problem?
   - Are edge cases (empty lists, negative numbers, null values) handled?
   - Are concurrency primitives thread-safe / async-safe?

2. **Security & Data Safety**:
   - Are user inputs sanitized?
   - Is authentication/authorization strictly enforced?
   - Are secrets or sensitive data exposed in logs or diffs?

3. **Performance & Resource Hygiene**:
   - Does this introduce quadratic or cubic algorithmic complexity?
   - Are database queries indexed and bounded?
   - Are network connections pooled and timed out?

4. **Maintainability & Cleanliness**:
   - Does it adhere to project conventions?
   - Is documentation updated to reflect interface changes?
   - Is dead or commented-out code eliminated?

5. **Architectural Coherence**:
   - Does this violate module boundaries or create circular dependencies?
   - Is this the smallest appropriate change?
