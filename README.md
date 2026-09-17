# Codex Agent Engineering (CAE)

[![CI](https://github.com/priyanshupk2022-arch/codex-agent-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/priyanshupk2022-arch/codex-agent-engineering/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-%3E%3D0.145.0-blue)](compatibility/codex/0.145.x.md)
[![Reference Pass](https://img.shields.io/badge/CAE%20Reference%20Suite-100%25%20Passing-brightgreen)](benchmarks/README.md)
[![Bug Detection](https://img.shields.io/badge/Buggy%20Detection-100%25%20Verified-brightgreen)](benchmarks/README.md)
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
| **What you can use** | 9 production Skills (`skills/`), projected into `.agents/skills/`, 10 structured Workflows (`workflows/`), a reproducible 5-task Benchmark Suite (`benchmarks/`), multi-tier AGENTS.md templates (`templates/`), and the `cae` CLI. |
| **How to start** | Clone the repo, run `python scripts/cae_cli.py doctor`, and run the benchmark suite with `python scripts/cae_cli.py benchmark run`. |
| **Why it is different** | **Evidence-backed & Deterministic.** Every pattern is verified by an automated test or cited paper. Claims strictly reflect genuine execution; no synthetic benchmarks or fake agent runs are reported. |

---

## 2. Navigational Pathways

Choose the learning pathway tailored to your experience level and immediate goal:

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│   START HERE    │ ──> │   LEARN BY DOING     │ ──> │   REFERENCE DOCS     │ ──> │   BENCHMARKS       │
│  (Quick Setup)  │     │ (Hands-on Tutorials) │     │ (Architectural Deep) │     │ (Empirical Evid.)  │
│                 │     │                      │     │                      │     │                    │
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
- [Skill Contract: Codex-Native Layer vs CAE Quality Layer](docs/skills/contract.md)
- [Context Engineering & Anti-Compaction Defense](docs/context-engineering/index.md)
- [Spec-Driven Development (GitHub Spec Kit)](docs/fundamentals/spec-driven-development.md)
- [AI-Driven Development Lifecycle (AI-DLC)](docs/fundamentals/aidlc-lifecycle.md)
- [Coding-Agent Threat Modeling & Hardening](docs/security/index.md)
- [Multi-Agent Orchestration: Single First, Swarm Second](docs/orchestration/index.md)

### [Benchmarks & Evidence (Expert)](benchmarks/README.md)
- [CAE Benchmark Suite v1 Overview](benchmarks/README.md)
- [Benchmark Results: Verified Reference & Buggy Baselines](benchmarks/results/summary.md)
- [Empirical Evidence Ledger](BENCHMARK_EVIDENCE.md)
- [Empirical Experiments Registry](experiments/README.md)
- [Codex Compatibility Matrix](compatibility/README.md)
- [Real-World Case Studies](case-studies/01-legacy-repo-modernization.md)

### [Contribute](CONTRIBUTING.md)
- [Contribution Guidelines & Quality Gates](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Disclosure Policy](SECURITY.md)
- [Issue Templates & Workflows](.github/ISSUE_TEMPLATE/)

---

## 3. Engineering Rigor & Evidence Classification

In strict adherence to CAE honesty invariants, repository claims are classified across four tiers:

| Tier | Status | Scope & Proof |
| :--- | :--- | :--- |
| **WHAT IS VERIFIED** | **VERIFIED (100%)** | • 100% pass rate on the 5-task deterministic reference implementation suite.<br>• 100% bug detection rate across buggy baselines.<br>• 9/9 skills adhering to CAE Quality Contract (`validate_skills.py`).<br>• Zero secret leaks, zero unsafe shell executions, clean sandbox boundaries.<br>• 100% passing test suites across `tests/` and `examples/`. |
| **WHAT IS REPRODUCIBLE** | **REPRODUCIBLE** | • The complete benchmark suite (`benchmarks/runners/runner.py`) with `--iterations N` flakiness analysis.<br>• Automated report generation (`scripts/generate_benchmark_report.py`).<br>• Automated OSS release audit gate (`scripts/oss_release_audit.py`). |
| **WHAT IS EXPERIMENTAL** | **EXPERIMENTAL** | • Large-scale MCP server overloading (>8 servers, EXP-003).<br>• Cross-model backend compatibility with non-Codex engines (Claude Code, Gemini CLI). |
| **WHAT IS PLANNED** | **PLANNED (v0.2.0)** | • Live Codex agent runs in headless CI containers with automated token and latency telemetry.<br>• Expansion of benchmark tasks to TypeScript and Rust runtimes. |

---

## 4. How the Benchmark Actually Works

Unlike static puzzle benchmarks, the CAE evaluation framework runs a fair, double-track evaluation inside isolated temporary workspaces:

```
                  ┌─────────────────────────────────────┐
                  │          BENCHMARK TASK             │
                  │ (task.json, _buggy.py, test_*.py)   │
                  └──────────────────┬──────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
   ┌───────────────────────────┐           ┌───────────────────────────┐
   │    ISOLATED WORKSPACE     │           │    ISOLATED WORKSPACE     │
   │      (Vanilla Track)      │           │        (CAE Track)        │
   ├───────────────────────────┤           ├───────────────────────────┤
   │ • Task description        │           │ • Task description        │
   │ • Buggy target file       │           │ • Buggy target file       │
   │ • Test harness            │           │ • Test harness            │
   │ • Vanilla prompt          │           │ • CAE AGENTS.md rules     │
   │                           │           │ • Relevant CAE Skill      │
   └─────────────┬─────────────┘           └─────────────┬─────────────┘
                 │                                       │
                 ▼                                       ▼
   ┌───────────────────────────┐           ┌───────────────────────────┐
   │       VANILLA CODEX       │           │      CODEX + CAE AGENT    │
   │ (Single-turn prompt exec) │           │ (Evidence-driven repair)  │
   └─────────────┬─────────────┘           └─────────────┬─────────────┘
                 │                                       │
                 ▼                                       ▼
   ┌───────────────────────────┐           ┌───────────────────────────┐
   │       VERIFICATION        │           │       VERIFICATION        │
   │ • Pytest exit code & pass │           │ • Pytest exit code & pass │
   │ • Git diff & modified f.  │           │ • Git diff & modified f.  │
   │ • Execution time & stderr │           │ • Execution time & stderr │
   └─────────────┬─────────────┘           └─────────────┬─────────────┘
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                  ┌─────────────────────────────────────┐
                  │     EVIDENCE & METRIC ARTIFACTS     │
                  │ benchmarks/results/runs/<run_id>/   │
                  │ metadata.json, diff.patch, logs     │
                  └─────────────────────────────────────┘
```

### Deterministic Benchmark Status

| Task ID | Failure Domain | Buggy Baseline Detection | Golden Reference Result |
| :--- | :--- | :--- | :--- |
| **`cae-task-001-deadlock`** | Concurrency | **DETECTED** (Deadlock on reciprocal & self-transfers) | **PASS** (Hierarchy ordering fixed; 20 threads completed) |
| **`cae-task-002-sql-injection`** | Security | **DETECTED** (Syntax crash on `O'Reilly`; injection leak) | **PASS** (Parameterized query blocked SQLi, allowed apostrophes) |
| **`cae-task-003-async-leak`** | Reliability | **DETECTED** (Leaked socket on mid-stream exception) | **PASS** (Structured `try/finally` closed socket under error) |
| **`cae-task-004-race-condition`** | Concurrency | **DETECTED** (Oversold 38 units; stock dropped to -13) | **PASS** (Atomic transaction lock prevented overselling) |
| **`cae-task-005-schema-migration`**| Data Eng | **DETECTED** (KeyError crashed modern/legacy callers) | **PASS** (Dual-schema adapter parsed both old and new formats) |
| **Overall Summary** | **5 Core Tasks** | **100% Detection Rate (5/5)** | **100% Pass Rate (5/5)** |

> **Agent Evaluation Notice**: Live Vanilla vs CAE agent comparison results are **NOT YET ESTABLISHED** on systems lacking a local OpenAI Codex CLI installation. CAE never presents synthetic reference code as a "Codex result". Run `python benchmarks/runners/agent_runner.py` in an environment with the `codex` binary to generate live comparison artifacts.

---

## 5. The Reusable Skills Library

Canonical skills reside in `skills/` and are mirrored to `.agents/skills/` for Codex CLI compatibility. All skills adhere to the [CAE Skill Contract](docs/skills/contract.md):

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

## 6. Quickstart: Using the `cae` CLI

```bash
# 1. Clone repository
git clone https://github.com/priyanshupk2022-arch/codex-agent-engineering.git
cd codex-agent-engineering

# 2. Check repository health
python scripts/cae_cli.py doctor

# 3. List available benchmark tasks
python scripts/cae_cli.py benchmark list

# 4. Run reference benchmark suite
python scripts/cae_cli.py benchmark run --mode reference

# 5. Run full automated OSS release audit
python scripts/cae_cli.py audit
```

---

## 7. Provenance & Research Grounding

Every factual claim in this repository is tracked in [`sources/provenance.json`](sources/provenance.json). We strictly distinguish between:
- **Official OpenAI Specifications**: Verified against Codex CLI source code and documentation (`VERIFIED`).
- **Academic Research**: Grounded in peer-reviewed literature (e.g., *SWE-bench* [Jimenez et al.], *Reflexion* [Shinn et al.], *HumanEval* [Chen et al.]) (`VERIFIED`).
- **Controlled Experiments**: Recorded in [`experiments/registry/`](experiments/README.md) (`REPRODUCIBLE`).
- **Community Empirical Findings**: Clearly labeled qualitative field observations (`COMMUNITY_REPORTED`).

---

## 8. License & Governance

- Distributed under the **[MIT License](LICENSE)**.
- Contributions welcome! See **[CONTRIBUTING.md](CONTRIBUTING.md)**.
- Adheres to the **[Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md)**.
- Security disclosures: See **[SECURITY.md](SECURITY.md)**.
