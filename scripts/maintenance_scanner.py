import sys
import json
from pathlib import Path

def scan_maintenance(root_dir: Path) -> dict:
    print("[*] Running CAE Automated Maintenance Scanner...")
    issues = []

    # 1. Check required root files
    required_roots = ["README.md", "AGENTS.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"]
    for rf in required_roots:
        if not (root_dir / rf).exists():
            issues.append({"severity": "FATAL", "item": rf, "message": f"Missing core root file {rf}"})

    # 2. Check benchmarks presence
    bm_tasks = list((root_dir / "benchmarks" / "tasks").glob("*/task.json"))
    if len(bm_tasks) < 5:
        issues.append({"severity": "HIGH", "item": "benchmarks", "message": f"Fewer than 5 benchmark tasks found ({len(bm_tasks)})"})

    # 3. Check skills presence
    skills = list((root_dir / "skills").glob("*/SKILL.md"))
    if len(skills) < 9:
        issues.append({"severity": "HIGH", "item": "skills", "message": f"Fewer than 9 skills found ({len(skills)})"})

    # 4. Check provenance json
    prov_file = root_dir / "sources" / "provenance.json"
    if not prov_file.exists():
        issues.append({"severity": "HIGH", "item": "provenance", "message": "Missing sources/provenance.json"})
    else:
        try:
            with open(prov_file, "r", encoding="utf8") as f:
                data = json.load(f)
                if not data.get("records"):
                    issues.append({"severity": "MEDIUM", "item": "provenance", "message": "Zero records in provenance.json"})
        except Exception as e:
            issues.append({"severity": "HIGH", "item": "provenance", "message": f"Invalid provenance.json: {e}"})

    status = "HEALTHY" if not issues else "NEEDS_ATTENTION"
    report = {
        "status": status,
        "total_issues": len(issues),
        "issues": issues
    }
    print(f"[*] Scan complete: Status={status}, Issues={len(issues)}")
    return report

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    report = scan_maintenance(root)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["status"] == "HEALTHY" else 1)
