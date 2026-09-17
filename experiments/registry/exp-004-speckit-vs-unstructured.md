# Experiment EXP-004: GitHub Spec Kit SDD vs Unstructured Prompting

- **Status**: `SUPPORTED`
- **Date**: 2026-09-17
- **Model / Harness**: Codex CLI with Spec Kit integration

---

## 1. Hypothesis
Using GitHub Spec Kit (`$speckit-specify` -> `$speckit-tasks` -> `$speckit-implement`) eliminates scope creep and reduces line diff churn by >= 40% compared to ad-hoc conversational prompting.

## 2. Results
- Across 15 feature requests, SDD workflows produced an average of 42 lines of code diff with 100% test coverage.
- Conversational prompting produced an average of 98 lines of diff, including 28 lines of unnecessary refactoring in unrelated helper files.

## 3. Conclusion
Spec-Driven Development enforces boundary discipline and preserves repository stability.
