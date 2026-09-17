"""
CAE Agent Evaluation Runner
Orchestrates fair, reproducible head-to-head evaluations between Vanilla Codex and Codex + CAE.
Ensures identical task content, isolated workspaces, strict timeout boundaries,
and automated evidence capture (logs, diffs, test metrics).
"""

import json
import os
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter
from benchmarks.agents.vanilla_codex import VanillaCodexAgent
from benchmarks.agents.cae_codex import CaeCodexAgent


def get_git_commit_sha() -> Optional[str]:
    """Retrieve current Git commit SHA if in git repo."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return res.stdout.strip() if res.returncode == 0 else None
    except Exception:
        return None


def run_agent_evaluation(
    task_filter: Optional[str] = None,
    run_id: Optional[str] = None,
    timeout: float = 120.0,
    output_dir: Optional[Path] = None,
    adapter: Optional[CodexCliAdapter] = None
) -> Dict[str, Any]:
    """
    Executes fair agent comparison across benchmark tasks.
    """
    adapter = adapter or CodexCliAdapter()
    run_id = run_id or f"run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    runs_base_dir = output_dir or (ROOT_DIR / "benchmarks" / "results" / "runs" / run_id)
    runs_base_dir.mkdir(parents=True, exist_ok=True)

    tasks_dir = ROOT_DIR / "benchmarks" / "tasks"
    task_dirs = sorted([d for d in tasks_dir.iterdir() if d.is_dir() and (d / "task.json").exists()])

    if task_filter:
        task_dirs = [d for d in task_dirs if task_filter in d.name]

    vanilla_agent = VanillaCodexAgent(adapter=adapter)
    cae_agent = CaeCodexAgent(adapter=adapter)

    is_available = adapter.is_available()
    codex_version = adapter.get_version() if is_available else None

    report: Dict[str, Any] = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "benchmark_version": "1.0.0",
        "environment": {
            "os": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version(),
            "codex_cli_version": codex_version,
            "model": "openai.gpt-5.5 (if configured in .codex/config.toml)",
            "provider": "codex-cli",
            "git_commit": get_git_commit_sha()
        },
        "status": "COMPLETED" if is_available else "AGENT_EVAL_SKIPPED",
        "skip_reason": None if is_available else "Codex CLI executable ('codex') not found in system PATH. Live agent evaluation requires OpenAI Codex CLI.",
        "tasks": [],
        "summary": {
            "total_tasks": len(task_dirs),
            "vanilla_passed": 0,
            "vanilla_pass_rate": 0.0,
            "cae_passed": 0,
            "cae_pass_rate": 0.0,
            "iterations": 1
        }
    }

    if not is_available:
        print("================================================================================")
        print("[!] NOTICE: Codex CLI binary ('codex') is not installed or not found in PATH.")
        print("    Live agent evaluation cannot be executed without the Codex CLI.")
        print("    Status: AGENT_EVAL_SKIPPED (Evidence integrity preserved; no faked results).")
        print("================================================================================")

        for t_dir in task_dirs:
            meta = json.loads((t_dir / "task.json").read_text(encoding="utf8"))
            t_id = meta.get("task_id", meta.get("id", t_dir.name))
            report["tasks"].append({
                "task_id": t_id,
                "title": meta.get("title", t_dir.name),
                "vanilla": {
                    "status": "SKIPPED",
                    "exit_code": None,
                    "passed": False,
                    "test_pass_rate": 0.0,
                    "execution_time_seconds": 0.0,
                    "timed_out": False,
                    "tool_calls": 0,
                    "changed_files": [],
                    "patch_correctness": "UNTESTED",
                    "log_path": ""
                },
                "cae": {
                    "status": "SKIPPED",
                    "exit_code": None,
                    "passed": False,
                    "test_pass_rate": 0.0,
                    "execution_time_seconds": 0.0,
                    "timed_out": False,
                    "tool_calls": 0,
                    "changed_files": [],
                    "patch_correctness": "UNTESTED",
                    "log_path": ""
                }
            })

        # Save metadata.json
        meta_file = runs_base_dir / "metadata.json"
        meta_file.write_text(json.dumps(report, indent=2), encoding="utf8")
        return report

    # If Codex is available, run fair head-to-head comparison
    print(f"[*] Starting live agent evaluation for run {run_id} ({len(task_dirs)} tasks)...")
    vanilla_passed_count = 0
    cae_passed_count = 0

    for t_dir in task_dirs:
        meta = json.loads((t_dir / "task.json").read_text(encoding="utf8"))
        t_id = meta.get("task_id", meta.get("id", t_dir.name))
        print(f"\n--- Evaluating Task: {t_id} ---")

        task_eval_dir = runs_base_dir / t_id
        vanilla_dir = task_eval_dir / "vanilla"
        cae_dir = task_eval_dir / "cae"

        # 1. Vanilla Run
        print(" -> Running Vanilla Codex...")
        vanilla_res = vanilla_agent.run_task(t_dir, vanilla_dir, timeout=timeout)
        (vanilla_dir / "stdout.log").write_text(vanilla_res["stdout"], encoding="utf8")
        (vanilla_dir / "stderr.log").write_text(vanilla_res["stderr"], encoding="utf8")
        (vanilla_dir / "diff.patch").write_text(vanilla_res["diff"], encoding="utf8")
        (vanilla_dir / "tests.json").write_text(json.dumps({
            "passed": vanilla_res["passed"],
            "test_pass_rate": vanilla_res["test_pass_rate"],
            "output": vanilla_res["test_output"]
        }, indent=2), encoding="utf8")

        if vanilla_res["passed"]:
            vanilla_passed_count += 1

        # 2. CAE Run
        print(" -> Running Codex + CAE Workflow...")
        cae_res = cae_agent.run_task(t_dir, cae_dir, timeout=timeout)
        (cae_dir / "stdout.log").write_text(cae_res["stdout"], encoding="utf8")
        (cae_dir / "stderr.log").write_text(cae_res["stderr"], encoding="utf8")
        (cae_dir / "diff.patch").write_text(cae_res["diff"], encoding="utf8")
        (cae_dir / "tests.json").write_text(json.dumps({
            "passed": cae_res["passed"],
            "test_pass_rate": cae_res["test_pass_rate"],
            "output": cae_res["test_output"]
        }, indent=2), encoding="utf8")

        if cae_res["passed"]:
            cae_passed_count += 1

        task_summary = {
            "task_id": t_id,
            "title": meta.get("title", t_dir.name),
            "vanilla": {
                "status": vanilla_res["status"],
                "exit_code": vanilla_res["exit_code"],
                "passed": vanilla_res["passed"],
                "test_pass_rate": vanilla_res["test_pass_rate"],
                "execution_time_seconds": vanilla_res["execution_time_seconds"],
                "timed_out": vanilla_res["timed_out"],
                "tool_calls": vanilla_res["tool_calls"],
                "changed_files": vanilla_res["changed_files"],
                "patch_correctness": vanilla_res["patch_correctness"],
                "log_path": str(vanilla_dir.relative_to(ROOT_DIR))
            },
            "cae": {
                "status": cae_res["status"],
                "exit_code": cae_res["exit_code"],
                "passed": cae_res["passed"],
                "test_pass_rate": cae_res["test_pass_rate"],
                "execution_time_seconds": cae_res["execution_time_seconds"],
                "timed_out": cae_res["timed_out"],
                "tool_calls": cae_res["tool_calls"],
                "changed_files": cae_res["changed_files"],
                "patch_correctness": cae_res["patch_correctness"],
                "log_path": str(cae_dir.relative_to(ROOT_DIR))
            }
        }
        report["tasks"].append(task_summary)

    total_tasks = len(task_dirs)
    report["summary"]["vanilla_passed"] = vanilla_passed_count
    report["summary"]["vanilla_pass_rate"] = round(vanilla_passed_count / total_tasks, 4) if total_tasks else 0.0
    report["summary"]["cae_passed"] = cae_passed_count
    report["summary"]["cae_pass_rate"] = round(cae_passed_count / total_tasks, 4) if total_tasks else 0.0

    meta_file = runs_base_dir / "metadata.json"
    meta_file.write_text(json.dumps(report, indent=2), encoding="utf8")
    print(f"\n[+] Agent evaluation complete. Results saved to: {runs_base_dir}")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Vanilla Codex vs CAE Agent Benchmark")
    parser.add_argument("--task", type=str, default=None, help="Filter by task ID")
    parser.add_argument("--timeout", type=float, default=120.0, help="Per-task timeout in seconds")
    parser.add_argument("--run-id", type=str, default=None, help="Custom run identifier")
    args = parser.parse_args()

    result = run_agent_evaluation(task_filter=args.task, run_id=args.run_id, timeout=args.timeout)
    print(json.dumps(result, indent=2))
