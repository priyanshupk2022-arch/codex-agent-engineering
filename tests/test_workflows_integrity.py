from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_all_workflows_have_vanilla_comparison():
    wf_dir = ROOT / "workflows"
    subdirs = [d for d in wf_dir.iterdir() if d.is_dir()]
    assert len(subdirs) >= 10

    for sd in subdirs:
        wf_file = sd / "workflow.md"
        assert wf_file.exists(), f"Missing workflow.md in {sd.name}"
        content = wf_file.read_text(encoding="utf8")
        assert "## Vanilla Codex Comparison" in content, f"Missing vanilla comparison in {sd.name}"
        assert "## 1. Input Specification" in content
        assert "## 7. Verification Protocol" in content
