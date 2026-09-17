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
        initial_files: Dict[str, str] = {}
        for p in workspace_dir.rglob("*"):
            if p.is_file():
                rel = str(p.relative_to(workspace_dir)).replace("\\", "/")
                try:
                    initial_files[rel] = p.read_text(encoding="utf8", errors="replace")
                except Exception:
                    pass

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
                "test_output": "Tests skipped: Agent executable not found.",
                "final_state": {}
            }

        # 3. Generate prompt & execute agent turn
        prompt = self.generate_prompt(task_meta, workspace_dir)
        exec_res = self.adapter.execute_prompt(prompt, cwd=workspace_dir, timeout=timeout)

        # 4. Measure workspace changes across all files
        final_files: Dict[str, str] = {}
        for p in workspace_dir.rglob("*"):
            if p.is_file():
                rel = str(p.relative_to(workspace_dir)).replace("\\", "/")
                try:
                    final_files[rel] = p.read_text(encoding="utf8", errors="replace")
                except Exception:
                    pass

        changed_files = []
        diff_chunks = []
        all_keys = sorted(set(initial_files.keys()) | set(final_files.keys()))
        for k in all_keys:
            init_c = initial_files.get(k)
            fin_c = final_files.get(k)
            if init_c != fin_c:
                changed_files.append(k)
                import difflib
                lines1 = init_c.splitlines(keepends=True) if init_c is not None else []
                lines2 = fin_c.splitlines(keepends=True) if fin_c is not None else []
                diff_chunks.extend(difflib.unified_diff(lines1, lines2, fromfile=f"a/{k}", tofile=f"b/{k}"))

        diff_text = "".join(diff_chunks)

        # Check for forbidden shortcut: test tampering
        test_rel = str(Path(test_file)).replace("\\", "/")
        test_tampered = (test_rel in changed_files)

        # 5. Run test verification on the resulting workspace
        test_path = workspace_dir / test_file
        if test_tampered:
            test_passed = False
            test_rate = 0.0
            test_log = f"FORBIDDEN_SHORTCUT_DETECTED: Test harness '{test_file}' was modified or deleted by agent."
            patch_correctness = "FORBIDDEN_SHORTCUT"
        else:
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

        final_state = {k: final_files[k] for k in changed_files if k in final_files}
        if target_file in final_files and target_file not in final_state:
            final_state[target_file] = final_files[target_file]

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
            "test_output": test_log,
            "final_state": final_state
        }
