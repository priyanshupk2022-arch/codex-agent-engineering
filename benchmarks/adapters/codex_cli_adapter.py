"""
Codex CLI Adapter for Agent Evaluations
Connects benchmark runners to local OpenAI Codex CLI execution environments.
Handles timeout enforcement, process isolation, output capture, and version detection.
"""

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


class CodexCliAdapter:
    """
    Adapter connecting benchmark runners to local Codex CLI execution environments.
    """
    def __init__(self, executable: str = "codex"):
        self.executable = executable

    def is_available(self) -> bool:
        """Check if the codex binary is discoverable in PATH or as an executable."""
        return shutil.which(self.executable) is not None

    def get_version(self) -> Optional[str]:
        """Query codex --version if available."""
        if not self.is_available():
            return None
        try:
            res = subprocess.run(
                [self.executable, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            return res.stdout.strip() or res.stderr.strip() or "unknown"
        except Exception:
            return "unknown"

    def execute_prompt(
        self,
        prompt: str,
        cwd: Path,
        approval_policy: str = "never",
        timeout: float = 120.0,
        extra_args: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute an agent turn via Codex CLI in the specified directory.
        """
        if not self.is_available():
            return {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": f"Executable '{self.executable}' not found in PATH.",
                "duration": 0.0,
                "timed_out": False,
                "error": f"Executable '{self.executable}' not found in PATH."
            }

        cmd = [self.executable, "exec", "--approval", approval_policy]
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(prompt)

        start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            duration = time.time() - start
            return {
                "success": proc.returncode == 0,
                "exit_code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "duration": duration,
                "timed_out": False,
                "error": None
            }
        except subprocess.TimeoutExpired as exc:
            duration = time.time() - start
            return {
                "success": False,
                "exit_code": -1,
                "stdout": (exc.stdout or "") if isinstance(exc.stdout, str) else "",
                "stderr": f"Execution timed out after {timeout}s: {exc}",
                "duration": duration,
                "timed_out": True,
                "error": f"Timed out after {timeout}s"
            }
        except Exception as exc:
            duration = time.time() - start
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(exc),
                "duration": duration,
                "timed_out": False,
                "error": str(exc)
            }
