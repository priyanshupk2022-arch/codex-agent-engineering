import sys
from pathlib import Path

def lint_markdown_file(file_path: Path) -> list:
    issues = []
    content = file_path.read_text(encoding="utf8", errors="ignore")
    lines = content.splitlines()
    if not any(line.startswith("# ") for line in lines):
        issues.append(f"{file_path}: Missing top-level # H1 heading")
    for i, line in enumerate(lines):
        if line.strip() == "```" and i > 0 and lines[i-1].strip() == "```":
            issues.append(f"{file_path}:{i+1}: Empty code block detected")
    return issues

def lint_all_docs(root: Path) -> dict:
    total_files = 0
    all_issues = []
    for md in root.rglob("*.md"):
        if any(p in md.parts for p in (".git", ".codex", "node_modules", ".specify", ".pytest_cache")):
            continue
        total_files += 1
        all_issues.extend(lint_markdown_file(md))
    return {"total_files": total_files, "issues_count": len(all_issues), "issues": all_issues}

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    res = lint_all_docs(root)
    print(f"Markdown Doc Linter: Scanned {res['total_files']} files, {res['issues_count']} issues.")
    if res["issues"]:
        for issue in res["issues"]: print(f" - {issue}")
        sys.exit(1)
    else:
        print("[+] All markdown documentation conforms to formatting standards.")
        sys.exit(0)
