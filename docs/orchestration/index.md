# Agent Orchestration: Single-Agent vs Multi-Agent

Multi-agent swarms are popular in marketing, but in production engineering they often introduce excessive token overhead, communication latency, and coordination failure modes.

---

## 1. The Orchestration Principle: Single First, Swarm Second

```
Can this task be solved by a single focused agent with proper tools?
      │
     YES ──> USE SINGLE-AGENT WORKFLOW (Lowest cost, highest predictability)
      │
      NO (Requires independent perspectives, actor-critic verification, or massive parallel search)
      │
      ▼
USE SPECIALIZED, BOUNDED SUBAGENTS
```

---

## 2. Legitimate Multi-Agent Use Cases

1. **Actor-Critic Verification**:
   - One agent writes the implementation code.
   - An independent adversarial agent writes red-team tests and audits edge cases.
2. **Parallel Spec Exploration**:
   - Multiple subagents explore independent candidate architectures or benchmark competing implementations concurrently.
3. **Domain Specialist Audits**:
   - A security-specialist subagent audits the cryptographic and permission layers while a performance subagent profiles memory usage.

### Prohibited Multi-Agent Patterns:
- "Chatty" subagent committees debating trivial naming decisions.
- Passing full uncompressed context between agents.
- Circular delegation loops where subagents delegate back and forth without progress.
