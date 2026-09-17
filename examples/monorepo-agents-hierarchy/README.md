# Example: Monorepo AGENTS.md Hierarchy & Precedence

This example illustrates how OpenAI Codex resolves nested instruction files in monorepos. Codex traverses from the project root down to the working directory, inheriting parent instructions while allowing child directories to override localized configurations.

## Architecture
- `AGENTS.md`: Global monorepo conventions (license check, branch conventions, PR formatting).
- `packages/billing/AGENTS.md`: Package-specific instructions (strict decimal precision, billing test runner).
- `packages/analytics/AGENTS.md`: Package-specific instructions (Spark/DuckDB pipeline rules).
- `verify_hierarchy.py`: Hierarchy resolver simulating Codex context concatenation.
- `test_hierarchy.py`: Automated tests verifying precedence and override behavior.

## Running Tests
```bash
python -m pytest examples/monorepo-agents-hierarchy/test_hierarchy.py -v
```
