"""
Vanilla Codex Benchmark Agent
Evaluates unassisted Codex CLI baseline on benchmark tasks.
Receives only the task prompt, buggy starting file, and test file.
No CAE skills, workflows, or custom AGENTS.md instructions are injected.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter
from benchmarks.agents.base import BaseBenchmarkAgent


class VanillaCodexAgent(BaseBenchmarkAgent):
    """
    Vanilla Codex agent configuration (control group).
    """
    def __init__(self, adapter: Optional[CodexCliAdapter] = None):
        super().__init__(name="vanilla_codex", adapter=adapter)

    def prepare_workspace(self, task_dir: Path, workspace_dir: Path, task_meta: Dict[str, Any]) -> None:
        target_file = task_meta["target_file"]
        test_file = task_meta["test_file"]
        stem = Path(target_file).stem

        # Copy buggy source
        buggy_source = task_dir / f"{stem}_buggy.py"
        if not buggy_source.exists():
            raise FileNotFoundError(f"Buggy source not found: {buggy_source}")

        shutil.copyfile(buggy_source, workspace_dir / target_file)
        shutil.copyfile(task_dir / test_file, workspace_dir / test_file)

    def generate_prompt(self, task_meta: Dict[str, Any], workspace_dir: Path) -> str:
        target_file = task_meta["target_file"]
        test_file = task_meta["test_file"]
        title = task_meta.get("title", "")
        description = task_meta.get("description", "")

        return (
            f"Fix the issue in `{target_file}`: {title}.\n"
            f"Description: {description}\n\n"
            f"Ensure all tests in `{test_file}` pass by running `pytest {test_file}`.\n"
            f"Modify only `{target_file}` and make minimal changes."
        )
