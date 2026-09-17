# Codex Surfaces: Choosing the Smallest Appropriate Surface

A foundational rule of Codex Agent Engineering is: **Always use the smallest, most restrictive surface that solves the problem.**

Over-specifying in the prompt or bloating global configuration degrades model reasoning, inflates token costs, and increases the surface area for agent drift and hallucination.

```
       Global Defaults: ~/.codex/config.toml, ~/.codex/AGENTS.md
                                 │
                                 ▼
       Project Scope:   .codex/config.toml, ./AGENTS.md
                                 │
                                 ▼
       Directory Scope: ./services/billing/AGENTS.md
                                 │
                                 ▼
       Procedural Task: .agents/skills/<skill>/SKILL.md
                                 │
                                 ▼
       External System: Model Context Protocol (MCP) Server
                                 │
                                 ▼
       Ephemeral Intent: Direct User Session Prompt
```

---

## The Surface Decision Matrix

| Surface | Lifecycle / Scope | Primary Purpose | Cost / Overhead | Anti-Pattern |
| :--- | :--- | :--- | :--- | :--- |
| **User Prompt** | Single turn / ephemeral | Expresses immediate intent, scope constraints, and transient decisions. | Low context, zero disk footprint. | Pasting full API documentation or multi-page runbooks in chat. |
| **`AGENTS.md` (Root)** | Persistent / repository | Declares non-negotiable project commands (build, test, lint), invariants, and directory topography. | Included on every session startup. Must be concise (<1,500 tokens). | Long architectural manifestos, full code samples, or step-by-step feature guides. |
| **`AGENTS.md` (Nested)** | Persistent / package | Provides subsystem-specific conventions (e.g., Python backend vs React frontend rules in monorepos). | Loaded only when agent operates within that directory tree. | Duplicating root build commands across nested files. |
| **`AGENTS.override.md`** | Ephemeral / local | Developer-specific overrides (e.g. personal local ports, debug flags) kept out of git. | Local to developer machine. | Checking personal credentials or machine paths into version control. |
| **Skill (`SKILL.md`)** | Invoked on demand | Encapsulates complex, multi-step engineering procedures (e.g., security audits, migrations). | Zero baseline cost; loaded only when triggered. | Creating one-line skills that should have been simple commands in `AGENTS.md`. |
| **Plugin** | Session-wide package | Bundles multiple related skills, hooks, and configuration templates into an installable unit. | Managed via CLI package manager. | Creating a monolithic plugin when isolated skills suffice. |
| **MCP Server** | External tool integration | Exposes structured APIs, database queries, and external services via JSON-RPC. | Tool definition tokens added to prompt window; network latency. | Exposing raw bash execution through MCP when Codex has native execution. |
| **`.codex/config.toml`** | Repository infrastructure | Enforces sandbox isolation, approval policies, model pins, and MCP configurations. | Zero prompt token cost; platform-enforced. | Storing prompt instructions inside configuration files. |

---

## Decision Flowchart: "Where should this instruction live?"

1. **Is it an absolute project invariant (e.g. "always run `npm test` before pushing")?**
   - **YES** -> Put it in **`AGENTS.md`**.
2. **Does it only apply to a specific package or microservice in a monorepo?**
   - **YES** -> Put it in that subdirectory's **`nested AGENTS.md`**.
3. **Is it a repeatable multi-step process with distinct phases (e.g. auditing security, running benchmarks)?**
   - **YES** -> Package it as a **Codex Skill (`.agents/skills/<name>/SKILL.md`)**.
4. **Does it require talking to an external database, issue tracker, or browser?**
   - **YES** -> Wire up a **Model Context Protocol (MCP)** server in `.codex/config.toml`.
5. **Is it a one-off request or exploratory task?**
   - **YES** -> Send it directly in the **User Prompt**.
