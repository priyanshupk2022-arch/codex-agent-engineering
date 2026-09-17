from pathlib import Path
from benchmarks.runners.evaluator import TaskEvaluator

ROOT = Path(__file__).resolve().parent.parent

def test_evaluator_reference_task_001():
    t_dir = ROOT / "benchmarks" / "tasks" / "cae-task-001-deadlock"
    passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode="reference")
    assert passed is True
    assert pass_rate == 1.0
    assert duration > 0

def test_evaluator_buggy_task_001():
    t_dir = ROOT / "benchmarks" / "tasks" / "cae-task-001-deadlock"
    passed, pass_rate, duration, log = TaskEvaluator.evaluate_task(t_dir, solution_mode="buggy")
    assert passed is False
    assert pass_rate == 0.0
