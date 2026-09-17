from pathlib import Path
from benchmarks.adapters.codex_cli_adapter import CodexCliAdapter

def test_adapter_nonexistent_executable():
    adapter = CodexCliAdapter(executable="nonexistent_codex_bin_12345")
    assert adapter.is_available() is False
    res = adapter.execute_prompt("fix this", Path("."))
    assert res["success"] is False
    assert "not found in PATH" in res["error"]

def test_adapter_initialization_default():
    adapter = CodexCliAdapter()
    assert adapter.executable == "codex"
    # availability reflects local environment
    assert isinstance(adapter.is_available(), bool)
