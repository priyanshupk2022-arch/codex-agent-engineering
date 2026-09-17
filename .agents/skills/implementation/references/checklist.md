# implementation Checklist & Surgical Modification Protocol

## Phase 1: Pre-Implementation Gate
- [ ] Functional specification approved ($speckit-specify or Jira/PR issue description).
- [ ] Implementation plan drafted with ordered, atomic task breakdowns ($speckit-plan).
- [ ] Baseline test suite passes 100% on unmodified main branch.
- [ ] Target file scope defined; commit not to touch files outside declared boundary.

## Phase 2: Surgical Implementation
- [ ] Write minimal, targeted code changes directly addressing the specification.
- [ ] Preserve existing code conventions, naming patterns, and typing style.
- [ ] Do not reformat unrelated lines, sort imports across untouched files, or rewrite working logic.
- [ ] Avoid introducing unvetted external dependencies.
- [ ] Add explicit input validation at all public function and API boundaries.

## Phase 3: Concurrency & Fault Tolerance
- [ ] Ensure thread safety: acquire locks in deterministic hierarchical order to prevent deadlocks.
- [ ] Handle error paths with explicit exceptions; never swallow errors with bare `except: pass`.
- [ ] Use `try...finally` or context managers for asynchronous resource reclamation.
- [ ] Normalize external input (whitespace, null checks, case sensitivity).

## Phase 4: Local Verification
- [ ] Execute newly written unit tests for the modified component.
- [ ] Execute full regression suite to ensure zero unintended breakages.
- [ ] Run `python skills/implementation/scripts/check_diff_scope.py <allowed_dir>` to verify scope containment.
- [ ] Inspect `git diff` manually to confirm no stray debug print statements or secret keys.
