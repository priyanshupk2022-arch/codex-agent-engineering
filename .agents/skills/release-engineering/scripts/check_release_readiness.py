import sys
from pathlib import Path

def check_readiness(root: Path, target_version: str) -> dict:
    issues = []
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        issues.append("Missing CHANGELOG.md")
    else:
        content = changelog.read_text(encoding="utf8")
        if target_version not in content:
            issues.append(f"Version {target_version} not documented in CHANGELOG.md")
            
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        p_content = pyproject.read_text(encoding="utf8")
        if f'version = "{target_version}"' not in p_content:
            issues.append(f"Version {target_version} does not match pyproject.toml")
            
    return {"version": target_version, "ready": len(issues) == 0, "issues": issues}

if __name__ == "__main__":
    ver = sys.argv[1] if len(sys.argv) > 1 else "0.1.1"
    res = check_readiness(Path("."), ver)
    print(f"Release Readiness for v{res['version']}: {'READY' if res['ready'] else 'NOT READY'}")
    if res["issues"]:
        for i in res["issues"]: print(f" - [FAIL] {i}")
        sys.exit(1)
    else:
        print("[+] All release prerequisites satisfied.")
        sys.exit(0)
