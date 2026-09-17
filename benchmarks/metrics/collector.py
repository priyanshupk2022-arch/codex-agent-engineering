import json
import time
import platform
from typing import Dict, Any, List

class MetricCollector:
    def __init__(self, suite_version: str = "1.0.0"):
        self.suite_version = suite_version
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
        total = len(self.results)
        passed_count = sum(1 for r in self.results if r["passed"])
        pass_rate = round(passed_count / total, 4) if total > 0 else 0.0
        durations = [r["execution_time_seconds"] for r in self.results]
        mean_duration = round(sum(durations) / total, 4) if total > 0 else 0.0

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
                "total_tasks": total,
                "total_passed": passed_count,
                "pass_rate": pass_rate,
                "mean_duration_seconds": mean_duration
            }
        }
