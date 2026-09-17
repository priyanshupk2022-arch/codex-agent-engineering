# AI-Driven Development Life Cycle (AI-DLC) on Codex CLI

AI-DLC provides an institutional, enterprise-grade development lifecycle engine for autonomous coding agents, featuring strict approval gates, immutable audit logging, and automated sensor verification.

---

## 1. The Four Core Phases

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  INCEPTION  │ ───> │  IDEATION   │ ───> │ CONSTRUCTION │ ───> │  OPERATION  │
└─────────────┘      └─────────────┘      └──────────────┘      └─────────────┘
```

1. **Inception**:
   - Defines intent, feasibility, domain boundaries, and team roles.
   - Outputs: `intent.md`, `feasibility.md`, `team.md`.
2. **Ideation**:
   - Captures user stories, functional design, non-functional requirements (NFRs), and contract design.
   - Outputs: `user-stories.md`, `contract-design.md`, `nfr-requirements.md`.
3. **Construction**:
   - Breaks work into testable units, generates code, and runs regression suites.
   - Verification: `sensor-type-check`, `sensor-linter`, `sensor-traceability`.
4. **Operation**:
   - Manages deployment planning, CI pipeline configuration, and observability instrumentation.

---

## 2. Sensors & Automated Quality Gates

AI-DLC deploys automated sensors that must pass before an agent can transition between stages:
- **`sensor-claim-sources`**: Ensures all requirements trace back to confirmed source interviews or documentation.
- **`sensor-traceability`**: Verifies 100% upstream and downstream mapping in `traceability.json`.
- **`sensor-required-sections`**: Enforces strict markdown document structure.
- **`sensor-type-check` & `sensor-linter`**: Executes static analysis before human approval handoff.
