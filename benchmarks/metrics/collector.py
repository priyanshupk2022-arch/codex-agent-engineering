import json
import math
import platform
import statistics
import time
from typing import Dict, Any, List, Optional


def calculate_p95(values: List[float]) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    idx = int(math.ceil(0.95 * len(sorted_v))) - 1
    idx = max(0, min(idx, len(sorted_v) - 1))
    return round(sorted_v[idx], 4)


class MetricCollector:
    def __init__(self, suite_version: str = "1.0.0", iterations: int = 1):
        self.suite_version = suite_version
        self.iterations = iterations
        self.start_time = time.time()
        self.results: List[Dict[str, Any]] = []

    def record_task_result(
        self,
        task_id: str,
        title: str,
        mode: str,
        passed: bool,
        test_pass_rate: float,
        duration: float,
        iterations: int = 1,
        tool_calls: int = 0,
        regressions: int = 0,
        security_resolved: int = 0,
        patch_correctness: str = "CORRECT",
        notes: str = ""
    ):
        self.results.append({
            "task_id": task_id,
            "title": title,
            "mode": mode,
            "passed": passed,
            "test_pass_rate": round(test_pass_rate, 4),
            "execution_time_seconds": round(duration, 4),
            "iterations": iterations,
            "tool_calls": tool_calls,
            "regressions_detected": regressions,
            "security_findings_resolved": security_resolved,
            "patch_correctness": patch_correctness,
            "notes": notes
        })

    def export_report(self) -> Dict[str, Any]:
        total_runs = len(self.results)
        if total_runs == 0:
            return {
                "suite_version": self.suite_version,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "environment": {
                    "os": platform.system() + " " + platform.release(),
                    "python_version": platform.python_version(),
                    "runner": "cae-benchmark-runner/1.0.0"
                },
                "tasks": [],
                "summary": {
                    "total_tasks": 0,
                    "total_passed": 0,
                    "pass_rate": 0.0,
                    "failure_rate": 0.0,
                    "flake_rate": 0.0,
                    "mean_duration_seconds": 0.0,
                    "median_duration_seconds": 0.0,
                    "p95_duration_seconds": 0.0,
                    "iterations": self.iterations
                }
            }

        # Aggregate task results by task_id to compute flakiness
        tasks_map: Dict[str, List[Dict[str, Any]]] = {}
        for r in self.results:
            tasks_map.setdefault(r["task_id"], []).append(r)

        unique_tasks_count = len(tasks_map)
        flaky_tasks_count = 0
        for tid, runs in tasks_map.items():
            pass_count = sum(1 for r in runs if r["passed"])
            if 0 < pass_count < len(runs):
                flaky_tasks_count += 1

        passed_runs_count = sum(1 for r in self.results if r["passed"])
        pass_rate = round(passed_runs_count / total_runs, 4)
        failure_rate = round(1.0 - pass_rate, 4)
        flake_rate = round(flaky_tasks_count / unique_tasks_count, 4) if unique_tasks_count > 0 else 0.0

        durations = [r["execution_time_seconds"] for r in self.results]
        mean_dur = round(statistics.mean(durations), 4) if durations else 0.0
        median_dur = round(statistics.median(durations), 4) if durations else 0.0
        p95_dur = calculate_p95(durations)

        # For single iteration or backward-compatibility, tasks is self.results
        return {
            "suite_version": self.suite_version,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "environment": {
                "os": platform.system() + " " + platform.release(),
                "python_version": platform.python_version(),
                "runner": "cae-benchmark-runner/1.0.0"
            },
            "tasks": self.results,
            "summary": {
                "total_tasks": total_runs if self.iterations == 1 else unique_tasks_count,
                "total_passed": passed_runs_count if self.iterations == 1 else sum(1 for runs in tasks_map.values() if all(r["passed"] for r in runs)),
                "pass_rate": pass_rate,
                "failure_rate": failure_rate,
                "flake_rate": flake_rate,
                "mean_duration_seconds": mean_dur,
                "median_duration_seconds": median_dur,
                "p95_duration_seconds": p95_dur,
                "iterations": self.iterations
            }
        }
