# Workflow: Release Engineering & Distribution Workflow

## 1. Input Specification
Target release version, branch to release (e.g. main), release notes template.

## 2. Context Ingestion
Commit history since last release tag, package manifests, CI/CD deployment configs.

## 3. Ordered Actions
1. Pre-Flight Verification: Verify branch is clean, CI is green, and all tests pass locally.
2. Version Bump: Update version string across all project manifests (pyproject.toml, package.json, etc.).
3. Changelog Generation: Extract conventional commits and synthesize categorized CHANGELOG.md.
4. Build Distribution Artifacts: Build wheel, sdist, or container image and verify file contents.
5. Release Tagging: Create signed git release tag.
6. Post-Release Verification: Verify newly tagged release can be installed and executed from scratch.

## 4. Required Tools & Surfaces
Git, package build tools (build/npm pack), changelog generator, test runner.

## 5. Constraints & Invariants
Never release from a dirty working tree or failing test suite. Strictly adhere to SemVer.

## 6. Output & Deliverables
Updated CHANGELOG.md, version commit, git tag, verified build artifacts.

## 7. Verification Protocol
Build artifact installs cleanly in a fresh isolated virtual environment; smoke tests pass.

## 8. Failure Handling & Recovery
If release verification fails, abort release process before pushing tag to remote.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex cannot safely manage releases due to missing cryptographic tagging and multi-step artifact verification.
