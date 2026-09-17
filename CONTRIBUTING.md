# Contributing to Codex Agent Engineering (CAE)

We welcome contributions from researchers, software engineers, and agent practitioners. To maintain exceptional quality, all contributions follow evidence-backed standards.

---

## 1. Contribution Categories
- **Skills**: Add or refine reusable skills in `skills/`. Must adhere to `SKILL.md` schema with runnable scripts, references, and failure handling.
- **Workflows**: Add or refine engineering workflows in `workflows/`. Must define Inputs -> Context -> Actions -> Tools -> Constraints -> Output -> Verification -> Failure Handling -> Vanilla Comparison.
- **Benchmarks**: Add deterministic tasks to `benchmarks/tasks/` with buggy baseline, fixed reference, and test suite.
- **Experiments**: Document controlled hypothesis tests in `experiments/registry/`. Negative results are welcome.
- **Documentation & Case Studies**: Add in-depth technical guides with provenance citations.

---

## 2. Quality Gates Before PR Submission
Every contribution must pass local verification:
```bash
# 1. Run full test suite
pytest tests/ -v

# 2. Run benchmark reference suite
python benchmarks/runners/runner.py reference

# 3. Validate skills format
python scripts/validate_skills.py

# 4. Check internal links
python scripts/check_links.py
```

---

## 3. Provenance & Anti-Plagiarism Rule
Never copy proprietary prompts or text from external repositories without attribution. Every factual claim must cite an official source or empirical test in `sources/`.
