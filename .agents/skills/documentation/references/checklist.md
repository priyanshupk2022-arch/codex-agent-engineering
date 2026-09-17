# documentation Checklist & Technical Writing Quality Protocol

## Phase 1: Information Architecture & Structure
- [ ] Clear top-level H1 header defining topic concisely.
- [ ] Progressive disclosure: Executive Summary -> Architecture -> Runnable Examples -> Reference.
- [ ] Headings follow hierarchical markdown order (H1 -> H2 -> H3); no heading levels skipped.
- [ ] Table of contents provided for documents exceeding 150 lines.

## Phase 2: Technical Accuracy & Reproducibility
- [ ] All CLI commands and code snippets verified by manual or automated execution.
- [ ] Example commands use standard POSIX / PowerShell syntax without fictitious flags.
- [ ] Relative file links resolve to real files on disk.
- [ ] Configuration samples validate against declared TOML / JSON schemas.

## Phase 3: Provenance & Evidence Standards
- [ ] Unverified community opinions clearly distinguished from official OpenAI Codex specifications.
- [ ] Empirical claims backed by citations in `sources/provenance.json`.
- [ ] Performance claims accompanied by benchmark replication commands.

## Phase 4: Formatting & Discoverability
- [ ] Markdown formatting passes `python skills/documentation/scripts/doc_lint.py`.
- [ ] Code blocks specify correct language identifier (`python`, `bash`, `toml`, `json`).
- [ ] Diagrams use standard Mermaid syntax with plain-text table fallbacks.
