import sys
import subprocess
import time

def run_repro(command: list, iterations: int = 5) -> dict:
    results = []
    failures = 0
    start_all = time.time()
    print(f"[*] Running repro test {iterations} times: {' '.join(command)}")
    for i in range(1, iterations + 1):
        t0 = time.time()
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elapsed = time.time() - t0
        passed = (proc.returncode == 0)
        if not passed: failures += 1
        results.append({"run": i, "passed": passed, "exit_code": proc.returncode, "duration": round(elapsed, 3)})
        status = "PASS" if passed else "FAIL"
        print(f" -> Run {i}/{iterations}: {status} in {round(elapsed, 3)}s")
        
    return {
        "command": command,
        "iterations": iterations,
        "failures": failures,
        "failure_rate": round(failures / iterations, 2),
        "total_time": round(time.time() - start_all, 3),
        "runs": results
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python repro_runner.py <cmd> [args...]")
        sys.exit(1)
    cmd = sys.argv[1:]
    report = run_repro(cmd, iterations=5)
    print(f"
Summary: {report['failures']}/{report['iterations']} failures ({report['failure_rate']*100}% failure rate)")
    sys.exit(0 if report['failures'] == 0 else 1)
