# Spec-Driven Development (SDD) with GitHub Spec Kit

Spec-Driven Development (SDD) inverts the standard coding agent workflow: **Specification precedes Implementation, and Invariants precede Code.**

Using the GitHub Spec Kit (`specify`), agents operate against explicit, structured contracts rather than ambiguous conversational requests.

---

## 1. The SDD Lifecycle

```
$speckit-constitution ──> $speckit-specify ──> $speckit-plan ──> $speckit-tasks ──> $speckit-implement ──> $speckit-converge
      (Principles)             (Spec)              (Plan)           (Breakdown)        (Execution)           (Verification)
```

1. **Constitution (`$speckit-constitution`)**: Declares project-wide architectural laws, tech stack constraints, and coding standards.
2. **Specification (`$speckit-specify`)**: Generates unambiguous functional specs with user stories and acceptance criteria.
3. **Plan (`$speckit-plan`)**: Creates architectural blueprints, dependency maps, and risk assessments.
4. **Tasks (`$speckit-tasks`)**: Breaks plans into atomic, verifiable implementation steps.
5. **Implement (`$speckit-implement`)**: Executes tasks step-by-step with automated verification.
6. **Converge (`$speckit-converge`)**: Assesses current repository state against the initial specification and reports deltas.

---

## 2. Why SDD is Critical for Codex Agents
Without structured specs, agents suffer from:
- **Scope Creep**: Implementing unnecessary abstractions or refactoring unrelated files.
- **Premature Convergence**: Declaring a task "complete" because the happy path works, while edge cases fail.
- **Context Drift**: Forgetting earlier requirements after multiple turns of debugging.
