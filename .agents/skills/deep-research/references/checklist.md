# deep-research Checklist & Provenance Verification

## Phase 1: Problem Definition & Scope Framing
- [ ] Define the specific architectural or empirical question to investigate.
- [ ] Identify key search terms, API methods, runtime flags, or paper concepts.
- [ ] Define exclusion criteria (e.g. discard blog posts older than 2 years without code repro).

## Phase 2: Authoritative Literature & Source Discovery
- [ ] Search official documentation and upstream primary repositories (OpenAI, Python, PEPs).
- [ ] Search peer-reviewed academic literature (arXiv, ACM, IEEE) for theoretical models.
- [ ] Search practitioner engineering reports and battle-tested post-mortems.
- [ ] Check official changelogs, issue trackers, and pull requests for recent runtime modifications.

## Phase 3: Provenance Recording & Attribution
- [ ] Record metadata: `source_type` (official, maintainer, paper, benchmark, experiment, community).
- [ ] Record retrieval timestamp (`retrieved_at: YYYY-MM-DD`).
- [ ] Record specific version tested or cited (`codex_version_if_known`).
- [ ] Assign empirical confidence score (0.0 to 1.0) based on source authority and reproducibility.
- [ ] Summarize core findings, constraints, and operational implications.

## Phase 4: Cross-Verification & Counter-Evidence
- [ ] Seek disconfirming evidence: does another official source contradict the finding?
- [ ] Distinguish verified runtime behavior from recommended conventions.
- [ ] Identify environmental boundary conditions (OS differences, sandbox modes, model variants).

## Phase 5: Synthesis & Integration
- [ ] Register new citations in `sources/provenance.json`.
- [ ] Link findings into relevant guides under `docs/`.
- [ ] Formulate concrete, actionable recommendations for agent engineering workflows.
