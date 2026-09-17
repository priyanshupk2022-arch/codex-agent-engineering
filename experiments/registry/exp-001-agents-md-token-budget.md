# Experiment EXP-001: AGENTS.md Token Budget vs Instruction Retention

- **Status**: `SUPPORTED`
- **Date**: 2026-09-17
- **Model / Harness**: Codex CLI >= 0.145.0 (GPT-5 class reasoning model)
- **Author**: Codex Agent Engineering Research Group

---

## 1. Hypothesis
Restricting the root `AGENTS.md` file to <= 1,500 tokens (focusing strictly on non-negotiable build/test invariants) will increase agent adherence to project testing rules in multi-turn sessions by >= 30% compared to a monolithic 4,500-token `AGENTS.md`.

## 2. Method
- **Dataset**: 20 simulated refactoring tasks across 5 repositories.
- **Trial Count**: 40 total executions (20 baseline, 20 intervention).
- **Metric**: `Instruction Adherence Rate` (percentage of runs where the agent executed the mandatory test command before declaring task complete).

## 3. Baseline vs Intervention
- **Baseline**: Monolithic `AGENTS.md` (4,480 tokens) containing architectural philosophy, detailed coding examples, deployment runbooks, and test commands.
- **Intervention**: Lean `AGENTS.md` (1,150 tokens) containing only build/test commands, invariants, and directory pointers, with procedural runbooks offloaded to on-demand Skills.

## 4. Measurements & Results
| Metric | Monolithic Baseline | Lean Intervention | Delta |
| :--- | :--- | :--- | :--- |
| Test Command Execution Rate | 65.0% (13/20) | 95.0% (19/20) | **+30.0%** |
| Average Session Token Overhead | 4,480 tokens/turn | 1,150 tokens/turn | **-74.3%** |
| Unrelated File Edits (Scope Creep) | 4 runs (20%) | 1 run (5%) | **-15.0%** |

## 5. Limitations
Evaluated primarily on Python and TypeScript repositories. Monorepos with >10 nested packages were not tested in this phase.

## 6. Conclusion
Excessive prose in root `AGENTS.md` dilutes model attention. Offloading procedural runbooks to Skills and keeping `AGENTS.md` strictly bounded directly increases agent compliance.
