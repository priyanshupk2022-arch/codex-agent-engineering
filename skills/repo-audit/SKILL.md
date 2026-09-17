# Skill: repo-audit

## Overview
Systematic structural, architectural, and security audit of an unfamiliar repository.

## When to Use
When first onboarding into a new codebase, before major refactoring, or during quarterly hygiene reviews.

## Inputs
Target repository path, optional focus areas (e.g. security, performance, dependencies).

## Workflow
1. Structural Reconnaissance: Run git status, inspect directory tree depth, identify language runtimes and build configs.
2. Architecture Mapping: Discover entry points, route handlers, data models, and dependency graphs.
3. Quality & Test Audit: Inspect test suites, coverage reports, linters, and CI workflows.
4. Security & Hygiene Check: Scan for hardcoded credentials, unpinned dependencies, outdated packages, and missing licenses.
5. Synthesis & Reporting: Generate structured markdown AUDIT_REPORT.md with prioritized remediation items.

## Outputs & Deliverables
Comprehensive AUDIT_REPORT.md with executive summary, topography map, risk register, and action plan.

## Constraints & Guardrails
Strictly read-only; no code or configuration changes. Do not execute untrusted binaries or install arbitrary packages.

## Verification Protocol
All reported file paths and line numbers must exist and be verifiable via git or ls. Risk ratings must cite CWE or CVE when applicable.

## Common Failure Modes & Recovery
Incomplete repo scan due to excessive size -> remedy by applying file exclusions (.git, vendor, node_modules) and chunking by subsystem.
