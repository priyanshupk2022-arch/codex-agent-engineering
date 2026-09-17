import sys
import json
import time
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from benchmarks.metrics.collector import MetricCollector
from benchmarks.runners.evaluator import TaskEvaluator

def run_suite(mode: str = "reference", task_filter: str = None) -> dict:
    tasks_dir = root_dir / "benchmarks" / "tasks"
    collector = MetricCollector(suite_version="1.0.0")

    task_dirs = sorted([d for d in tasks_dir.iterdir() if d.is_dir()])
    print(f"[*] Discovered {len(task_dirs)} benchmark tasks.")

    for t_dir in task_dirs:
        task_meta_file = t_dir / "task.json"
        if not task_meta_file.exists():
            continue

        with open(task_meta_file, "r", encoding="utf8") as f:
            meta = json.load(f)

        if task_filter and task_filter not in meta["id"]:
            continue

        print(f" -> Running task [{meta['id']}] in mode '{mode}'...")
        passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode=mode)
        
        patch_correctness = "CORRECT" if passed else ("FAILED" if mode == "buggy" else "INCOMPLETE")
        collector.record_task_result(
            task_id=meta["id"],
            title=meta["title"],
            mode=mode,
            passed=passed,
            test_pass_rate=pass_rate,
            duration=duration,
            patch_correctness=patch_correctness,
            notes=f"Evaluated with exit code {'0' if passed else 'non-zero'} in {round(duration, 3)}s"
        )
        status_str = "PASS" if passed else "FAIL (Expected for buggy baseline)"
        print(f"    Result: {status_str} in {round(duration, 3)}s")

    report = collector.export_report()
    return report

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "reference"
    report = run_suite(mode=mode_arg)
    print(json.dumps(report, indent=2))
