# CAE Skill Architecture & Contract Specification

This document establishes the formal separation between the **Codex-Native Skill Interface** and the **CAE Quality & Verification Layer**.

---

## 1. Architectural Separation

In standard agent development, native platform discovery rules are frequently conflated with framework-level quality standards. We strictly decouple these two concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                 CODEX-NATIVE SKILL LAYER                    │
│  (Platform Discovery, Prompt Injection, Basic Conventions)  │
│                                                             │
│  • Directory: skills/<name>/ or .agents/skills/<name>/     │
│  • SKILL.md: Core instruction prompt file                   │
│  • Optional folders: scripts/, references/, examples/       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAE QUALITY & RIGOR LAYER                 │
│  (Deterministic Gates, Executable Tooling, Completeness)    │
│                                                             │
│  • 8 Mandatory Architectural Headings                       │
│  • Executable Python verification script (scripts/*.py)     │
│  • Operative checklist (>200 bytes in references/)          │
│  • Realistic sample output (>200 bytes in examples/)        │
│  • Automated CI schema enforcement (validate_skills.py)    │
└─────────────────────────────────────────────────────────────┘
```

> **Important Boundary Clarification**: The OpenAI Codex platform requires only a discoverable `SKILL.md` instruction file. The additional requirements enforced by `scripts/validate_skills.py` represent the **CAE Quality Standard** to ensure production reliability, not an upstream OpenAI specification.

---

## 2. Layer 1: Codex-Native Interface

Every skill must be compatible with OpenAI Codex skill discovery:

- **Naming**: Lowercase alphanumeric with hyphens (e.g. `repo-audit`, `security-review`).
- **Location**:
  - `skills/<name>/`: Canonical source repository for CAE reusable skills.
  - `.agents/skills/<name>/`: Projected location recognized by Codex and AI-DLC tooling.
- **Entrypoint**: `SKILL.md` containing natural language directives for the model.
- **Support Directories**:
  - `scripts/`: Optional utility scripts or automation entry points.
  - `references/`: Optional context documents, checklists, or API schemas.
  - `examples/`: Optional few-shot demonstrations and sample outputs.

---

## 3. Layer 2: CAE Quality & Verification Contract

To prevent generic or degraded prompt packages, every canonical skill in `skills/` must satisfy the CAE Quality Contract:

### 3.1 Required Headings in `SKILL.md`
Every `SKILL.md` must contain the following 8 exact Markdown headings:
1. `## Overview`: Executive summary of purpose and technical domain.
2. `## When to Use`: Precise activation triggers and operational conditions.
3. `## Inputs`: Mandatory parameters, file paths, and environment state.
4. `## Workflow`: Ordered, step-by-step procedures the agent must execute.
5. `## Outputs & Deliverables`: Explicit files, reports, or artifacts created.
6. `## Constraints & Guardrails`: Non-negotiable boundaries, prohibited shortcuts, and isolation limits.
7. `## Verification Protocol`: Mechanical, test-driven validation commands.
8. `## Common Failure Modes & Recovery`: Triage procedures for edge cases and breakdowns.

### 3.2 Executable Automation Script
Every skill must provide at least one runnable Python script in `skills/<name>/scripts/<script>.py`:
- Must execute cleanly without unhandled syntax or runtime errors.
- Must accept `--help` or standard arguments.
- Must provide meaningful exit codes (`0` on success, non-zero on failure).

### 3.3 Operative Reference Checklist
Every skill must provide `skills/<name>/references/checklist.md`:
- Must exceed 200 bytes of concrete, non-trivial verification gates.
- Must define phase-by-phase criteria before advancing.

### 3.4 Authentic Sample Output
Every skill must provide `skills/<name>/examples/sample-output.md`:
- Must exceed 200 bytes of realistic output artifacts.
- Demonstrates expected formatting, density, and evidence structure.

---

## 4. Automated Compliance Verification

CAE skills are verified automatically via `scripts/validate_skills.py`:

```bash
python scripts/validate_skills.py
```

Any skill failing any of the contract invariants will block CI and release gates.
