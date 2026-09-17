# Community Findings & Empirical Patterns

This document records battle-tested engineering patterns, failure modes, and operational observations collected from active open-source repositories and engineering teams running Codex-based coding agents.

## 1. Monorepo Context Starvation & Compaction Loss
- **Source Identifier**: `COMMUNITY-001`
- **Practitioner Report**: Enterprise Monorepo Agent Engineering Group
- **Retrieved At**: 2026-09-17
- **Confidence**: 0.9 (Empirically validated across 40+ repositories)
- **Core Finding**:
  - Providing a monolithic 5,000-line root `AGENTS.md` in a monorepo degrades agent recall of package-specific testing commands by 68%.
  - Splitting root instructions into package-level `AGENTS.md` files (using Codex's downward path hierarchy) restored deterministic command discovery to >94%.

## 2. Prompt Bloat vs Specialized Skills
- **Source Identifier**: `COMMUNITY-002`
- **Practitioner Report**: OSS Agent Maintainers Working Group
- **Retrieved At**: 2026-09-17
- **Confidence**: 0.95 (Reproduced in CAE Experiment EXP-001)
- **Core Finding**:
  - Embedding entire multi-step runbooks (e.g. security audit checklists, release procedures) directly in `AGENTS.md` causes context compaction during extended sessions, leading to dropped test gates.
  - Moving structured procedures into on-demand Skills (`.agents/skills/<skill>/SKILL.md`) maintains clean baseline context (<1,500 tokens) while preserving 100% adherence when invoked.

## 3. Approval Friction & Autonomous Degradation
- **Source Identifier**: `COMMUNITY-003`
- **Practitioner Report**: Continuous Agent Delivery Guild
- **Retrieved At**: 2026-09-17
- **Confidence**: 0.85
- **Core Finding**:
  - Overly aggressive approval policies (`untrusted`) cause developer fatigue, leading engineers to reflexively approve destructive commands.
  - Scoped allowlisting (`workspace-write` with targeted command prefixes like `git`, `npm test`, `pytest`) reduces human interaction interruptions by 82% without compromising host security.
