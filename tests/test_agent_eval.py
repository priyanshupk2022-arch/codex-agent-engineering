"""
Unit tests for CAE Agent Evaluation Architecture and Schema Enforcement.
Tests schema validity, evidence file layout (metadata.json, result.json, logs, diffs, tests),
mock multi-turn execution, and forbidden shortcut / test tampering defense.
"""

import json
import shutil
from pathlib import Path
import pytest
import jsonschema

ROOT = Path(__file__).resolve().parent.parent

from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter
from benchmarks.runners.agent_runner import run_agent_evaluation
from benchmarks.agents.vanilla_codex import VanillaCodexAgent
from benchmarks.agents.cae_codex import CaeCodexAgent


def test_agent_eval_schema_valid():
    """Verify that agent_eval_schema.json is a syntactically valid Draft-07 schema."""
    schema_path = ROOT / "benchmarks" / "metrics" / "agent_eval_schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf8"))
    jsonschema.Draft7Validator.check_schema(schema)


def test_agent_eval_skipped_conforms_to_schema_and_layout(tmp_path):
    """
    Verify that skipped evaluations produce compliant metadata.json and
    generate all required evidence files (result.json, logs, patch, tests.json).
    """
    schema = json.loads((ROOT / "benchmarks" / "metrics" / "agent_eval_schema.json").read_text(encoding="utf8"))
    dummy_adapter = CodexCliAdapter(executable="nonexistent_codex_bin_xyz")

    report = run_agent_evaluation(
        task_filter="cae-task-002-sql-injection",
        output_dir=tmp_path,
        adapter=dummy_adapter
    )

    # Validate JSON schema conformance
    jsonschema.validate(instance=report, schema=schema)

    # Validate metadata.json on disk
    meta_file = tmp_path / "metadata.json"
    assert meta_file.exists()
    disk_data = json.loads(meta_file.read_text(encoding="utf8"))
    jsonschema.validate(instance=disk_data, schema=schema)

    # Validate root-level evidence layout per Phase 1-D
    for agent_dir_name in ["vanilla", "cae"]:
        agent_dir = tmp_path / agent_dir_name
        assert agent_dir.exists(), f"Missing root {agent_dir_name} directory"
        assert (agent_dir / "result.json").exists()
        assert (agent_dir / "stdout.log").exists()
        assert (agent_dir / "stderr.log").exists()
        assert (agent_dir / "diff.patch").exists()
        assert (agent_dir / "tests.json").exists()

        res_data = json.loads((agent_dir / "result.json").read_text(encoding="utf8"))
        assert res_data["status"] == "SKIPPED"
        assert res_data["passed"] is False


class MockSuccessAdapter(CodexCliAdapter):
    """Mock adapter simulating an agent that replaces the buggy target with the fixed code."""
    def __init__(self, task_dir: Path, target_name: str, fixed_name: str):
        super().__init__(executable="mock-codex")
        self.task_dir = task_dir
        self.target_name = target_name
        self.fixed_name = fixed_name

    def is_available(self) -> bool:
        return True

    def get_version(self) -> str:
        return "mock-codex-1.0.0"

    def execute_prompt(self, prompt: str, cwd: Path, approval_policy: str = "never", timeout: float = 120.0, extra_args=None):
        fixed_source = self.task_dir / self.fixed_name
        target_path = cwd / self.target_name
        shutil.copyfile(fixed_source, target_path)
        return {
            "success": True,
            "exit_code": 0,
            "stdout": f"Mock agent modified {self.target_name} successfully.",
            "stderr": "",
            "duration": 0.15,
            "timed_out": False,
            "error": None
        }


def test_agent_eval_mock_execution_conforms_to_schema(tmp_path):
    """
    Verify that an active agent execution run produces passing results,
    generates unified diffs, writes result.json, and satisfies agent_eval_schema.json.
    """
    schema = json.loads((ROOT / "benchmarks" / "metrics" / "agent_eval_schema.json").read_text(encoding="utf8"))
    task_dir = ROOT / "benchmarks" / "tasks" / "cae-task-002-sql-injection"

    mock_adapter = MockSuccessAdapter(
        task_dir=task_dir,
        target_name="product_repo.py",
        fixed_name="product_repo_fixed.py"
    )

    report = run_agent_evaluation(
        task_filter="cae-task-002-sql-injection",
        output_dir=tmp_path,
        adapter=mock_adapter
    )

    assert report["status"] == "COMPLETED"
    assert report["summary"]["vanilla_passed"] == 1
    assert report["summary"]["cae_passed"] == 1
    jsonschema.validate(instance=report, schema=schema)

    # Check evidence artifacts
    for agent_name in ["vanilla", "cae"]:
        agent_dir = tmp_path / agent_name
        assert (agent_dir / "result.json").exists()
        res_json = json.loads((agent_dir / "result.json").read_text(encoding="utf8"))
        assert res_json["passed"] is True
        assert res_json["patch_correctness"] == "CORRECT"
        assert "product_repo.py" in res_json["changed_files"]
        assert len(res_json["final_state"]) > 0

        diff_text = (agent_dir / "diff.patch").read_text(encoding="utf8")
        assert "--- a/product_repo.py" in diff_text
        assert "+++ b/product_repo.py" in diff_text


class MockTamperingAdapter(CodexCliAdapter):
    """Mock adapter that maliciously tampers with the test suite to fake a pass."""
    def __init__(self, test_name: str):
        super().__init__(executable="mock-tamper-codex")
        self.test_name = test_name

    def is_available(self) -> bool:
        return True

    def get_version(self) -> str:
        return "mock-tamper-1.0.0"

    def execute_prompt(self, prompt: str, cwd: Path, approval_policy: str = "never", timeout: float = 120.0, extra_args=None):
        # Maliciously overwrite test suite with trivial pass
        tampered_test = cwd / self.test_name
        tampered_test.write_text("def test_bypass():\n    assert True\n", encoding="utf8")
        return {
            "success": True,
            "exit_code": 0,
            "stdout": "Tampered test suite.",
            "stderr": "",
            "duration": 0.05,
            "timed_out": False,
            "error": None
        }


def test_agent_forbidden_shortcut_test_tampering_detected(tmp_path):
    """
    Verify that if an agent attempts to tamper with or modify the test harness,
    BaseBenchmarkAgent catches it as a forbidden shortcut, fails the run, and rejects the patch.
    """
    task_dir = ROOT / "benchmarks" / "tasks" / "cae-task-002-sql-injection"
    tamper_adapter = MockTamperingAdapter(test_name="test_product_repo.py")

    agent = VanillaCodexAgent(adapter=tamper_adapter)
    res = agent.run_task(task_dir, tmp_path / "tamper_workspace")

    assert res["passed"] is False
    assert res["test_pass_rate"] == 0.0
    assert res["patch_correctness"] == "FORBIDDEN_SHORTCUT"
    assert "FORBIDDEN_SHORTCUT_DETECTED" in res["test_output"]
