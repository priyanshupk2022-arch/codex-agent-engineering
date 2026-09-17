import os
import sys
import json
from pathlib import Path

def audit_directory(target_path: Path) -> dict:
    summary = {
        "path": str(target_path.resolve()),
        "file_counts": {},
        "total_files": 0,
        "indicators": {
            "has_license": False,
            "has_readme": False,
            "has_security_policy": False,
            "has_ci": False,
            "runtimes": []
        }
    }
    ignored = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".pytest_cache"}
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in ignored]
        for f in files:
            summary["total_files"] += 1
            ext = Path(f).suffix.lower() or "no_extension"
            summary["file_counts"][ext] = summary["file_counts"].get(ext, 0) + 1
            upper = f.upper()
            if "LICENSE" in upper: summary["indicators"]["has_license"] = True
            elif "README" in upper: summary["indicators"]["has_readme"] = True
            elif "SECURITY" in upper: summary["indicators"]["has_security_policy"] = True

    if (target_path / "pyproject.toml").exists() or ".py" in summary["file_counts"]:
        summary["indicators"]["runtimes"].append("Python")
    if (target_path / "package.json").exists() or ".ts" in summary["file_counts"] or ".js" in summary["file_counts"]:
        summary["indicators"]["runtimes"].append("Node/TypeScript")
    if (target_path / "Cargo.toml").exists() or ".rs" in summary["file_counts"]:
        summary["indicators"]["runtimes"].append("Rust")
    if (target_path / "go.mod").exists() or ".go" in summary["file_counts"]:
        summary["indicators"]["runtimes"].append("Go")
    if (target_path / ".github" / "workflows").exists():
        summary["indicators"]["has_ci"] = True
    return summary

if __name__ == "__main__":
    t = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(audit_directory(t), indent=2))
