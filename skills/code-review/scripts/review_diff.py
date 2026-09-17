import sys
import subprocess
import re

def review_staged_diff() -> dict:
    cmd = ["git", "diff", "HEAD"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0: return {"status": "ERROR", "message": proc.stderr}
    diff = proc.stdout
    findings = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            if re.search(r"\bprint\s*\(", line):
                findings.append({"type": "WARN", "message": f"Debug print() statement found: {line.strip()}"})
            if re.search(r"(api_key|password|secret|token)\s*=\s*['\"][^'\"]+['\"]", line, re.IGNORECASE):
                findings.append({"type": "CRITICAL", "message": f"Potential hardcoded credential: {line.strip()}"})
            if re.search(r"\bdebugger\b|\bbreakpoint\s*\(", line):
                findings.append({"type": "CRITICAL", "message": f"Debugger breakpoint found: {line.strip()}"})
                
    return {"status": "PASS" if not findings else "REVIEW_NEEDED", "findings_count": len(findings), "findings": findings}

if __name__ == "__main__":
    res = review_staged_diff()
    print(f"Diff Review Status: {res['status']}")
    if res["findings"]:
        for f in res["findings"]: print(f" - [{f['type']}] {f['message']}")
        sys.exit(1 if any(f['type'] == 'CRITICAL' for f in res['findings']) else 0)
    else:
        print("[+] No anti-patterns detected in current diff.")
        sys.exit(0)
