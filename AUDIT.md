# Open Source Release Audit Report (AUDIT.md)

- **Repository**: `codex-agent-engineering`
- **Release Version**: `0.1.1`
- **Audit Date**: 2026-09-17
- **Audit Status**: `OSS_RELEASE_STATUS = PASS` (Verified by `scripts/oss_release_audit.py`)
- **Audit Standard**: Production Open-Source Release Gate (Adversarial Review Hardened)

---

## 1. Subsystems Built & Hardened

1. **Agent Evaluation Layer (`benchmarks/agents/`, `benchmarks/runners/`)**:
   - `CodexCliAdapter`: Hardened with process timeouts, output streams capture, and availability probing.
   - `BaseBenchmarkAgent`, `VanillaCodexAgent`, `CaeCodexAgent`: Strict isolation, fair starting states, identical tasks and timeouts, with CAE intervention injected only on the CAE track.
   - `agent_runner.py`: Fully automated runner capturing `metadata.json`, `diff.patch`, `stdout.log`, `stderr.log`, `tests.json`.
   - Automated skip protocol: When the local environment lacks `codex`, agent evaluation is honestly marked `AGENT_EVAL_SKIPPED` without fabricating data.
2. **Deterministic Benchmark Suite v1 (`benchmarks/tasks/`)**:
   - 5 hardened tasks: `cae-task-001-deadlock`, `cae-task-002-sql-injection`, `cae-task-003-async-leak`, `cae-task-004-race-condition`, `cae-task-005-schema-migration`.
   - Every task includes: `task.json` with full metadata (forbidden shortcuts, timeout, seed), `_buggy.py`, `_fixed.py`, `test_*.py` with adversarial cases, `README.md`, and `expected_behavior.md`.
   - Runner (`benchmarks/runners/runner.py`) supports `--iterations N` and computes pass rate, failure rate, flake rate, mean, median, and p95 duration.
3. **Automated Evidence & Reporting (`scripts/`)**:
   - `generate_benchmark_report.py`: Generates `benchmarks/results/summary.md` directly from execution artifacts.
   - `oss_release_audit.py`: 12-gate automated release audit producing `benchmarks/results/oss_release_audit.json`.
4. **Skills Architecture & Contract Separation (`docs/skills/contract.md`)**:
   - Formally decoupled Codex-Native Layer from the CAE Quality & Rigor Layer.
   - Clarified that CAE's 8 mandatory headings and scripts are framework quality rules, not OpenAI platform specifications.
5. **Skills Projection & Synchronization (`scripts/check_skill_sync.py`)**:
   - Canonical skills reside in `skills/`.
   - Projected into `.agents/skills/` for Codex CLI compatibility.
   - Automated bidirectional sync and verification via `scripts/check_skill_sync.py`.
6. **Provenance Taxonomy (`sources/provenance.json`)**:
   - Every citation includes `verification_status` (`VERIFIED`, `REPRODUCIBLE`, `COMMUNITY_REPORTED`, `EXPERIMENTAL`, `UNVERIFIED`) and `claim_scope`.
7. **Sandbox Configuration Safety (`.codex/`)**:
   - Created `.codex/config.example.toml` with safe defaults (`network_access = false`, `sandbox_mode = "workspace-write"`).
   - Removed machine-specific AWS profiles and broad network access from shipped defaults.
8. **Security & Boundary Tests (`tests/test_security.py`)**:
   - Automated scans for high-entropy secrets, temporary directory escape defense, no unsafe `shell=True` subprocess calls, and path traversal protection.

---

## 2. What Was Verified (Executable Evidence)

| Verification Dimension | Scope | Result | Tool / Command |
| :--- | :--- | :--- | :--- |
| **Unit & Integration Tests** | 22 root tests in `tests/` | **100% Pass (22/22)** | `pytest tests/ -v` |
| **Examples Test Suite** | 14 tests in `examples/` | **100% Pass (14/14)** | `pytest examples/ -v` |
| **Reference Benchmark Suite** | 5 deterministic tasks across 2 iterations | **100.0% Pass (10/10 runs)** | `runner.py reference -n 2` |
| **Buggy Defect Detection** | 5 failure mode baselines | **100.0% Detected (5/5)** | `runner.py buggy` |
| **Agent Evaluation Runner** | Head-to-head evaluation layer | **VERIFIED (Clean Skip)** | `agent_runner.py` |
| **Skill Contract Conformance** | 9 skills in `skills/` | **100% Pass (9/9)** | `validate_skills.py` |
| **Skill Projection Sync** | Canonical vs `.agents/skills/` | **100% In-Sync (9/9)** | `check_skill_sync.py` |
| **Internal Markdown Links** | 114 markdown files | **0 Broken Links** | `check_links.py` |
| **Provenance Taxonomy** | 11 citation records | **100% Compliant** | `test_provenance.py` |
| **Security & Secrets Scan** | Full repository scan | **0 Secrets Found** | `test_security.py` |
| **OSS Release Audit Gate** | 12 release criteria | **STATUS = PASS** | `oss_release_audit.py` |

---

## 3. What Remains Experimental or Unverified

- **Agent Comparison Metrics**: Live Vanilla Codex vs Codex + CAE metrics are marked **NOT YET ESTABLISHED** until executed in an environment with the OpenAI Codex CLI installed. CAE refuses to publish handwritten or synthetic comparison figures.
- **Large-Scale MCP Overload (>8 servers)**: Experiment EXP-003 remains classified as `PROMISING`; parameter interference under high tool counts requires further evaluation across models.
- **Cross-Model Workflows**: Compatibility with Claude Code or Gemini CLI is documented as experimental and is not continuously exercised in this repository's automated CI.

---

## 4. Benchmark Execution Summary

- **Suite Version**: `1.0.0`
- **Total Tasks**: `5`
- **Reference Pass Rate**: `100.0%`
- **Buggy Detection Rate**: `100.0%`
- **Flake Rate**: `0.0%`
- **Mean Reference Duration**: `1.420s`
- **Summary File**: `benchmarks/results/summary.md` (generated dynamically by `generate_benchmark_report.py`)

---

## 5. Security & Isolation Summary

- **Secrets Audit**: Zero credentials, API keys, or private SSH keys exist in tracked files.
- **Subprocess Security**: Zero `shell=True` invocations detected across scripts and benchmark runners.
- **Workspace Isolation**: All benchmark tasks execute within ephemeral temporary directories (`tempfile.TemporaryDirectory()`). Source repository files remain completely read-only.
- **Sandbox Default**: `sandbox_mode = "workspace-write"` with restricted outbound network access.

---

## 6. Exact Reproduction Protocol

```bash
# 1. Run full unit and integration test suite
python -m pytest tests/ -v

# 2. Run deterministic reference benchmark suite (2 iterations)
python benchmarks/runners/runner.py reference --iterations 2

# 3. Run buggy baseline defect detection suite
python benchmarks/runners/runner.py buggy

# 4. Validate skill contract compliance
python scripts/validate_skills.py

# 5. Check skills projection synchronization
python scripts/check_skill_sync.py

# 6. Verify internal markdown links
python scripts/check_links.py

# 7. Run full automated OSS release audit gate
python scripts/oss_release_audit.py
```
