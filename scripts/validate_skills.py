import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Overview",
    "## When to Use",
    "## Inputs",
    "## Workflow",
    "## Outputs & Deliverables",
    "## Constraints & Guardrails",
    "## Verification Protocol",
    "## Common Failure Modes & Recovery"
]

def validate_skills(skills_dir: Path) -> bool:
    skills = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skills:
        print("[!] No skills found in skills/ directory.")
        return False

    all_valid = True
    print(f"[*] Validating {len(skills)} skills against schema...")

    for s in sorted(skills):
        skill_file = s / "SKILL.md"
        if not skill_file.exists():
            print(f"[FAIL] {s.name}: Missing SKILL.md")
            all_valid = False
            continue

        content = skill_file.read_text(encoding="utf8")
        missing = [h for h in REQUIRED_HEADINGS if h not in content]
        if missing:
            print(f"[FAIL] {s.name}: Missing required headings: {missing}")
            all_valid = False
        else:
            print(f"[OK] {s.name}")

    return all_valid

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    success = validate_skills(root / "skills")
    sys.exit(0 if success else 1)
