# Provenance & Sources Index

This directory establishes the evidentiary foundation for **Codex Agent Engineering (CAE)**. Every architectural pattern, prompt design, workflow gate, and security rule in this repository is mapped to a verified source.

## Citation & Provenance Taxonomy

To prevent AI cargo-culting and unverified claims, all assertions in CAE are classified by `source_type`:

| Source Type | Definition | Verification Standard | Example |
| :--- | :--- | :--- | :--- |
| **`official`** | Published documentation, official repos, or release notes from OpenAI or Codex product teams | Direct link to official OpenAI domain, repository, or tool output | Codex CLI flags, `config.toml` schema |
| **`maintainer`** | Official OpenAI maintainer statements, discussions, or issue responses | Public commit, issue comment, or developer forum response | Subagent context boundary behaviors |
| **`paper`** | Peer-reviewed academic literature or formal technical reports | ArXiv, ACM, IEEE, or institutional preprint with methodology | SWE-bench, SWE-agent, Reflexion |
| **`benchmark`** | Empirical evaluations conducted under controlled, reproducible conditions | Task definitions, test suites, and raw metric logs in `benchmarks/` | CAE Benchmark Suite v1 results |
| **`experiment`** | Structured hypothesis tests conducted specifically within this repository | Recorded in `experiments/registry/` with methodology and raw data | Approval friction vs patch accuracy tests |
| **`community`** | Empirical findings and battle-tested patterns from external practitioners | Documented reproducible repro and clear caveats | Monorepo context optimization patterns |

---

## File Registry

- [`official-openai.md`](official-openai.md): Official OpenAI documentation, Codex CLI specifications, and platform constraints.
- [`papers.md`](papers.md): Academic research on coding agents, benchmark methodologies, context engineering, and software verification.
- [`community.md`](community.md): Documented patterns from production agent deployments across the open-source ecosystem.
- [`provenance.json`](provenance.json): Machine-readable index connecting guidelines to evidence.
