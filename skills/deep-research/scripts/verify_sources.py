import sys
import json
from pathlib import Path

def verify_provenance(provenance_path: Path) -> dict:
    if not provenance_path.exists():
        return {"status": "ERROR", "message": f"File not found: {provenance_path}"}
        
    data = json.loads(provenance_path.read_text(encoding="utf8"))
    records = data.get("records", [])
    valid_types = {"official", "maintainer", "paper", "benchmark", "experiment", "community"}
    errors = []
    
    for r in records:
        rid = r.get("id", "UNKNOWN")
        if not r.get("title"): errors.append(f"{rid}: Missing title")
        if r.get("source_type") not in valid_types: errors.append(f"{rid}: Invalid source_type '{r.get('source_type')}'")
        if not r.get("url"): errors.append(f"{rid}: Missing url")
        conf = r.get("confidence", 0.0)
        if not (0.0 <= conf <= 1.0): errors.append(f"{rid}: Confidence {conf} outside [0.0, 1.0]")
            
    return {
        "status": "VALID" if not errors else "INVALID",
        "total_records": len(records),
        "error_count": len(errors),
        "errors": errors
    }

if __name__ == "__main__":
    p_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("sources/provenance.json")
    res = verify_provenance(p_path)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "VALID" else 1)
