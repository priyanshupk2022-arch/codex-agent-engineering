import sys
import subprocess
from pathlib import Path

def check_scope(allowed_prefixes: list) -> dict:
    cmd = ["git", "status", "--porcelain"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        return {"status": "ERROR", "message": proc.stderr.strip()}
        
    lines = proc.stdout.strip().splitlines()
    modified_files = []
    out_of_scope = []
    
    for l in lines:
        if len(l) < 4: continue
        file_path = l[3:].strip()
        if " -> " in file_path: file_path = file_path.split(" -> ")[1].strip()
        modified_files.append(file_path)
        if allowed_prefixes:
            if not any(file_path.startswith(prefix) for prefix in allowed_prefixes):
                out_of_scope.append(file_path)
                
    return {
        "status": "FAIL" if out_of_scope else "PASS",
        "total_modified": len(modified_files),
        "modified_files": modified_files,
        "out_of_scope_files": out_of_scope
    }

if __name__ == "__main__":
    allowed = sys.argv[1:] if len(sys.argv) > 1 else []
    res = check_scope(allowed)
    print(f"Modified files ({res['total_modified']}):")
    for f in res["modified_files"]: print(f" - {f}")
    if res["out_of_scope_files"]:
        print("
[!] OUT OF SCOPE MODIFICATIONS DETECTED:")
        for f in res["out_of_scope_files"]: print(f" [!] {f}")
        sys.exit(1)
    print("
[+] All changes within permitted scope.")
    sys.exit(0)
