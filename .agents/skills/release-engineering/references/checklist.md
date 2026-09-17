# release-engineering Checklist & Semantic Release Protocol

## Phase 1: Versioning & Documentation Sync
- [ ] Determine next semantic version bump (MAJOR.MINOR.PATCH) following SemVer 2.0.0.
- [ ] Update `pyproject.toml` version string.
- [ ] Add version section in `CHANGELOG.md` with categorized changes (Added, Changed, Fixed, Security).
- [ ] Update `ROADMAP.md` marking completed deliverables.

## Phase 2: Quality Gate Verification
- [ ] Unit and integration test suite passes 100% locally (`pytest tests/ -v`).
- [ ] Benchmark reference suite passes 5/5 (`python benchmarks/runners/runner.py reference`).
- [ ] Skills schema validator passes 9/9 (`python scripts/validate_skills.py`).
- [ ] Documentation link checker reports zero broken links (`python scripts/check_links.py`).
- [ ] Health scanner reports status `HEALTHY` (`python scripts/cae_cli.py doctor`).

## Phase 3: Artifact Building & Packaging
- [ ] Build distribution package (`pip install -e .` or `python -m build`).
- [ ] Verify entrypoint command works cleanly (`cae --help`).
- [ ] Verify package installs cleanly in clean virtual environment.

## Phase 4: Git Release & Tagging
- [ ] Create signed or annotated git tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`).
- [ ] Push branch and tags to remote repository (`git push origin main --tags`).
- [ ] Draft GitHub Release notes with highlights, breaking changes, and contributor thanks.
