# Git Workflows for Agentic Systems

Git is the transactional ledger of software development. Agent workflows must maintain a pristine, bisectable commit history with clean rollback semantics.

---

## 1. Worktree Isolation

For parallel tasks or speculative refactoring, use Git Worktrees to isolate agent work from the active developer workspace:

```bash
# Create isolated worktree for agent task
git worktree add ../agent-feature-worktree -b feature/isolated-agent-task

# Run agent workflow within worktree
cd ../agent-feature-worktree
# ... perform work, run tests ...

# Clean up after merge or abandonment
git worktree remove ../agent-feature-worktree
```

---

## 2. Atomic Commits & Conventional Messages

- Commits must be atomic: each commit represents one logical change that passes all tests.
- Follow Conventional Commits format:
  - `feat(auth): implement token refresh rotation`
  - `fix(db): resolve connection pool starvation under heavy load`
  - `test(benchmarks): add concurrency stress suite for order processing`
