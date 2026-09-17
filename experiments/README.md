# Codex Agent Engineering Experiment Framework

Empirical investigation is essential to separate software engineering discipline from prompt folklore. Every experiment in this registry adheres to a strict scientific methodology:

```
Hypothesis ──> Method ──> Baseline ──> Intervention ──> Measurements ──> Result ──> Limitations ──> Conclusion
```

## Result Classifications
- **`SUPPORTED`**: Hypothesis verified with statistically significant or deterministic data across >= 10 trials.
- **`PROMISING`**: Hypothesis indicates positive directional trend but requires larger sample size or multi-model replication.
- **`INCONCLUSIVE`**: Variance across runs exceeds signal; confounding variables identified.
- **`FAILED`**: Hypothesis disproven; intervention caused regression or no measurable improvement.

## Registry Index
- [`EXP-001: AGENTS.md Token Budget vs Instruction Retention`](registry/exp-001-agents-md-token-budget.md) (`SUPPORTED`)
- [`EXP-002: Approval Policy Friction & Rubber-Stamping Fatigue`](registry/exp-002-approval-policy-friction.md) (`SUPPORTED`)
- [`EXP-003: MCP Tool Count vs Agent Tool Hallucination`](registry/exp-003-mcp-context-overload.md) (`PROMISING`)
- [`EXP-004: GitHub Spec Kit SDD vs Unstructured Prompting`](registry/exp-004-speckit-vs-unstructured.md) (`SUPPORTED`)
