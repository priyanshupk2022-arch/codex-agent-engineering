import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any

class CodexCliAdapter:
    """
    Adapter connecting benchmark runners to local Codex CLI execution environments.
    """
    def __init__(self, executable: str = "codex"):
        self.executable = executable

    def is_available(self) -> bool:
        return shutil.which(self.executable) is not None

    def execute_prompt(self, prompt: str, cwd: Path, approval_policy: str = "never") -> Dict[str, Any]:
        if not self.is_available():
            return {"success": False, "error": f"Executable '{self.executable}' not found in PATH."}
        
        cmd = [self.executable, "exec", "--approval", approval_policy, prompt]
        proc = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode
        }
