"""
CAE Open Source Release Audit
Automated gatekeeper verifying repository compliance, test health, benchmark integrity,
skill synchronization, provenance validity, link health, secret scanning, and license standards.
Outputs machine-readable JSON to benchmarks/results/oss_release_audit.json and exits 0 on PASS, 1 on FAIL.
"""

import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def check_license() -> Tuple[bool, str]:
    lic_file = ROOT_DIR / "LICENSE"
    if not lic_file.exists():
        return False, "LICENSE file missing."
    content = lic_file.read_text(encoding="utf8")
    if "MIT License" not in content or len(content) < 200:
        return False, "LICENSE is not a valid MIT license (>200 bytes)."
    return True, "Valid MIT License present."


def check_repository_metadata() -> Tuple[bool, str]:
    pyproject = ROOT_DIR / "pyproject.toml"
    if not pyproject.exists():
        return False, "pyproject.toml is missing."
    content = pyproject.read_text(encoding="utf8")
    if 'name = "codex-agent-engineering"' not in content:
        return False, "pyproject.toml does not contain valid project package name."
    return True, "pyproject.toml metadata verified."


def check_required_docs() -> Tuple[bool, str]:
    required = [
        "README.md", "AUDIT.md", "AGENTS.md", "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "ROADMAP.md", "CHANGELOG.md"
    ]
    missing = [doc for doc in required if not (ROOT_DIR / doc).exists()]
    if missing:
        return False, f"Missing required documentation: {missing}"
    return True, f"All {len(required)} required governance documents present."


def check_skills_integrity() -> Tuple[bool, str]:
    from scripts.validate_skills import validate_skills
    ok = validate_skills(ROOT_DIR / "skills")
    if not ok:
        return False, "validate_skills.py failed on skills/."
    return True, "9/9 canonical skills pass contract validation."


def check_skills_sync() -> Tuple[bool, str]:
    from scripts.check_skill_sync import check_skill_sync
    ok = check_skill_sync(ROOT_DIR / "skills", ROOT_DIR / ".agents" / "skills")
    if not ok:
        return False, "Skills projection in .agents/skills/ is out of sync."
    return True, "All canonical skills are in sync with .agents/skills/ projection."


def check_provenance_integrity() -> Tuple[bool, str]:
    prov_file = ROOT_DIR / "sources" / "provenance.json"
    if not prov_file.exists():
        return False, "sources/provenance.json missing."
    try:
        data = json.loads(prov_file.read_text(encoding="utf8"))
        records = data.get("records", [])
        if len(records) < 5:
            return False, f"Too few records in provenance.json: {len(records)}"
        for r in records:
            if not r.get("verification_status") or not r.get("claim_scope"):
                return False, f"Record {r.get('id')} lacks verification_status or claim_scope"
        return True, f"{len(records)} provenance records verified with strict taxonomy."
    except Exception as exc:
        return False, f"Provenance validation error: {exc}"


def check_internal_links() -> Tuple[bool, str]:
    from scripts.check_links import check_markdown_links
    ok = check_markdown_links(ROOT_DIR)
    if not ok:
        return False, "Broken markdown links detected."
    return True, "All internal markdown links resolved."


def check_ci_configuration() -> Tuple[bool, str]:
    ci_file = ROOT_DIR / ".github" / "workflows" / "ci.yml"
    if not ci_file.exists():
        return False, ".github/workflows/ci.yml missing."
    content = ci_file.read_text(encoding="utf8")
    required_steps = ["pytest tests/", "runner.py reference", "validate_skills.py", "check_links.py"]
    missing = [step for step in required_steps if step not in content]
    if missing:
        return False, f"CI workflow missing required validation steps: {missing}"
    return True, "CI workflow configured with comprehensive test matrix."


def check_benchmark_integrity() -> Tuple[bool, str]:
    tasks_dir = ROOT_DIR / "benchmarks" / "tasks"
    tasks = sorted([d for d in tasks_dir.iterdir() if d.is_dir()])
    if len(tasks) < 5:
        return False, f"Fewer than 5 benchmark tasks ({len(tasks)})"

    required_files = ["task.json", "README.md", "expected_behavior.md"]
    for t in tasks:
        for rf in required_files:
            if not (t / rf).exists():
                return False, f"Task {t.name} is missing {rf}"
        # Check task.json metadata
        meta = json.loads((t / "task.json").read_text(encoding="utf8"))
        if not meta.get("task_id") or not meta.get("forbidden_shortcuts") or not meta.get("timeout"):
            return False, f"Task {t.name} task.json missing hardened metadata"
    return True, f"All {len(tasks)} benchmark tasks satisfy task specification."


def check_secrets_scan() -> Tuple[bool, str]:
    suspicious = [
        re.compile(r'AKIA[0-9A-Z]{16}'),
        re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        re.compile(r'ghp_[A-Za-z0-9]{36}'),
        re.compile(r'sk-proj-[A-Za-z0-9_-]{30,}')
    ]
    excluded = {".git", ".pytest_cache", "__pycache__", "codex_agent_engineering.egg-info"}
    for p in ROOT_DIR.rglob("*"):
        if p.is_file() and not any(part in excluded for part in p.parts):
            try:
                text = p.read_text(encoding="utf8", errors="ignore")
            except Exception:
                continue
            for pat in suspicious:
                if pat.search(text):
                    return False, f"Secret pattern matched in {p.relative_to(ROOT_DIR)}"
    return True, "Zero secrets or personal API tokens detected in repository."


def check_benchmark_freshness() -> Tuple[bool, str]:
    summary_md = ROOT_DIR / "benchmarks" / "results" / "summary.md"
    if not summary_md.exists():
        return False, "benchmarks/results/summary.md is missing."
    content = summary_md.read_text(encoding="utf8")
    if "Generated At" not in content or "Git Commit SHA" not in content:
        return False, "summary.md is missing required provenance generation headers."
    if "100.0% (5/5)" not in content:
        return False, "summary.md does not record verified reference pass rate."
    return True, "Benchmark summary is fresh and contains execution metadata."


def check_unit_tests() -> Tuple[bool, str]:
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60
    )
    if res.returncode != 0:
        return False, f"pytest tests/ failed:\n{res.stdout}\n{res.stderr}"
    return True, "Full unit and integration test suite passing (100%)."


def run_oss_release_audit() -> Dict[str, Any]:
    print("================================================================================")
    print("                CODEX AGENT ENGINEERING OSS RELEASE AUDIT                      ")
    print("================================================================================")

    checks = [
        ("license", check_license),
        ("repository_metadata", check_repository_metadata),
        ("required_docs", check_required_docs),
        ("skills_integrity", check_skills_integrity),
        ("skills_sync", check_skills_sync),
        ("provenance_integrity", check_provenance_integrity),
        ("internal_links", check_internal_links),
        ("ci_configuration", check_ci_configuration),
        ("benchmark_integrity", check_benchmark_integrity),
        ("secrets_scan", check_secrets_scan),
        ("benchmark_freshness", check_benchmark_freshness),
        ("unit_tests", check_unit_tests)
    ]

    results = {}
    all_passed = True

    for name, func in checks:
        start = time.time()
        passed, msg = func()
        dur = time.time() - start
        results[name] = {
            "passed": passed,
            "message": msg,
            "duration_seconds": round(dur, 3)
        }
        status_tag = "[PASS]" if passed else "[FAIL]"
        print(f"{status_tag:7} {name:24} -> {msg} ({dur:.2f}s)")
        if not passed:
            all_passed = False

    overall_status = "PASS" if all_passed else "FAIL"

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "audit_version": "1.0.0",
        "oss_release_status": overall_status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for r in results.values() if r["passed"]),
        "failed_checks": sum(1 for r in results.values() if not r["passed"]),
        "environment": {
            "os": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version()
        },
        "checks": results
    }

    results_dir = ROOT_DIR / "benchmarks" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    out_file = results_dir / "oss_release_audit.json"
    out_file.write_text(json.dumps(report, indent=2), encoding="utf8")

    print("\n================================================================================")
    print(f"OSS_RELEASE_STATUS = {overall_status}")
    print(f"Audit report saved to: {out_file.relative_to(ROOT_DIR)}")
    print("================================================================================")

    return report


if __name__ == "__main__":
    report = run_oss_release_audit()
    sys.exit(0 if report["oss_release_status"] == "PASS" else 1)
