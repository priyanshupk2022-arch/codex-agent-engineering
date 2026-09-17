# Workflow: Production Incident Debugging & Hotfix Workflow

## 1. Input Specification
Incident alert, error spikes, user impact summary, production logs, monitoring dashboards.

## 2. Context Ingestion
Recent deployments, production commit SHAs, database migration history, system architecture.

## 3. Ordered Actions
1. Impact Containment: Determine if immediate rollback or circuit breaking is required.
2. Telemetry Analysis: Correlate error spikes with timestamps, commit SHAs, or traffic surges.
3. Local Reproduction: Mirror production failure conditions in an isolated local test harness.
4. Surgical Hotfix: Implement minimal, low-risk fix addressing immediate failure mode.
5. Verification & Sanity Check: Validate hotfix against stress load locally.
6. Post-Mortem Documentation: Record incident timeline, root cause, short-term fix, and long-term prevention.

## 4. Required Tools & Surfaces
Log parsers, git log / diff, test runner, local stress test harness.

## 5. Constraints & Invariants
High urgency, minimal change footprint. No speculative refactoring or non-essential cleanup during incident response.

## 6. Output & Deliverables
Validated hotfix commit, reproduction test, and draft POST_MORTEM.md.

## 7. Verification Protocol
Hotfix passes local reproduction test under simulated load; zero unintended regressions.

## 8. Failure Handling & Recovery
If hotfix risk is high or root cause is ambiguous, advise immediate rollback to previous stable commit.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Never run unconstrained vanilla Codex during production incidents; structured verification prevents panic-induced bad commits.
