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
