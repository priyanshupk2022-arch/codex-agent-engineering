import sys
import re
from pathlib import Path

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z]+ PRIVATE KEY-----"), "Private Key Header"),
    (re.compile(r"(?i)(api[_-]?key|secret|password|auth[_-]?token)\s*=\s*['"][0-9a-zA-Z\-_]{16,}['"]"), "High-Entropy Secret String"),
    (re.compile(r"ghp_[0-9a-zA-Z]{36}"), "GitHub Personal Access Token"),
    (re.compile(r"sk-[0-9a-zA-Z]{32,}"), "OpenAI API Key"),
    (re.compile(r"(?i)bearer\s+[0-9a-zA-Z\-_\.]{20,}"), "Bearer Token"),
]

def scan_file(file_path: Path) -> list:
    findings = []
    try:
        content = file_path.read_text(encoding="utf8", errors="ignore")
        for lineno, line in enumerate(content.splitlines(), start=1):
            for pattern, desc in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append({"file": str(file_path), "line": lineno, "description": desc, "snippet": line.strip()[:60]})
    except Exception: pass
    return findings

def scan_repo(target_dir: Path) -> list:
    all_findings = []
    ignored = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}
    for p in target_dir.rglob("*"):
        if p.is_file() and not any(part in ignored for part in p.parts):
            if p.suffix in (".py", ".js", ".ts", ".json", ".toml", ".yml", ".yaml", ".env", ".sh"):
                all_findings.extend(scan_file(p))
    return all_findings

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    findings = scan_repo(target)
    if findings:
        print(f"[!] Found {len(findings)} potential security issues:")
        for f in findings: print(f" - [{f['description']}] {f['file']}:{f['line']} -> {f['snippet']}")
        sys.exit(1)
    else:
        print("[+] No credentials or plaintext secrets found.")
        sys.exit(0)
