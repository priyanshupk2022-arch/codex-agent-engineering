# AGENTS.md Hierarchy, Resolution & Inheritance

`AGENTS.md` is the standardized machine-readable instruction file for OpenAI Codex and compatible coding agents. Understanding how Codex resolves these files across directory trees is vital for monorepo scalability.

---

## 1. Resolution Order & Precedence

When Codex executes a command or navigates a workspace, it resolves instructions in strict order from most general to most specific:

```
1. Global User Instructions:     ~/.codex/AGENTS.md
2. Workspace Root Instructions:  <workspace_root>/AGENTS.md
3. Directory Tree Instructions:  <workspace_root>/path/to/subpkg/AGENTS.md
4. Local Override Instructions:  <workspace_root>/AGENTS.override.md (or nested equivalent)
```

### Precedence Rule
If an instruction in a nested `AGENTS.md` conflicts with a parent `AGENTS.md`, **the most specific (deepest) directive wins**.

*Example*:
- Root `AGENTS.md`: `Run pytest tests/`
- `services/billing/AGENTS.md`: `Run pytest services/billing/tests/ -m "not integration"`
- **Result when operating in `services/billing`**: The agent runs the billing-specific test command with the exclusion flag.

---

## 2. Token Budgeting & Compaction Defense

Because root `AGENTS.md` is loaded into the model context at the start of every session, large `AGENTS.md` files lead to:
1. **Context Window Contention**: Reduces room for codebase retrieval.
2. **Loss of Attention**: Models suffer attention degradation over long context windows.
3. **Compaction Erasure**: When conversations exceed context thresholds and trigger auto-compaction, verbose instructions are summarized and nuance is lost.

### Best Practices:
- Keep root `AGENTS.md` **under 1,500 tokens** (approx. 100-150 lines).
- Never include full code samples in `AGENTS.md`; link to reference files instead.
- Use imperative, concise statements:
  - Good: `Run 'pytest -q' before committing.`
  - Bad: `It is very important and highly recommended that you always remember to execute the pytest command with the quiet flag prior to concluding any commit.`
