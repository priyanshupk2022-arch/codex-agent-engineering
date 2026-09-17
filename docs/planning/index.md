# Planning & Task Breakdown Architecture

A plan is an executable specification of work. In Codex Agent Engineering, planning is strictly separated from code generation to prevent premature convergence and unconstrained diffs.

---

## 1. The Spec-First Planning Pipeline

```
Raw User Request
       │
       ▼
Clarification & Ambiguity Elimination (Eliminate guesswork)
       │
       ▼
Invariant Definition (What must NEVER break)
       │
       ▼
Atomic Task Decomposition (Units < 50 lines of diff)
       │
       ▼
Verification Harness Definition (How each unit is tested)
```

---

## 2. Invariant-Driven Design

Before generating any code, declare **System Invariants**:
- *Data Invariant*: Database schema backwards compatibility (no destructive column drops without deprecation windows).
- *Security Invariant*: Authentication must be checked before authorization; all external inputs must be validated with Pydantic/Zod schemas.
- *Performance Invariant*: No N+1 queries; all network calls must have explicit timeouts.
- *Testing Invariant*: Test coverage must not decrease; existing regression suites must pass.

---

## 3. Atomic Task Sizing

Tasks assigned to coding agents should satisfy the **Single-Concern Principle**:
- Modifies at most 2-3 tightly coupled files.
- Accompanied by a dedicated test verifying the change.
- Can be independently committed, reverted, or reviewed.
