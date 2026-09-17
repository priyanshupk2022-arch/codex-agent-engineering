# AGENTS.md Template for Production Repositories

This file provides persistent context and strict invariants for OpenAI Codex CLI and compatible coding agents.

## 1. Project Invariants
- **Primary Tech Stack**: [e.g. Python 3.12+, FastAPI, SQLAlchemy, PostgreSQL]
- **Package Manager**: [e.g. poetry / uv / pip / npm / pnpm]
- **Execution Sandbox**: Always assume `workspace-write` sandbox; no outbound network calls allowed in unit tests.

## 2. Essential Commands
- **Install Dependencies**: `[e.g. pip install -e ".[dev]" / npm install]`
- **Run Test Suite**: `[e.g. pytest tests/ -q / npm test]`
- **Run Single Test**: `[e.g. pytest tests/test_auth.py -k "test_login" -q]`
- **Run Type Checker**: `[e.g. mypy src/ tests/ / npx tsc --noEmit]`
- **Run Linter / Formatter**: `[e.g. ruff check . / npm run lint]`

## 3. Implementation Rules
1. **Minimal Diffs**: Touch only files required for the task. Do not reformat unrelated code.
2. **Test First**: Write failing tests before applying implementation changes.
3. **Zero Regressions**: All tests must pass before declaring work complete.
4. **No Destructive Operations**: Never run `git push --force`, `rm -rf`, or drop database tables without explicit authorization.

## 4. Directory Topography
- `src/`: Core application logic
- `tests/`: Automated test suites
- `docs/`: Architecture documentation and ADRs
