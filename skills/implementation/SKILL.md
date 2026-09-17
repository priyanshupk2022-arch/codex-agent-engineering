# Skill: implementation

## Overview
Atomic, test-driven code implementation adhering to minimal diff principles.

## When to Use
When implementing a planned feature, bug fix, or interface contract.

## Inputs
Task specification, acceptance criteria, target files, existing test suites.

## Workflow
1. Baseline Verification: Run existing test suites to confirm green baseline before making edits.
2. Interface Contract Scaffolding: Define types, interfaces, and function signatures.
3. Test-First Authoring: Write unit tests expressing the acceptance criteria.
4. Minimal Diff Implementation: Write the smallest contiguous code block that satisfies tests.
5. Local Verification: Execute test suite and linter; inspect git diff for accidental modifications.

## Outputs & Deliverables
Clean, tested code diffs and passing test results.

## Constraints & Guardrails
Do not touch files outside task scope. Do not reformat unrelated lines. Maintain backward compatibility unless breaking change is explicitly specified.

## Verification Protocol
100% pass rate on new and existing test suites; static analysis (mypy/tsc/ruff) exits 0 with zero new warnings.

## Common Failure Modes & Recovery
Cascading type errors or broken downstream tests -> roll back to clean git state and re-evaluate interface boundaries.
