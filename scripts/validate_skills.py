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
            continue

        # Validate scripts presence
        scripts_dir = s / "scripts"
        scripts = list(scripts_dir.glob("*.py")) if scripts_dir.exists() else []
        if not scripts:
            print(f"[FAIL] {s.name}: Missing executable python script in scripts/")
            all_valid = False
            continue

        # Validate references checklist
        checklist = s / "references" / "checklist.md"
        if not checklist.exists() or len(checklist.read_text(encoding="utf8").strip()) < 200:
            print(f"[FAIL] {s.name}: Missing or trivial references/checklist.md (<200 bytes)")
            all_valid = False
            continue

        # Validate sample output example
        sample_output = s / "examples" / "sample-output.md"
        if not sample_output.exists() or len(sample_output.read_text(encoding="utf8").strip()) < 200:
            print(f"[FAIL] {s.name}: Missing or trivial examples/sample-output.md (<200 bytes)")
            all_valid = False
            continue

        print(f"[OK] {s.name} (SKILL.md + {scripts[0].name} + checklist + sample-output)")

    return all_valid

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    success = validate_skills(root / "skills")
    sys.exit(0 if success else 1)
