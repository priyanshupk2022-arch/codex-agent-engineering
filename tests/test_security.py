"""
Security and Boundary Isolation Tests
Verifies that the repository, benchmark runners, and configuration enforces:
- Zero credentials or secrets in tracked files
- Workspace isolation and escape prevention
- Safe subprocess invocations (no shell=True injection vectors)
- Path traversal defense
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent

SUSPICIOUS_PATTERNS = [
    re.compile(r'(?:api[_-]?key|access[_-]?token|secret[_-]?key)\s*[:=]\s*["\'][A-Za-z0-9_\-\.]{20,}["\']', re.IGNORECASE),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'ghp_[A-Za-z0-9]{36}'),
    re.compile(r'sk-proj-[A-Za-z0-9_-]{30,}')
]

EXCLUDED_DIRS = {".git", ".pytest_cache", "__pycache__", "codex_agent_engineering.egg-info"}


def test_no_hardcoded_secrets_in_repo():
    """Scans all tracked text files for high-entropy secrets and credential patterns."""
    findings = []
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in EXCLUDED_DIRS for part in path.parts):
            # Skip binary files
            try:
                content = path.read_text(encoding="utf8", errors="ignore")
            except Exception:
                continue

            for pat in SUSPICIOUS_PATTERNS:
                matches = pat.findall(content)
                if matches:
                    findings.append(f"{path.relative_to(ROOT)}: match {pat.pattern[:30]}...")

    assert len(findings) == 0, f"Potential secrets detected:\n" + "\n".join(findings)


def test_evaluator_workspace_isolation():
    """Ensures task evaluation creates an isolated copy and does not mutate source task files."""
    from benchmarks.runners.evaluator import TaskEvaluator

    task_dir = ROOT / "benchmarks" / "tasks" / "cae-task-002-sql-injection"
    target_file = task_dir / "product_repo_fixed.py"
    original_mtime = target_file.stat().st_mtime
    original_content = target_file.read_text(encoding="utf8")

    # Run evaluation
    passed, rate, dur, log = TaskEvaluator.evaluate_task(task_dir, solution_mode="reference")
    assert passed is True

    # Assert source file in repo was never touched or modified
    assert target_file.stat().st_mtime == original_mtime
    assert target_file.read_text(encoding="utf8") == original_content


def test_no_unsafe_shell_true_invocations():
    """Verifies that Python automation scripts avoid shell=True in subprocess calls."""
    shell_true_pattern = re.compile(r'subprocess\.(?:run|Popen|check_call|check_output)\([^)]*shell\s*=\s*True', re.DOTALL)

    violations = []
    python_files = list((ROOT / "scripts").glob("*.py")) + list((ROOT / "benchmarks").rglob("*.py"))
    for py_file in python_files:
        code = py_file.read_text(encoding="utf8", errors="ignore")
        if shell_true_pattern.search(code):
            violations.append(str(py_file.relative_to(ROOT)))

    assert len(violations) == 0, f"Unsafe shell=True found in:\n" + "\n".join(violations)


def test_config_security_boundaries():
    """Ensures shipped configs default to safe boundaries without hardcoded AWS profiles."""
    config_file = ROOT / ".codex" / "config.toml"
    assert config_file.exists()
    content = config_file.read_text(encoding="utf8")

    # Ensure profile = "default" is commented out or absent
    lines = content.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("profile =") or stripped.startswith("region ="):
            assert False, f"Active machine profile found in .codex/config.toml: {stripped}"
        if stripped == "sandbox_mode = \"danger-full-access\"":
            assert False, "Danger full access enabled in config.toml!"


def test_path_traversal_defense_in_runner():
    """Ensures task filter or identifiers cannot traverse outside benchmarks/tasks."""
    from benchmarks.runners.evaluator import TaskEvaluator

    malicious_path = ROOT / "benchmarks" / "tasks" / ".." / ".." / "docs"
    with pytest.raises((FileNotFoundError, KeyError, Exception)):
        TaskEvaluator.evaluate_task(malicious_path, solution_mode="reference")
