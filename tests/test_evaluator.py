from pathlib import Path
from benchmarks.runners.evaluator import TaskEvaluator

ROOT = Path(__file__).resolve().parent.parent

def test_evaluator_all_reference_tasks():
    tasks_dir = ROOT / "benchmarks" / "tasks"
    task_dirs = sorted([d for d in tasks_dir.iterdir() if d.is_dir()])
    assert len(task_dirs) == 5

    for t_dir in task_dirs:
        passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode="reference")
        assert passed is True, f"Task {t_dir.name} failed in reference mode: {log}"
        assert pass_rate == 1.0
        assert duration > 0

def test_evaluator_all_buggy_tasks():
    tasks_dir = ROOT / "benchmarks" / "tasks"
    task_dirs = sorted([d for d in tasks_dir.iterdir() if d.is_dir()])
    assert len(task_dirs) == 5

    for t_dir in task_dirs:
        passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode="buggy")
        assert passed is False, f"Buggy baseline for {t_dir.name} unexpectedly passed!"
        assert pass_rate == 0.0
