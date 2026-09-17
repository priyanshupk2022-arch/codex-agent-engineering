# Context Engineering for Codex Agents

Context is the finite working memory of any LLM-powered coding agent. Context engineering is the deliberate practice of maximizing signal while strictly bounding token noise.

---

## 1. The Token Economy in Codex

Every token injected into the Codex context window incurs:
1. **Financial Cost**: API pricing scales linearly or quadratically with prompt tokens.
2. **Latency Penalty**: Time-To-First-Token (TTFT) and processing latency increase.
3. **Reasoning Degradation ("Lost in the Middle")**: Models demonstrate decreased retrieval and attention accuracy as context fills up.
4. **Auto-Compaction Risk**: When context exceeds limits, the runtime compresses previous history into lossy summaries.

---

## 2. Context Triage: The 3-Tier Retrieval Pattern

Never dump entire directory trees or large files into the prompt. Follow the **3-Tier Retrieval Pattern**:

```
Tier 1: Structural Discovery (tree / fd / git ls-files)
           │
           ▼
Tier 2: Targeted Indexing (grep / ripgrep for exact symbols)
           │
           ▼
Tier 3: Surgical Inspection (bounded line slices, e.g. lines 40-90)
```

### Prohibited Patterns:
- Running `cat <large-file>` without line bounds.
- Dumping entire vendor directories (`node_modules/`, `.venv/`).
- Concatenating all test outputs when only 2 tests failed.

---

## 3. Anti-Compaction Defense

Auto-compaction occurs when a continuous multi-turn session exceeds ~80% of model window capacity.
To prevent critical requirements from being lost during compaction:

1. **State Persistence**: Write architectural decisions to persistent markdown files (`docs/`, `.specify/`, `aidlc/`) rather than keeping them solely in conversation memory.
2. **Session Bounding**: For major tasks, start fresh sessions with clean working trees rather than dragging 40-turn debugging sessions into new feature work.
3. **Structured Handoffs**: Use standardized handoff summaries when transferring tasks between subagents or across sessions.
