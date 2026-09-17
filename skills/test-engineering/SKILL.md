# Skill: test-engineering

## Overview
Comprehensive test suite design covering unit, integration, property, and stress testing.

## When to Use
When hardening critical modules, testing edge cases, or improving test coverage.

## Inputs
Target module source code, specification, edge-case requirements.

## Workflow
1. Boundary Analysis: Identify input domain boundaries, null cases, empty collections, and extreme values.
2. Invariant Definition: Formulate properties that must hold across all valid inputs.
3. Test Authoring: Implement unit tests, parametric test tables, and integration mocks.
4. Edge Case Hardening: Add concurrency, timeout, and fault-injection test cases.
5. Coverage & Flakiness Audit: Run tests repeatedly (e.g. 10x) to ensure zero flakiness.

## Outputs & Deliverables
Hardened test files, fixtures, and coverage report.

## Constraints & Guardrails
Tests must be deterministic and self-contained; no reliance on unseeded randomness or external live network services.

## Verification Protocol
All tests pass reliably across repeated runs; code coverage increases without asserting tautologies.

## Common Failure Modes & Recovery
Flaky timing tests -> replace arbitrary sleep() calls with condition polling and async synchronization primitives.
