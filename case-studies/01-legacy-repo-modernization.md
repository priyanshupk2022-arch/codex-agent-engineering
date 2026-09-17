# Case Study 01: Modernizing a Legacy Monolith with Zero Test Coverage

## 1. Problem
A 10-year-old billing microservice (14,000 lines of Python 2.7/3.6 hybrid code) had zero automated tests, 48 undocumented endpoints, and accumulated technical debt that prevented Python 3.12 migration.

## 2. The Naive Approach
A prompt-only agent was instructed: *"Upgrade this entire repository to Python 3.12 and add pytest tests."*

## 3. Failure Mode
The agent attempted to rewrite 20 files simultaneously, replaced custom date parsers with incompatible standard library calls, broke undocumented edge cases in currency conversion, and failed because there were no tests to confirm whether its changes were correct.

## 4. Revised CAE Workflow
1. **Repository Audit**: Executed `repo-audit` to catalog all route handlers and generate a dependency map.
2. **Spec-First Invariant Definition**: Used `$speckit-specify` to formalize billing calculation invariants (e.g. half-even rounding, exact cent precision).
3. **Characterization Testing**: Used `test-engineering` to write black-box regression tests against existing live responses *before* touching application code.
4. **Atomic Refactoring**: Used `refactor` workflow to migrate modules one by one, executing the test suite at every atomic commit.

## 5. Outcome & Lessons
- Successfully upgraded to Python 3.12 across 14 atomic commits.
- Zero accounting discrepancies observed in staging verification.
- **Core Lesson**: Never allow an agent to refactor un-tested code. Write characterization tests first.
