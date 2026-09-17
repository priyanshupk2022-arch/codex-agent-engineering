"""
CAE Benchmark Suite Runner
Runs deterministic benchmark tasks across modes: reference, buggy, or agent.
Supports multiple iterations with flakiness and statistical aggregation.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from benchmarks.metrics.collector import MetricCollector
from benchmarks.runners.evaluator import TaskEvaluator


def run_suite(
    mode: str = "reference",
    task_filter: Optional[str] = None,
    iterations: int = 1
) -> Dict[str, Any]:
    """
    Runs the benchmark suite over the requested mode and iterations.
    """
    if mode == "agent":
        from benchmarks.runners.agent_runner import run_agent_evaluation
        return run_agent_evaluation(task_filter=task_filter)

    tasks_dir = root_dir / "benchmarks" / "tasks"
    collector = MetricCollector(suite_version="1.0.0", iterations=iterations)

    task_dirs = sorted([d for d in tasks_dir.iterdir() if d.is_dir()])
    discovered = []
    for t_dir in task_dirs:
        task_meta_file = t_dir / "task.json"
        if not task_meta_file.exists():
            continue
        with open(task_meta_file, "r", encoding="utf8") as f:
            meta = json.load(f)
        task_id = meta.get("task_id", meta.get("id", t_dir.name))
        if task_filter and task_filter not in task_id:
            continue
        discovered.append((t_dir, meta, task_id))

    print(f"[*] Discovered {len(discovered)} benchmark tasks. Running in mode '{mode}' with iterations={iterations}...")

    for i in range(1, iterations + 1):
        if iterations > 1:
            print(f"\n=== Iteration {i}/{iterations} ===")
        for t_dir, meta, task_id in discovered:
            title = meta.get("title", task_id)
            print(f" -> Running task [{task_id}] in mode '{mode}' (iter {i})...")
            passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode=mode)

            patch_correctness = "CORRECT" if passed else ("FAILED" if mode == "buggy" else "INCOMPLETE")
            collector.record_task_result(
                task_id=task_id,
                title=title,
                mode=mode,
                passed=passed,
                test_pass_rate=pass_rate,
                duration=duration,
                iterations=i,
                patch_correctness=patch_correctness,
                notes=f"Evaluated with exit code {'0' if passed else 'non-zero'} in {round(duration, 3)}s"
            )
            status_str = "PASS" if passed else "FAIL (Expected for buggy baseline)"
            print(f"    Result: {status_str} in {round(duration, 3)}s")

    report = collector.export_report()
    return report


def main():
    parser = argparse.ArgumentParser(description="CAE Benchmark Runner")
    parser.add_argument("mode", nargs="?", default="reference", choices=["reference", "buggy", "agent"],
                        help="Benchmark execution mode (default: reference)")
    parser.add_argument("--task", type=str, default=None, help="Filter by task ID")
    parser.add_argument("--iterations", "-n", type=int, default=1, help="Number of iterations to run (for flakiness detection)")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output JSON path")
    args = parser.parse_args()

    report = run_suite(mode=args.mode, task_filter=args.task, iterations=args.iterations)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2), encoding="utf8")
        print(f"[+] Benchmark report saved to: {out_path}")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
