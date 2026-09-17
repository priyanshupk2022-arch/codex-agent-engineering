# Release Manifest: Codex Agent Engineering v0.1.1

**Version**: v0.1.1  
**Release Date**: 2026-09-17  
**Git Tag**: `v0.1.1`  
**Release Manager**: CAE Release Specialist  
**Release Status**: STABLE & VERIFIED  

---

## 1. Release Highlights
- Hardened benchmark concurrency runner: fixed self-transfer lock contention and introduced absolute join deadlines.
- Implemented robust input validation for inventory race condition and schema migration parser edge cases.
- Unified CLI (`cae`): added positional suite argument parsing supporting `cae benchmark run suite-v1`.
- Added complete packaging infrastructure (`pyproject.toml`, `pytest.ini`) with editable pip installation.
- Populated complete, runnable Python helper scripts and comprehensive checklists for all 9 core skills.

---

## 2. Quality Gate Verification Log
```bash
$ python scripts/cae_cli.py doctor
=== Codex Agent Engineering Doctor ===
[*] Running CAE Automated Maintenance Scanner...
[*] Scan complete: Status=HEALTHY, Issues=0
Repository Health: HEALTHY
[+] All systems green.

$ pytest tests/ -v
============================== 8 passed in 3.33s ==============================
```

---

## 3. Artifact Checksums
- `codex_agent_engineering-0.1.1-0.editable-py3-none-any.whl`: Verified SHA256 match.
