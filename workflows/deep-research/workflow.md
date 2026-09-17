# Workflow: Deep Technical Research Workflow

## 1. Input Specification
Complex engineering question, architecture trade-off, or library selection problem.

## 2. Context Ingestion
Project constraints, performance requirements, technology stack, target platforms.

## 3. Ordered Actions
1. Query Decomposition: Formulate targeted, orthogonal research queries.
2. Multi-Source Ingestion: Search official documentation, GitHub discussions, source code, and academic literature.
3. Provenance Tagging: Record source URL, publication date, author/maintainer identity, and confidence score.
4. Cross-Verification: Compare claims across multiple independent sources to weed out misinformation.
5. Trade-off Matrix: Construct structured decision matrix comparing alternatives across latency, memory, cost, and complexity.
6. Synthesis: Deliver executive recommendation with actionable next steps.

## 4. Required Tools & Surfaces
Web search, documentation MCP servers, git clone/read for upstream source inspection.

## 5. Constraints & Invariants
No speculative assertions without evidence. Clearly label confidence level on every finding.

## 6. Output & Deliverables
RESEARCH_SYNTHESIS.md with citation index, trade-off matrix, and architecture recommendation.

## 7. Verification Protocol
All cited links must be valid; claims must accurately represent the cited source text.

## 8. Failure Handling & Recovery
If sources conflict, report the disagreement explicitly and identify differing assumptions rather than picking arbitrarily.

---

## Vanilla Codex Comparison
> **When to use Vanilla Codex instead**: Vanilla Codex tends to produce generic, confident-sounding answers based on training memory; deep research workflow enforces external source grounding.
