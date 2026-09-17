import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import subprocess
import json

def cmd_benchmark(args):
    from benchmarks.runners.runner import run_suite
    mode = args.mode or "reference"
    task_filter = args.task
    if not task_filter and args.suite and args.suite not in ("all", "default", "suite-v1"):
        task_filter = args.suite
    print(f"[*] Running CAE Benchmark Suite ({args.suite or 'default'}) in mode: {mode}")
    report = run_suite(mode=mode, task_filter=task_filter)
    
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2), encoding="utf8")
        print(f"[+] Saved benchmark report to {out_path}")
    else:
        print(json.dumps(report, indent=2))

def cmd_test(args):
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    if args.filter:
        cmd.extend(["-k", args.filter])
    sys.exit(subprocess.run(cmd, cwd=ROOT).returncode)

def cmd_validate_skills(args):
    from scripts.validate_skills import validate_skills
    ok = validate_skills(ROOT / "skills")
    sys.exit(0 if ok else 1)

def cmd_check_links(args):
    from scripts.check_links import check_markdown_links
    ok = check_markdown_links(ROOT)
    sys.exit(0 if ok else 1)

def cmd_doctor(args):
    print("=== Codex Agent Engineering Doctor ===")
    from scripts.maintenance_scanner import scan_maintenance
    report = scan_maintenance(ROOT)
    print(f"Repository Health: {report['status']}")
    if report['issues']:
        for issue in report['issues']:
            print(f" - [{issue['severity']}] {issue['item']}: {issue['message']}")
    else:
        print("[+] All systems green.")
    sys.exit(0 if report['status'] == "HEALTHY" else 1)

def main():
    parser = argparse.ArgumentParser(prog="cae", description="Codex Agent Engineering CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available commands")

    # benchmark
    bm_parser = subparsers.add_parser("benchmark", help="Run reproducible benchmarks")
    bm_parser.add_argument("action", choices=["run", "list"], help="Action to perform")
    bm_parser.add_argument("suite", nargs="?", default="default", help="Suite identifier or task filter (e.g. suite-v1, cae-task-001)")
    bm_parser.add_argument("--mode", choices=["reference", "buggy"], default="reference", help="Evaluation mode")
    bm_parser.add_argument("--task", type=str, default=None, help="Filter by task ID")
    bm_parser.add_argument("--output", "-o", type=str, default=None, help="Output JSON path")

    # test
    t_parser = subparsers.add_parser("test", help="Run test suites")
    t_parser.add_argument("-k", "--filter", type=str, default=None, help="Test filter expression")

    # validate-skills
    subparsers.add_parser("validate-skills", help="Validate skills directory structure")

    # check-links
    subparsers.add_parser("check-links", help="Check markdown internal links")

    # doctor
    subparsers.add_parser("doctor", help="Inspect environment and repository health")

    args = parser.parse_args()

    if args.subcommand == "benchmark":
        if args.action == "list":
            tasks = sorted((ROOT / "benchmarks" / "tasks").glob("*/task.json"))
            print(f"Available tasks ({len(tasks)}):")
            for t in tasks:
                meta = json.loads(t.read_text(encoding="utf8"))
                print(f" - {meta['id']}: {meta['title']} ({meta['category']})")
        else:
            cmd_benchmark(args)
    elif args.subcommand == "test":
        cmd_test(args)
    elif args.subcommand == "validate-skills":
        cmd_validate_skills(args)
    elif args.subcommand == "check-links":
        cmd_check_links(args)
    elif args.subcommand == "doctor":
        cmd_doctor(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
