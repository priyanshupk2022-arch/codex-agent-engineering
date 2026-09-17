# Implementation Hygiene & Minimal Diffs

Writing code with AI agents requires strict implementation hygiene to prevent regressions, unintended code churn, and architectural degradation.

---

## 1. Principles of Minimal Diff Engineering

1. **Do Not Refactor Unrelated Code**:
   - If you are fixing a bug in `auth.py`, do not reformat `database.py` or update imports in unrelated modules.
   - Large diffs hide regressions and make peer review nearly impossible.

2. **Match Surrounding Conventions**:
   - Adhere to the established styling, naming, error handling, and typing conventions of the existing file.
   - Do not introduce new third-party dependencies when standard library or existing dependencies suffice.

3. **Atomic File Modifications**:
   - Prefer surgical replacements (`replace_file_content` style chunks) over full file rewrites.
   - Full rewrites frequently drop edge-case handling or subtle comments.

---

## 2. Defensive Implementation Checklist

- [ ] Does this change introduce any new dependencies? (If yes, justify).
- [ ] Are all newly created functions typed and documented?
- [ ] Are external inputs validated at the boundary?
- [ ] Are all resources (file handles, network sockets, database connections) closed properly?
- [ ] Did I verify both the happy path and error paths?
