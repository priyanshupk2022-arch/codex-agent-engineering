import sys
from pathlib import Path

def check_test_pairing(src_dir: Path, test_dir: Path) -> dict:
    if not src_dir.exists() or not test_dir.exists():
        return {"status": "ERROR", "message": "Directories do not exist"}
        
    src_files = [f for f in src_dir.rglob("*.py") if not f.name.startswith("__") and not f.name.startswith("test_")]
    test_files = [f for f in test_dir.rglob("*.py") if f.name.startswith("test_")]
    test_names = {f.name for f in test_files}
    
    paired = []
    unpaired = []
    
    for sf in src_files:
        expected = f"test_{sf.name}"
        if expected in test_names: paired.append((sf.name, expected))
        else: unpaired.append(sf.name)
            
    return {
        "total_source_files": len(src_files),
        "paired_count": len(paired),
        "unpaired_count": len(unpaired),
        "unpaired_files": unpaired
    }

if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scripts")
    tst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("tests")
    res = check_test_pairing(src, tst)
    print(f"Source files checked: {res['total_source_files']}")
    print(f"Paired with tests:    {res['paired_count']}")
    print(f"Unpaired:             {res['unpaired_count']}")
    if res["unpaired_files"]:
        print("
Unpaired source modules:")
        for u in res["unpaired_files"]: print(f" - {u}")
