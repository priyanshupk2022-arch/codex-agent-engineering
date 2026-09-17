# Release Engineering & Version Management

Releasing software authored or maintained with agent assistance requires rigorous validation gates and automated provenance tracking.

---

## 1. Release Verification Pipeline

Before cutting a release tag:
1. **Clean Working Tree**: No uncommitted changes or untracked artifacts.
2. **Full Test Suite (Exit 0)**: All unit, integration, and regression suites pass.
3. **Link & Documentation Integrity**: All internal and external links resolve.
4. **Security Scan**: Zero known critical vulnerabilities in dependencies.
5. **Changelog Validation**: Release notes accurately reflect conventional commits.

---

## 2. Semantic Versioning Standards

- `MAJOR` (v1.0.0): Incompatible API or workflow breaking changes.
- `MINOR` (v0.1.0): Backward-compatible new features, skills, or benchmarks.
- `PATCH` (v0.0.1): Backward-compatible bug fixes and documentation updates.
