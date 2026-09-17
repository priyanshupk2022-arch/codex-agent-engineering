# Skill: deep-research

## Overview
Evidence-backed technical research on architecture, algorithms, libraries, or security vulnerabilities.

## When to Use
When evaluating technology choices, debugging undocumented framework behavior, or designing novel agent workflows.

## Inputs
Research question, scope boundaries, required evidence standard (e.g. official docs, peer-reviewed papers).

## Workflow
1. Query Formulation: Decompose broad research question into targeted search queries.
2. Multi-Source Gathering: Consult official documentation, authoritative code repositories, academic preprints, and issue trackers.
3. Evidence Triangulation: Compare multiple independent sources to eliminate hallucinated or outdated claims.
4. Synthesis & Documentation: Author RESEARCH_BRIEF.md with explicit provenance, confidence scores, and trade-off tables.
5. Peer Review: Challenge conclusions against known counterexamples and edge cases.

## Outputs & Deliverables
Structured RESEARCH_BRIEF.md with citations, trade-off matrices, and implementation recommendations.

## Constraints & Guardrails
Every factual claim must cite a verifiable source URL or paper DOI. Must clearly distinguish between verified facts and community opinions.

## Verification Protocol
All links checked and valid; confidence scores calculated using standard rubric (1.0 official, 0.8 community, 0.5 unconfirmed).

## Common Failure Modes & Recovery
Information obsolescence -> verify library version matches current target; check commit dates and deprecation notices.
