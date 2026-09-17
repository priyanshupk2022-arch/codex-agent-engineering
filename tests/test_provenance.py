import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_provenance_structure():
    prov_path = ROOT / "sources" / "provenance.json"
    assert prov_path.exists()
    
    data = json.loads(prov_path.read_text(encoding="utf8"))
    assert "version" in data
    assert "records" in data
    assert len(data["records"]) >= 5

    for rec in data["records"]:
        assert "id" in rec
        assert "source_type" in rec
        assert rec["source_type"] in ["official", "maintainer", "paper", "benchmark", "experiment", "community"]
        assert "url" in rec
        assert "confidence" in rec
        assert 0.0 <= rec["confidence"] <= 1.0
