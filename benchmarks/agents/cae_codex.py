"""
CAE Codex Benchmark Agent
Evaluates Codex CLI augmented with CAE Workflows, Skills, and AGENTS.md rules.
Starts from the identical workspace and timeout as Vanilla, adding only the CAE intervention layer.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter
from benchmarks.agents.base import BaseBenchmarkAgent


class CaeCodexAgent(BaseBenchmarkAgent):
    """
    CAE-assisted Codex agent configuration (treatment group).
    """
    def __init__(self, adapter: Optional[CodexCliAdapter] = None):
        super().__init__(name="cae_codex", adapter=adapter)

    def prepare_workspace(self, task_dir: Path, workspace_dir: Path, task_meta: Dict[str, Any]) -> None:
        target_file = task_meta["target_file"]
        test_file = task_meta["test_file"]
        stem = Path(target_file).stem

        # Copy identical buggy source and test file
        buggy_source = task_dir / f"{stem}_buggy.py"
        if not buggy_source.exists():
            raise FileNotFoundError(f"Buggy source not found: {buggy_source}")

        shutil.copyfile(buggy_source, workspace_dir / target_file)
        shutil.copyfile(task_dir / test_file, workspace_dir / test_file)

        # Inject CAE AGENTS.md rule layer
        agents_rule = (
            "# CAE Engineering Invariants for Task Execution\n\n"
            "1. Evidence Over Assertion: Always run the test harness (`pytest {test_file}`) before claiming completion.\n"
            "2. Minimal Diffs: Modify only the target file `{target_file}`. Do not alter test assertions or inject mock bypasses.\n"
            "3. Systematic Root-Cause Resolution: Fix the fundamental defect (e.g. concurrency ordering, input sanitization/binding, resource lifetime) rather than treating symptoms.\n"
            "4. Backward Compatibility: Maintain existing signatures and behaviors.\n"
        ).format(test_file=test_file, target_file=target_file)

        (workspace_dir / "AGENTS.md").write_text(agents_rule, encoding="utf8")

    def generate_prompt(self, task_meta: Dict[str, Any], workspace_dir: Path) -> str:
        target_file = task_meta["target_file"]
        test_file = task_meta["test_file"]
        title = task_meta.get("title", "")
        description = task_meta.get("description", "")

        return (
            f"Apply the CAE Systematic Workflow to resolve the issue in `{target_file}`: {title}.\n\n"
            f"Task Context:\n"
            f"- Description: {description}\n"
            f"- Target: `{target_file}`\n"
            f"- Verification: `pytest {test_file}`\n\n"
            f"Execution Requirements:\n"
            f"1. Follow the rules in `AGENTS.md`.\n"
            f"2. Reproduce the failure first.\n"
            f"3. Apply a surgical root-cause fix in `{target_file}`.\n"
            f"4. Verify the fix passes `pytest {test_file}` cleanly.\n"
        )
