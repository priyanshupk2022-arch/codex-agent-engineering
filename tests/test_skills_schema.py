from pathlib import Path
from scripts.validate_skills import validate_skills

ROOT = Path(__file__).resolve().parent.parent

def test_all_skills_conform_to_schema():
    assert validate_skills(ROOT / "skills") is True
