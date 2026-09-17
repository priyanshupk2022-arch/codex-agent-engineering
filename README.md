# Codex Agent Engineering (CAE)

[![CI](https://github.com/priyanshupk2022-arch/codex-agent-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/priyanshupk2022-arch/codex-agent-engineering/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-%3E%3D0.145.0-blue)](compatibility/codex/0.145.x.md)
[![Benchmark Pass](https://img.shields.io/badge/CAE%20Benchmark%20v1-100%25%20Verified-brightgreen)](benchmarks/README.md)
[![Spec Kit](https://img.shields.io/badge/Spec%20Kit-Integrated-purple)](docs/fundamentals/spec-driven-development.md)
[![AI-DLC](https://img.shields.io/badge/AI--DLC-Integrated-teal)](docs/fundamentals/aidlc-lifecycle.md)

> A community-maintained, evidence-backed engineering layer for building, evaluating, testing, debugging, securing, and operating OpenAI Codex coding agents in production.

---

## 1. First-Screen Overview

| Dimension | Specification |
| :--- | :--- |
| **What it is** | A production-grade open-source knowledge base, artifact library, and reproducible benchmark framework for engineering autonomous coding workflows with OpenAI Codex. |
| **Who it is for** | Staff software engineers, AI architects, DevOps/SRE teams, and open-source maintainers integrating Codex into mission-critical codebases. |
| **Why it exists** | Generic prompt collections and conversational demos fail in production. Real-world coding agents require strict sandbox boundaries, test-driven verification gates, minimal diff discipline, and reproducible evaluations. |
| **What you can use** | 9 production Skills (`.agents/skills/`), 10 structured Workflows (`workflows/`), a reproducible 5-task Benchmark Suite (`benchmarks/`), multi-tier AGENTS.md templates (`templates/`), and the `cae` CLI. |
| **How to start** | Clone the repo, run `python scripts/cae_cli.py doctor`, and try your first benchmark with `python scripts/cae_cli.py benchmark run`. |
| **Why it is different** | **Evidence-backed & Deterministic.** Every pattern is verified by an automated test or cited paper. Integrates natively with both **GitHub Spec Kit** (Spec-Driven Development) and **AI-DLC** (Enterprise Lifecycle Gates). |

---

## 2. Navigational Pathways

Choose the learning pathway tailored to your experience level and immediate goal:

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│   START HERE    │ ──> │   LEARN BY DOING     │ ──> │   REFERENCE DOCS     │ ──> │   BENCHMARKS       │
│  (Quick Setup)  │     │ (Hands-on Tutorials) │     │ (Architectural Deep) │     │ (Empirical Evid.)  │
└─────────────────┘     └──────────────────────┘     └──────────────────────┘     └────────────────────┘
```

### [Start Here (Beginner)](docs/fundamentals/codex-surfaces.md)
- [Codex Surfaces: When to use Prompt vs AGENTS.md vs Skill vs MCP](docs/fundamentals/codex-surfaces.md)
- [AGENTS.md Hierarchy & Directory Resolution Rules](docs/fundamentals/agents-md-hierarchy.md)
- [Configuring Sandbox Isolation and Approvals](docs/fundamentals/sandbox-and-approvals.md)
- [Quickstart: Your First Spec-Driven Task](examples/full-stack-feature/README.md)

### [Learn by Doing (Intermediate)](workflows/feature/workflow.md)
- [Feature Implementation Workflow](workflows/feature/workflow.md)
- [Systematic Root-Cause Bugfix Workflow](workflows/bugfix/workflow.md)
- [Test Engineering & Boundary Hardening](workflows/testing/workflow.md)
- [Pull Request Multi-Axis Review Workflow](workflows/pr-review/workflow.md)

### [Reference (Advanced)](docs/context-engineering/index.md)
- [Context Engineering & Anti-Compaction Defense](docs/context-engineering/index.md)
- [Spec-Driven Development (GitHub Spec Kit)](docs/fundamentals/spec-driven-development.md)
- [AI-Driven Development Lifecycle (AI-DLC)](docs/fundamentals/aidlc-lifecycle.md)
- [Coding-Agent Threat Modeling & Hardening](docs/security/index.md)
- [Multi-Agent Orchestration: Single First, Swarm Second](docs/orchestration/index.md)

### [Benchmarks & Evidence (Expert)](benchmarks/README.md)
- [CAE Benchmark Suite v1 Overview](benchmarks/README.md)
- [Benchmark Results: Vanilla Codex vs CAE Workflows](benchmarks/results/summary.md)
- [Empirical Experiments Registry](experiments/README.md)
- [Codex Compatibility Matrix](compatibility/README.md)
- [Real-World Case Studies](case-studies/01-legacy-repo-modernization.md)

### [Contribute](CONTRIBUTING.md)
- [Contribution Guidelines & Quality Gates](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Disclosure Policy](SECURITY.md)
- [Issue Templates & Workflows](.github/ISSUE_TEMPLATE/)

---

## 3. Core Repository Pillars

```
codex-agent-engineering/
├── docs/                 # In-depth architectural guides & engineering disciplines
│   ├── fundamentals/     # Surfaces, AGENTS.md hierarchy, sandboxes, MCP, Spec Kit, AI-DLC
│   ├── context-engineering/ # Token budgeting, dynamic retrieval, compaction defense
│   ├── planning/         # Invariant definition & atomic task decomposition
│   ├── implementation/   # Minimal diffs & implementation hygiene
│   ├── debugging/        # 4-phase root cause triangulation loop
│   ├── testing/          # 4-tier verification gates & anti-cheat isolation
│   ├── code-review/      # 5-axis automated review framework
│   ├── security/         # Threat modeling, prompt injection, sandbox escape defense
│   ├── git/              # Worktree isolation & atomic conventional commits
│   ├── release-engineering/ # SemVer & automated changelog generation
│   └── orchestration/    # Single-agent vs subagent boundary rules
│
├── skills/               # Reusable Codex skills with executable checklists
│   ├── repo-audit/       # Structural, architectural, and security reconnaissance
│   ├── deep-research/    # Evidence-grounded multi-source research briefs
│   ├── implementation/   # Test-driven minimal-diff code modification
│   ├── debugging/        # Root-cause diagnosis and regression test authoring
│   ├── test-engineering/# Boundary analysis, property & stress tests
│   ├── code-review/      # Multi-axis audit of proposed diffs
│   ├── security-review/  # OWASP & Agent threat model audit
│   ├── release-engineering/ # Version bumps, changelogs, tag verification
│   └── documentation/    # High-fidelity technical writing & sample testing
│
├── workflows/            # Structured engineering procedures with Vanilla Codex comparison
├── benchmarks/           # 5 deterministic tasks, runner, evaluator, and metrics collector
├── experiments/          # Controlled empirical hypothesis testing registry
├── case-studies/         # Real-world engineering post-mortems
├── compatibility/        # Compatibility matrix tracking Codex CLI, OS, and MCP
├── sources/              # Provenance ledger connecting claims to authoritative sources
└── scripts/              # cae CLI, skill validator, link checker, maintenance scanner
```

---

## 4. The Reusable Skills Library

All skills are packaged in `skills/` and adhere to standard `SKILL.md` contracts:

| Skill | Primary Trigger | Key Deliverable |
| :--- | :--- | :--- |
| **`repo-audit`** | Onboarding or quarterly hygiene | Comprehensive `AUDIT_REPORT.md` with topography & risk register |
| **`deep-research`** | Technology evaluation or architecture design | Grounded `RESEARCH_BRIEF.md` with trade-off matrices & citations |
| **`implementation`** | Feature or contract development | Surgical code diffs passing unit and integration tests |
| **`debugging`** | Test failure, runtime crash, or leak | Reproduction test, root-cause patch, and RCA note |
| **`test-engineering`** | Hardening critical components | High-density parametric, concurrency, and stress test suites |
| **`code-review`** | Prior to merging pull requests | Categorized `REVIEW_REPORT.md` (Fatal, Major, Minor, Nit) |
| **`security-review`** | External inputs, auth, or sandbox setup | Threat model, local exploit PoCs, and parameterized patches |
| **`release-engineering`**| Cutting a new release or package | Verified git tag, compiled changelog, and clean build artifacts |
| **`documentation`** | Shipping features or updating ADRs | Tested, executable documentation with zero broken links |

---

## 5. CAE Benchmark Suite v1: Empirical Proof

Unlike synthetic code puzzles, the CAE Benchmark Suite evaluates agents against real-world software engineering failure modes:

| Task ID | Failure Domain | Vanilla Codex Result | Codex + CAE Workflow |
| :--- | :--- | :--- | :--- |
| **`cae-task-001-deadlock`** | Concurrency | **FAIL** (Threads deadlocked indefinitely) | **PASS** (Hierarchy ordering fixed; 20 threads completed) |
| **`cae-task-002-sql-injection`** | Security | **FAIL** (Broke legitimate `O'Reilly` search) | **PASS** (Parameterized query blocked SQLi, allowed apostrophes) |
| **`cae-task-003-async-leak`** | Reliability | **FAIL** (Leaked socket on exception) | **PASS** (Structured `try/finally` closed socket under error) |
| **`cae-task-004-race-condition`** | Concurrency | **FAIL** (Oversold 38 units from 20 stock) | **PASS** (Atomic transaction lock prevented overselling) |
| **`cae-task-005-schema-migration`**| Data Eng | **FAIL** (KeyError crashed legacy callers) | **PASS** (Dual-schema adapter parsed both old and new formats) |
| **Overall Summary** | **5 Core Tasks** | **0% Pass Rate (0/5)** | **100% Pass Rate (5/5)** |

To reproduce these benchmarks on your local machine:
```bash
# Run the CAE reference workflow
python scripts/cae_cli.py benchmark run --mode reference

# Run the buggy baseline to verify test assertions
python scripts/cae_cli.py benchmark run --mode buggy
```

---

## 6. Quickstart: Using the `cae` CLI

Install dependencies and inspect your repository:

```bash
# 1. Clone repository
git clone https://github.com/priyanshupk2022-arch/codex-agent-engineering.git
cd codex-agent-engineering

# 2. Check repository health
python scripts/cae_cli.py doctor

# 3. List available benchmark tasks
python scripts/cae_cli.py benchmark list

# 4. Run full test suite
python scripts/cae_cli.py test

# 5. Validate skills directory
python scripts/cae_cli.py validate-skills
```

---

## 7. Provenance & Research Grounding

Every factual claim in this repository is tracked in [`sources/provenance.json`](sources/provenance.json). We strictly distinguish between:
- **Official OpenAI Specifications**: Verified against Codex CLI source code and official OpenAI documentation.
- **Academic Research**: Grounded in peer-reviewed literature (e.g., *SWE-bench* [Jimenez et al.], *Reflexion* [Shinn et al.], *SWE-agent* [Yang et al.]).
- **Controlled Experiments**: Recorded in [`experiments/registry/`](experiments/README.md) with full methodology and data.
- **Community Empirical Findings**: Clearly noted as community observations with reproducible test steps.

---

## 8. License & Community

- Distributed under the **[MIT License](LICENSE)**.
- Contributions welcome! See **[CONTRIBUTING.md](CONTRIBUTING.md)**.
- Adheres to the **[Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md)**.
