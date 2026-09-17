"""
Robustness and Error Handling Unit Tests
Tests failure paths, malformed tasks, subprocess timeouts, missing executables,
corrupted metadata, and boundary error conditions.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter
from benchmarks.runners.evaluator import TaskEvaluator
from benchmarks.runners.runner import run_suite
from benchmarks.runners.agent_runner import run_agent_evaluation


def test_missing_codex_binary():
    """Adapter must gracefully report unavailability without raising exceptions."""
    adapter = CodexCliAdapter(executable="nonexistent_binary_xyz_12345")
    assert adapter.is_available() is False
    assert adapter.get_version() is None

    res = adapter.execute_prompt("test", cwd=ROOT)
    assert res["success"] is False
    assert res["exit_code"] is None
    assert "not found in PATH" in res["stderr"]


def test_agent_eval_skipped_when_codex_unavailable(tmp_path):
    """Agent runner must produce AGENT_EVAL_SKIPPED result without fabricating data."""
    dummy_adapter = CodexCliAdapter(executable="nonexistent_codex_xyz")
    res = run_agent_evaluation(
        output_dir=tmp_path,
        adapter=dummy_adapter
    )
    assert res["status"] == "AGENT_EVAL_SKIPPED"
    assert "not found in system PATH" in res["skip_reason"]
    assert res["summary"]["vanilla_passed"] == 0
    assert res["summary"]["cae_passed"] == 0
    assert (tmp_path / "metadata.json").exists()


def test_evaluator_missing_task_implementation(tmp_path):
    """TaskEvaluator must raise FileNotFoundError if source implementation is missing."""
    task_json = tmp_path / "task.json"
    task_json.write_text(json.dumps({
        "target_file": "missing.py",
        "test_file": "test_missing.py"
    }), encoding="utf8")

    with pytest.raises(FileNotFoundError):
        TaskEvaluator.evaluate_task(tmp_path, solution_mode="reference")


def test_evaluator_malformed_task_json(tmp_path):
    """TaskEvaluator must raise ValueError/JSONDecodeError on malformed JSON."""
    task_json = tmp_path / "task.json"
    task_json.write_text("{ unclosed json", encoding="utf8")

    with pytest.raises(json.JSONDecodeError):
        TaskEvaluator.evaluate_task(tmp_path, solution_mode="reference")


def test_evaluator_timeout_handling(tmp_path):
    """TaskEvaluator must catch subprocess timeout and mark task as failed without hanging."""
    task_json = tmp_path / "task.json"
    task_json.write_text(json.dumps({
        "target_file": "hang.py",
        "test_file": "test_hang.py"
    }), encoding="utf8")

    # Write an infinite loop test
    test_hang = tmp_path / "test_hang.py"
    test_hang.write_text("import time\ndef test_infinite():\n    time.sleep(30)\n", encoding="utf8")

    hang_ref = tmp_path / "hang_reference.py"
    hang_ref.write_text("# dummy", encoding="utf8")

    # In TaskEvaluator, default timeout is 15s. Let's monkeypatch or run it
    import benchmarks.runners.evaluator as ev_mod
    original_eval = TaskEvaluator.evaluate_task

    # Evaluate with low timeout directly
    passed, rate, dur, log = TaskEvaluator.evaluate_task(tmp_path, solution_mode="reference")
    assert passed is False
    assert rate == 0.0
    assert "timed out" in log.lower()


def test_runner_filter_nonexistent_task():
    """Runner with a filter matching 0 tasks should return empty summary cleanly."""
    res = run_suite(mode="reference", task_filter="nonexistent_task_xyz")
    assert res["summary"]["total_tasks"] == 0
    assert res["summary"]["pass_rate"] == 0.0


def test_skill_sync_detection_on_tampered_dir(tmp_path):
    """check_skill_sync logic must detect missing files in projection."""
    from scripts.check_skill_sync import compare_directories

    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()

    (dir1 / "file.txt").write_text("content A", encoding="utf8")
    (dir2 / "file.txt").write_text("content B", encoding="utf8")

    match, diffs = compare_directories(dir1, dir2)
    assert match is False
    assert any("Content divergence" in d for d in diffs)
