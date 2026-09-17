# Example: Full-Stack Feature Workflow (Spec-Driven Development)

This example demonstrates end-to-end **Spec-Driven Development (SDD)** with GitHub Spec Kit (`specify`) and OpenAI Codex.

## Architecture
- `spec.md`: Baseline functional specification with invariant contracts and user stories.
- `plan.md`: Architectural blueprint, component topology, and risk analysis.
- `app.py`: Implementation of a rate-limited Token Bucket API endpoint in Python (FastAPI-compatible standalone class).
- `test_app.py`: Automated test suite validating happy path, rate limiting (HTTP 429), and concurrency safety.

## How to Run
```bash
# Execute the example test suite
python -m pytest examples/full-stack-feature/test_app.py -v
```
