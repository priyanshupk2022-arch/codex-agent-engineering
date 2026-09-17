import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_cli_benchmark_list():
    cmd = [sys.executable, str(ROOT / "scripts" / "cae_cli.py"), "benchmark", "list"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert proc.returncode == 0
    assert "cae-task-001-deadlock" in proc.stdout
    assert "cae-task-005-schema-migration" in proc.stdout

def test_cli_validate_skills():
    cmd = [sys.executable, str(ROOT / "scripts" / "cae_cli.py"), "validate-skills"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert proc.returncode == 0
    assert "[OK] code-review" in proc.stdout
