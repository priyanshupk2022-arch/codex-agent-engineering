# Skill: code-review

## Overview
Rigorous multi-axis audit of pull requests or proposed diffs.

## When to Use
Before merging any pull request or committing major agent-generated changes.

## Inputs
Git diff or pull request branch, commit messages, design specification.

## Workflow
1. Diff Scope Inspection: Check for scope creep, accidental file modifications, or debug artifacts.
2. Correctness & Edge-Case Analysis: Verify logic against edge cases, boundary conditions, and concurrency hazards.
3. Security & Dependency Audit: Inspect inputs for sanitization, auth validation, and dependency safety.
4. Performance & Resource Check: Identify algorithmic inefficiencies, unclosed handles, and memory leaks.
5. Synthesis & Feedback: Issue structured review report with blocking items vs non-blocking suggestions.

## Outputs & Deliverables
REVIEW_REPORT.md with categorized findings (Fatal, Major, Minor, Nit) and actionable remediation steps.

## Constraints & Guardrails
Objective and evidence-based. Cite exact file and line numbers. Do not offer generic subjective praise.

## Verification Protocol
Every cited issue must correspond to a verifiable defect in the diff.

## Common Failure Modes & Recovery
Superficial review missing subtle logic bugs -> apply adversarial mental execution and trace data flow step-by-step.
