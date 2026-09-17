# Example: Secure Sandbox Deployment & Containment

This example demonstrates how to configure and enforce OpenAI Codex execution boundaries in enterprise environments using sandbox confinement policies.

## Architecture
- `codex.sandbox.toml`: Hardened project configuration locking sandbox to `workspace-write` with explicit network host allowlisting.
- `sandbox_enforcer.py`: Confinement enforcer validating filesystem write containment and network domain egress.
- `test_sandbox_enforcer.py`: Automated tests verifying defense against path traversal, arbitrary host writes, and unauthorized network calls.

## Running Tests
```bash
python -m pytest examples/secure-sandbox-deployment/test_sandbox_enforcer.py -v
```
