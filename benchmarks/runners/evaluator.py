import os
import sys
import json
import shutil
import tempfile
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Tuple

class TaskEvaluator:
    @staticmethod
    def evaluate_task(task_dir: Path, solution_mode: str = "reference") -> Tuple[bool, float, float, str]:
        """
        Evaluates a task by copying target implementation into a temporary isolated workspace,
        executing the test file, and measuring pass rate and duration.
        Modes: 'buggy', 'reference', 'fixed'
        Returns: (passed, pass_rate, duration, output_log)
        """
        with open(task_dir / "task.json", "r", encoding="utf8") as f:
            meta = json.load(f)

        target_file = meta["target_file"]
        test_file = meta["test_file"]
        stem = Path(target_file).stem

        if solution_mode in ("reference", "fixed"):
            candidates = [task_dir / f"{stem}_reference.py", task_dir / f"{stem}_fixed.py"]
            source_path = next((c for c in candidates if c.exists()), None)
        else:
            candidates = [task_dir / f"{stem}_buggy.py"]
            source_path = next((c for c in candidates if c.exists()), None)

        if not source_path or not source_path.exists():
            raise FileNotFoundError(f"Source implementation for mode '{solution_mode}' not found in {task_dir}")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Copy implementation as target_file
            shutil.copyfile(source_path, temp_path / target_file)
            shutil.copyfile(task_dir / test_file, temp_path / test_file)

            cmd = [sys.executable, "-m", "pytest", str(temp_path / test_file), "-q"]
            start = time.time()
            try:
                proc = subprocess.run(cmd, cwd=temp_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
                duration = time.time() - start
                passed = (proc.returncode == 0)
                output = proc.stdout + "\n" + proc.stderr
                pass_rate = 1.0 if passed else 0.0
            except subprocess.TimeoutExpired as exc:
                duration = time.time() - start
                passed = False
                output = f"Execution timed out after 15.0s: {exc}"
                pass_rate = 0.0

            return passed, pass_rate, duration, output
