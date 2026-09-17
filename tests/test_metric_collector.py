from benchmarks.metrics.collector import MetricCollector

def test_metric_collector_aggregation():
    collector = MetricCollector(suite_version="1.0.0")
    collector.record_task_result(
        task_id="test-1",
        title="Sample Task",
        mode="reference",
        passed=True,
        test_pass_rate=1.0,
        duration=1.25,
        patch_correctness="CORRECT"
    )
    collector.record_task_result(
        task_id="test-2",
        title="Sample Task 2",
        mode="buggy",
        passed=False,
        test_pass_rate=0.0,
        duration=0.75,
        patch_correctness="FAILED"
    )

    report = collector.export_report()
    assert report["summary"]["total_tasks"] == 2
    assert report["summary"]["total_passed"] == 1
    assert report["summary"]["pass_rate"] == 0.5
    assert report["summary"]["mean_duration_seconds"] == 1.0


def test_metric_collector_multi_iterations_and_flakiness():
    """Verify flakiness detection, flake rate, median, and p95 across iterations."""
    collector = MetricCollector(suite_version="1.0.0", iterations=2)

    # Task 1 passes both iterations (stable)
    collector.record_task_result("task-1", "Task 1", "reference", passed=True, test_pass_rate=1.0, duration=1.0, iterations=1)
    collector.record_task_result("task-1", "Task 1", "reference", passed=True, test_pass_rate=1.0, duration=1.2, iterations=2)

    # Task 2 passes iter 1 but fails iter 2 (flaky!)
    collector.record_task_result("task-2", "Task 2", "reference", passed=True, test_pass_rate=1.0, duration=0.8, iterations=1)
    collector.record_task_result("task-2", "Task 2", "reference", passed=False, test_pass_rate=0.0, duration=2.5, iterations=2)

    report = collector.export_report()
    summary = report["summary"]

    assert summary["total_tasks"] == 2  # 2 unique tasks
    assert summary["total_passed"] == 1  # Only task-1 passed all iterations
    assert summary["pass_rate"] == 0.75  # 3 of 4 runs passed
    assert summary["failure_rate"] == 0.25
    assert summary["flake_rate"] == 0.5  # 1 of 2 unique tasks is flaky
    assert summary["median_duration_seconds"] > 0
    assert summary["p95_duration_seconds"] >= 2.0
    assert summary["iterations"] == 2

