"""
CAE Skills Synchronization Validator
Enforces synchronization between canonical skills (skills/) and the Codex/AI-DLC
projection path (.agents/skills/). Prevents silently divergent skill copies.
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_canonical_skills(source_dir: Path) -> List[Path]:
    """Retrieve all directories in source_dir containing SKILL.md."""
    if not source_dir.exists():
        return []
    return sorted([d for d in source_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])


IGNORE_NAMES = {"__pycache__", ".DS_Store"}


def is_ignored(rel_path: Path) -> bool:
    """Check if relative path should be ignored (e.g. cache or compiled files)."""
    for part in rel_path.parts:
        if part in IGNORE_NAMES or part.endswith(".pyc") or part.endswith(".pyo"):
            return True
    return False


def sync_skills(source_dir: Path, target_dir: Path) -> None:
    """Project all canonical skills into target directory."""
    target_dir.mkdir(parents=True, exist_ok=True)
    canonical = get_canonical_skills(source_dir)
    print(f"[*] Projecting {len(canonical)} canonical skills to {target_dir.relative_to(ROOT_DIR)}...")

    for s_dir in canonical:
        dest_dir = target_dir / s_dir.name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(s_dir, dest_dir, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"))
        print(f" [+] Projected: {s_dir.name} -> {dest_dir.relative_to(ROOT_DIR)}")


def compare_directories(dir1: Path, dir2: Path) -> Tuple[bool, List[str]]:
    """Recursively compare two directories for byte-identical files."""
    mismatches = []
    
    # Collect relative files from dir1, ignoring caches
    files1 = {p.relative_to(dir1) for p in dir1.rglob("*") if p.is_file() and not is_ignored(p.relative_to(dir1))}
    files2 = {p.relative_to(dir2) for p in dir2.rglob("*") if p.is_file() and not is_ignored(p.relative_to(dir2))}

    missing_in_2 = files1 - files2
    extra_in_2 = files2 - files1

    for m in missing_in_2:
        mismatches.append(f"Missing in projection: {m}")
    for e in extra_in_2:
        mismatches.append(f"Unexpected in projection: {e}")

    # Check content of common files
    common = files1 & files2
    for c in common:
        f1 = dir1 / c
        f2 = dir2 / c
        if not filecmp.cmp(f1, f2, shallow=False):
            mismatches.append(f"Content divergence: {c}")

    return len(mismatches) == 0, mismatches


def check_skill_sync(source_dir: Path, target_dir: Path) -> bool:
    """Verify that every canonical skill matches its projected copy."""
    canonical = get_canonical_skills(source_dir)
    if not canonical:
        print("[!] No canonical skills found in skills/.")
        return False

    all_in_sync = True
    print(f"[*] Checking synchronization for {len(canonical)} canonical skills...")

    for s_dir in canonical:
        proj_dir = target_dir / s_dir.name
        if not proj_dir.exists():
            print(f"[FAIL] Missing projection for skill: {s_dir.name} (expected at {proj_dir.relative_to(ROOT_DIR)})")
            all_in_sync = False
            continue

        match, diffs = compare_directories(s_dir, proj_dir)
        if not match:
            print(f"[FAIL] Divergence detected in skill projection: {s_dir.name}")
            for d in diffs:
                print(f"       - {d}")
            all_in_sync = False
        else:
            print(f"[OK] In-sync: {s_dir.name}")

    if all_in_sync:
        print("[+] All canonical skills are in perfect synchronization with .agents/skills/ projection.")
    else:
        print("\n[!] Skills projection out of sync.")
        print("    Run 'python scripts/check_skill_sync.py --sync' to re-project canonical skills.")

    return all_in_sync


def main():
    parser = argparse.ArgumentParser(description="Check or synchronize canonical skills to .agents/skills/")
    parser.add_argument("--sync", action="store_true", help="Synchronize canonical skills to projection directory")
    args = parser.parse_args()

    source = ROOT_DIR / "skills"
    target = ROOT_DIR / ".agents" / "skills"

    if args.sync:
        sync_skills(source, target)

    in_sync = check_skill_sync(source, target)
    sys.exit(0 if in_sync else 1)


if __name__ == "__main__":
    main()
