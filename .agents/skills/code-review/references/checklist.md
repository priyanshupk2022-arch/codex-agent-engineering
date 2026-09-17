# code-review Checklist & Multi-Axis Evaluation Protocol

## Axis 1: Correctness & Logic
- [ ] Does the implementation fulfill all requirements specified in the design / spec?
- [ ] Are all edge cases handled (empty collections, null values, negative numbers, boundary limits)?
- [ ] Are off-by-one errors eliminated in loops, slices, and index arithmetic?
- [ ] Are return types and exception types consistent with the rest of the codebase?

## Axis 2: Security & Defensiveness
- [ ] Are user inputs properly validated, parameterized, or sanitized?
- [ ] Are secrets, credentials, and API keys strictly managed via environment variables?
- [ ] Are execution sandboxes and approval boundaries respected?
- [ ] Are exceptions caught specifically rather than swallowed by broad `except Exception:`?

## Axis 3: Concurrency & Performance
- [ ] Are locks acquired in consistent order to prevent deadlocks?
- [ ] Are database queries indexed and free of N+1 query patterns?
- [ ] Are async coroutines awaited properly without blocking the event loop?
- [ ] Are resources (files, sockets, database sessions) closed safely in `finally:` blocks?

## Axis 4: Test Coverage & Verification
- [ ] Does the pull request include automated tests for new or modified behavior?
- [ ] Do tests assert specific outcomes rather than merely testing that code runs without crash?
- [ ] Does the full repository test suite pass locally?

## Axis 5: Maintainability & Clean Code
- [ ] Are functions short, focused, and single-purpose?
- [ ] Are variable and function names self-documenting?
- [ ] Is commented-out code, temporary debug logging, and dead code removed?
