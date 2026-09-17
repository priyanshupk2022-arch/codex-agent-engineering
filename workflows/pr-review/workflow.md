# Workflow: Pull Request Review & Verification Workflow

## 1. Input Specification
Pull request URL, git diff, target branch comparison.

## 2. Context Ingestion
Repository conventions, architectural guidelines, CI status, linked issues.

## 3. Ordered Actions
1. Context Fetching: Fetch PR diff, commit messages, and linked issue requirements.
2. Automated Test Validation: Run test suite against the PR branch to verify claims independently.
3. Multi-Axis Code Audit: Review diff across Correctness, Security, Performance, Cleanliness, and Architecture.
4. Edge Case Check: Identify overlooked error handling or boundary failures.
5. Constructive Review Report: Produce structured markdown comment with clear categorization (Blocking vs Non-Blocking).

## 4. Required Tools & Surfaces
Git diff, gh cli, test runner, linter/type-checker.

## 5. Constraints & Invariants
Objective, courteous, evidence-backed. Point to concrete line numbers. Do not approve without test proof.

## 6. Output & Deliverables
PR_REVIEW_COMMENT.md ready for posting on GitHub PR.

## 7. Verification Protocol
Every issue raised corresponds to a real defect or verifiable violation of repository standards.

## 8. Failure Handling & Recovery
If PR diff is too large (>500 lines), request author split into smaller logical PRs before completing review.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex often gives overly agreeable reviews ('Looks great!'); PR review workflow enforces strict adversarial checks.
