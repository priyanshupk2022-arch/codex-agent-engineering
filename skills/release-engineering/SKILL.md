# Skill: release-engineering

## Overview
Production release preparation, changelog compilation, and deployment readiness verification.

## When to Use
When preparing a tagged release, publishing a package, or promoting code to production.

## Inputs
Commit history since last release, target version bump (patch/minor/major), release checklist.

## Workflow
1. Working Tree Sanitization: Verify git working directory is clean with zero uncommitted changes.
2. Full Quality Gate Execution: Run full test suite, linter, type-check, and documentation link checks.
3. Changelog Compilation: Parse conventional commit messages and generate categorized CHANGELOG.md entry.
4. Version Bump & Tagging: Update version in metadata files (package.json, pyproject.toml) and prepare release tag.
5. Release Artifact Verification: Build distribution packages (wheel, tarball) and verify manifest completeness.

## Outputs & Deliverables
Updated CHANGELOG.md, version bump commit, release notes, and verified release artifacts.

## Constraints & Guardrails
Never publish or tag on a broken build. Enforce semantic versioning rules strictly.

## Verification Protocol
All release gates exit 0; clean build artifacts can be imported and executed in fresh environment.

## Common Failure Modes & Recovery
Missing files in release archive -> check MANIFEST.in or package.json files array; test install from built artifact.
