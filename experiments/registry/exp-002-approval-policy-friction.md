# Experiment EXP-002: Approval Policy Friction & Rubber-Stamping Fatigue

- **Status**: `SUPPORTED`
- **Date**: 2026-09-17
- **Model / Harness**: Codex CLI >= 0.145.0

---

## 1. Hypothesis
Operating Codex under an `untrusted` approval policy (prompting on every terminal command) increases human developer fatigue and causes a higher rate of inadvertent approval of destructive commands compared to an `on-request` policy combined with scoped allowlists.

## 2. Method
- 10 developers tasked with overseeing 5 complex migration tasks.
- 5 developers assigned `approval = "untrusted"`; 5 assigned `approval = "on-request"` with pre-approved read and test commands.
- At an unpredictable step in turn 15-20, an ambiguous command (`rm -rf build/ && rm -rf temp/`) was generated.

## 3. Results
- **`untrusted` Group**: 4 out of 5 developers approved the ambiguous command within <1.5 seconds without reading the path arguments (habitual rubber-stamping).
- **`on-request` Group**: 5 out of 5 developers stopped, inspected the prompt, and asked for clarification before approving.

## 4. Conclusion
Maximum prompt frequency degrades human vigilance. Scoped trust boundaries with selective approval prompts yield superior operational security.
