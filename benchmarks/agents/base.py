"""
Base Benchmark Agent Interface
Defines the standard contract for autonomous coding agent evaluation.
"""

import abc
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter


class BaseBenchmarkAgent(abc.ABC):
    """
    Abstract base class for benchmark evaluation agents.
    """
    def __init__(self, name: str, adapter: Optional[CodexCliAdapter] = None):
        self.name = name
        self.adapter = adapter or CodexCliAdapter()

    @abc.abstractmethod
    def prepare_workspace(self, task_dir: Path, workspace_dir: Path, task_meta: Dict[str, Any]) -> None:
        """
        Prepare the workspace before agent invocation.
        Vanilla setup vs CAE setup hook.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def generate_prompt(self, task_meta: Dict[str, Any], workspace_dir: Path) -> str:
        """
        Build the prompt provided to the agent.
        """
        raise NotImplementedError

    def run_task(
        self,
        task_dir: Path,
        workspace_dir: Path,
        timeout: float = 120.0
    ) -> Dict[str, Any]:
        """
        Executes a benchmark task against an isolated workspace directory.
        Evaluates agent modification with the task's pytest suite.
        """
        with open(task_dir / "task.json", "r", encoding="utf8") as f:
            task_meta = json.load(f)

        target_file = task_meta["target_file"]
        test_file = task_meta["test_file"]

        # 1. Prepare isolated workspace
        workspace_dir.mkdir(parents=True, exist_ok=True)
        self.prepare_workspace(task_dir, workspace_dir, task_meta)

        # Snapshot initial state for diff calculation
        initial_file = workspace_dir / target_file
        initial_content = initial_file.read_text(encoding="utf8") if initial_file.exists() else ""

        # 2. Check if adapter can execute
        if not self.adapter.is_available():
            # If codex CLI is missing, cannot execute live agent
            return {
                "status": "AGENT_EVAL_SKIPPED",
                "exit_code": None,
                "passed": False,
                "test_pass_rate": 0.0,
                "execution_time_seconds": 0.0,
                "timed_out": False,
                "tool_calls": 0,
                "changed_files": [],
                "diff": "",
                "patch_correctness": "UNTESTED",
                "stdout": "",
                "stderr": f"Codex CLI executable ('{self.adapter.executable}') not available in PATH.",
                "test_output": "Tests skipped: Agent executable not found."
            }

        # 3. Generate prompt & execute agent turn
        prompt = self.generate_prompt(task_meta, workspace_dir)
        exec_res = self.adapter.execute_prompt(prompt, cwd=workspace_dir, timeout=timeout)

        # 4. Measure changes
        final_file = workspace_dir / target_file
        final_content = final_file.read_text(encoding="utf8") if final_file.exists() else ""

        changed_files = []
        diff_text = ""
        if initial_content != final_content:
            changed_files.append(target_file)
            import difflib
            diff_lines = difflib.unified_diff(
                initial_content.splitlines(keepends=True),
                final_content.splitlines(keepends=True),
                fromfile=f"a/{target_file}",
                tofile=f"b/{target_file}"
            )
            diff_text = "".join(diff_lines)

        # 5. Run test verification on the resulting workspace
        test_path = workspace_dir / test_file
        cmd = [sys.executable, "-m", "pytest", str(test_path), "-q"]
        test_start = time.time()
        try:
            test_proc = subprocess.run(
                cmd,
                cwd=str(workspace_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=min(timeout, 30.0)
            )
            test_passed = (test_proc.returncode == 0)
            test_rate = 1.0 if test_passed else 0.0
            test_log = test_proc.stdout + "\n" + test_proc.stderr
        except subprocess.TimeoutExpired as exc:
            test_passed = False
            test_rate = 0.0
            test_log = f"Pytest verification timed out: {exc}"
        except Exception as exc:
            test_passed = False
            test_rate = 0.0
            test_log = f"Pytest execution error: {exc}"

        patch_correctness = "CORRECT" if test_passed else ("INCOMPLETE" if changed_files else "FAILED")

        return {
            "status": "COMPLETED" if not exec_res["timed_out"] else "TIMED_OUT",
            "exit_code": exec_res["exit_code"],
            "passed": test_passed,
            "test_pass_rate": test_rate,
            "execution_time_seconds": round(exec_res["duration"], 4),
            "timed_out": exec_res["timed_out"],
            "tool_calls": 0,
            "changed_files": changed_files,
            "diff": diff_text,
            "patch_correctness": patch_correctness,
            "stdout": exec_res["stdout"],
            "stderr": exec_res["stderr"],
            "test_output": test_log
        }
