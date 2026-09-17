# Case Study 01: Modernizing a Legacy Monolith with Zero Test Coverage

## 1. Problem Description and Initial State
A mission-critical subscription billing microservice (`acme-billing`, 14,200 lines of Python 2.7/3.6 hybrid code) processed $4.8M monthly recurring revenue across 48 unversioned REST endpoints. 

The service suffered from acute architectural decay:
- **Zero Automated Test Coverage**: No unit, integration, or contract test suites existed. Verification historically relied on manual Postman runs by billing operations.
- **Python 2 Legacy Idioms**: Pervasive use of `six`, `urllib2`, `__builtin__`, and raw SQL queries formatted with `%` string interpolation.
- **Subtle Decimal Rounding Invariants**: Currency calculations mixed standard floating-point arithmetic with bespoke fixed-point helpers that implemented banker's rounding (`ROUND_HALF_EVEN`) inconsistently across payment providers.
- **Upgrade Blocker**: Enterprise infrastructure mandates required migration to Python 3.12 within 30 days due to CVE vulnerabilities in base container images.

## 2. The Naive Approach
An engineering team tasked an unconstrained Codex agent with a single monolithic prompt:
```text
"Upgrade this entire repository to Python 3.12. Remove all deprecated six/urllib2 dependencies, replace custom SQL formatting with SQLAlchemy ORM, and write a full pytest suite with 90% coverage."
```

The agent was given `danger-full-access` mode with no phased checkpoints, no specification guardrails, and no intermediate testing harness.

## 3. Failure Mode Analysis
The naive execution collapsed across multiple failure axes:
1. **Context Window Saturation & File Hallucination**: The agent modified 45 files in a single pass. By file 28, it lost track of shared database session patterns defined in `db_engine.py` and hallucinated competing transaction lifecycle models in downstream routes.
2. **Circular Self-Validating Tests**: Because no pre-existing tests defined ground truth, the agent wrote pytest suites that asserted its *modified* behaviors rather than the original business invariants. Tests passed locally while silently introducing catastrophic logic shifts.
3. **Rounding & Currency Drift**: The agent replaced the bespoke `money_math.py` module with Python's standard `round()` function. In Python 3, `round(2.5)` rounds to 2 (even), whereas the legacy helper had a bug where negative values rounded toward zero. While fixing the bug seemed clean, it silently broke reconciliations for 18,000 active credit card charge cycles.
4. **Blast Radius Explosion**: The single 3,800-line diff proved unreviewable by human maintainers, requiring an emergency rollback after 4 hours of staging failure triage.

## 4. The Revised Workflow
The team restructured the engagement using the Codex Agent Engineering framework, pairing GitHub Spec Kit (`specify`) for behavioral specification with AI-DLC (`aidlc`) for staged execution:

```
[Phase 1: repo-audit] ──> [Phase 2: specify (Invariants)] ──> [Phase 3: test-engineering (Golden Master)]
                                                                           │
                                                                           ▼
[Phase 6: release] <── [Phase 5: code-review] <── [Phase 4: Atomic Refactoring (Walking Skeleton)]
```

- **Stage 1 (Audit)**: Invoked `skills/repo-audit` to map the 48 route handlers, external dependencies, and state boundaries into an explicit dependency matrix.
- **Stage 2 (Specification)**: Used GitHub Spec Kit (`.specify/`) to generate a formal behavioral contract (`specs/billing-invariants.md`) detailing tax rules, decimal rounding modes, and idempotency guarantees.
- **Stage 3 (Characterization Testing)**: Invoked `skills/test-engineering` to capture 500 recorded historical HTTP payloads as black-box golden master regression fixtures *before* touching application code.
- **Stage 4 (Atomic Migration)**: Partitioned the upgrade into 14 scoped units, enforced by `skills/implementation/scripts/check_diff_scope.py` (max 5 files and 300 LOC per step).

## 5. Step-by-Step Implementation Walkthrough
1. **Golden Master Harness Creation**:
   - Recorded live database transaction snapshots from the staging replica.
   - Authored `tests/characterization/test_golden_billing.py` executing 100% of routes against captured fixtures using pytest and `responses`.
2. **Foundational Modernization**:
   - Migrated core typing and runtime dependencies: eliminated `six`, upgraded `setup.py` to `pyproject.toml` targeting Python 3.12.
   - Enforced CI execution with Python 3.12; characterization tests initially failed on syntax errors.
3. **Surgical Math & Currency Alignment**:
   - Modernized `money_math.py` to use `decimal.Decimal` with explicit `ROUND_HALF_EVEN` context.
   - Ran `test_golden_billing.py` to verify that 100% of historical test fixtures produced exact bit-for-bit penny parity.
4. **Endpoint Modernization via Walking Skeleton**:
   - Migrated endpoints in priority clusters (1: Health & Ping, 2: Customer Read, 3: Invoice Calculations, 4: Charge Processing).
   - Replaced raw SQL strings with parameterized queries while preserving exact JSON response envelopes.
5. **Quality Gate Verification**:
   - Evaluated each stage with `skills/code-review` and `skills/security-review`.

## 6. Verification and Test Results
The migration achieved full verification across all production dimensions:
- **Test Suite Growth**: From 0 tests to 142 unit tests, 48 contract tests, and 500 characterization replays.
- **Ledger Invariant Verification**: Replayed $14.2M in historical invoice calculations across 10,000 synthetic transaction permutations with 0 cent deviation.
- **CI Performance**: Entire test suite runs in 42.6 seconds under pytest on GitHub Actions.
- **Production Staging Trial**: Deployed to staging running in parallel with production (shadow traffic mode) for 7 days; 0 discrepancies logged across 124,000 API requests.

## 7. Benchmark Comparison: Naive vs Structured Workflow

| Evaluation Dimension | Naive Single-Prompt Codex | CAE Structured Workflow (Spec Kit + AI-DLC) | Delta / Impact |
| :--- | :--- | :--- | :--- |
| **End-to-End Success Rate** | 0% (Staging failure, unmergeable) | 100% (Production deployed) | **Complete Resolution** |
| **Files Modified Per Commit** | 45 files (unreviewable mega-diff) | 3.2 files average (14 atomic commits) | **-93% blast radius** |
| **Regressed Endpoints** | 19 / 48 endpoints broken | 0 / 48 endpoints broken | **Zero regressions** |
| **Token Consumption** | 185,000 tokens (exhaustion loops) | 78,000 tokens (staged sessions) | **-58% token overhead** |
| **Human Review Time** | 14 hours (aborted triage) | 45 minutes (staged PR approvals) | **18.6x faster review** |
| **Financial Parity** | Failed (Rounding drift detected) | Bit-identical penny accuracy ($0 error) | **100% financial safety** |

## 8. Key Lessons and Reusable Rules for AGENTS.md

### Rule 1: Characterization Gate Before Code Modification
> **MANDATE**: When touching legacy or untested codebases, NEVER modify application code until a characterization test suite captures current runtime behavior. Tests written after or during refactoring will inherit the agent's hallucinations.

### Rule 2: Bound PR Scope to Micro-Batches
> **ENFORCEMENT**: Configure agent tasks with maximum change boundaries:
> ```ini
> MAX_FILES_PER_DIFF=5
> MAX_LINES_PER_DIFF=300
> ```
> Multi-file refactors must be split into dependency order (Domain Types -> Core Engine -> Service Handlers -> Route Controllers).

### Rule 3: Spec-Backed Invariant Checking
> **SPECIFICATION**: For business-critical logic (financials, authorization, state transitions), generate explicit invariants via GitHub Spec Kit (`.specify/`) and make every agent pass an invariant assertion check prior to review submission.
