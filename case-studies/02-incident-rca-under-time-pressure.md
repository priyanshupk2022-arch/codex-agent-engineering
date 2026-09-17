# Case Study 02: Production Incident RCA Under Time Pressure

## 1. Problem Description and Initial State
During a high-visibility Black Friday promotional event, an e-commerce platform's core checkout microservice (`checkout-service`) began experiencing cascading HTTP 504 Gateway Timeouts. 

Initial telemetry revealed:
- **Throughput**: 8,500 checkout requests/second across 16 Kubernetes pods.
- **Error Spike**: HTTP 504 errors escalated from a baseline of 0.01% to 38.4% within 6 minutes, eventually reaching 71.2%.
- **Worker Starvation**: Gunicorn worker pools saturated at 100% capacity; incoming requests queued at the Nginx reverse proxy until timing out at the 30-second client threshold.
- **Log Signatures**: Logs were flooded with database connection errors:
  ```text
  sqlalchemy.exc.TimeoutError: QueuePool limit of size 20 overflow 10 reached, connection timed out, timeout 30.00
  ```

## 2. The Naive Approach
An on-call engineer facing escalating executive pressure copied the tail of the error log directly into an unconstrained Codex session:
```text
"Our checkout-service is dying with 504 Gateway Timeouts. Error log shows:
'sqlalchemy.exc.TimeoutError: QueuePool limit of size 20 overflow 10 reached'
Fix this connection pool starvation immediately so the database stops timing out."
```

The agent was permitted to propose an emergency configuration patch without providing trace evidence or running an isolated reproduction script.

## 3. Failure Mode Analysis
The naive suggestion produced a near-fatal secondary outage:
1. **Symptom Confusion (Pool Starvation vs Upstream Block)**: The agent treated the `QueuePool` exhaustion as the root cause rather than a downstream symptom. It generated a patch increasing `pool_size` from 20 to 500 and `max_overflow` from 10 to 200 per pod.
2. **Database Engine Crash (Thundering Herd)**: When deployed across 16 pods, the new configuration allowed up to 11,200 simultaneous database connections. The primary PostgreSQL database instance had a hard kernel limit of `max_connections = 1000`. Within 45 seconds of rollout, the database crashed from OS memory exhaustion (OOM killer terminated postmaster), turning a degraded checkout flow into a complete platform-wide outage.
3. **Absence of Trace Analysis**: The naive agent failed to inspect distributed trace spans or flamegraphs, completely missing the fact that database transactions were stalling because worker threads were held hostage by a third-party outbound HTTP call.

## 4. The Revised Workflow
The engineering team engaged the CAE `debugging` and `incident-rca` protocol, enforcing strict separation between incident containment, hypothesis triangulation, and surgical remediation:

```
[Phase 1: Containment] ──> [Phase 2: Distributed Trace Triangulation] ──> [Phase 3: Repro Runner Test]
                                                                                       │
                                                                                       ▼
[Phase 6: Canary Verification] <── [Phase 5: Surgical Resiliency Patch] <── [Phase 4: Hypothesis Testing]
```

- **Stage 1 (Containment)**: Activated Nginx emergency rate-limiting and shed non-essential background worker loads to protect database survival.
- **Stage 2 (Telemetry Triangulation)**: Queried OpenTelemetry distributed traces to identify the longest-duration child span within the stalled checkout transactions.
- **Stage 3 (Reproduction Harness)**: Used `skills/debugging/scripts/repro_runner.py` to recreate thread pool exhaustion locally using a mock upstream dependency.
- **Stage 4 (Surgical Resiliency Patch)**: Reverted the dangerous connection pool increase and implemented bounded network timeouts with cached fallbacks.

## 5. Step-by-Step Implementation Walkthrough
1. **Span Latency Triangulation**:
   - Tracing revealed that the database connections were held open during an un-timeouted HTTP request to an external third-party tax estimation SaaS (`api.taxvendor.com`).
   - The tax vendor had experienced an internal latency degradation, responding in 42–58 seconds per call. Because the Python `requests.get()` invocation omitted an explicit `timeout` parameter, the Gunicorn worker thread held the database transaction lock open while waiting indefinitely for the HTTP socket.
2. **Deterministic Repro Test Authoring**:
   - Authored `tests/repro/test_tax_timeout_exhaustion.py` initializing a local mock server with a 30s sleep.
   - Verified that without a timeout, 10 concurrent requests exhausted the test worker pool in under 1 second.
3. **Resilient Implementation Patch**:
   - Updated `services/tax_provider.py`:
     ```python
     # Bounded socket timeout with regional fallback
     try:
         resp = session.post(TAX_URL, json=payload, timeout=(0.5, 1.2)) # 500ms connect, 1.2s read
         return resp.json()["rate"]
     except (requests.Timeout, requests.RequestException) as err:
         logger.warning("Tax provider timeout; applying cached regional fallback", exc_info=err)
         return get_cached_regional_fallback_rate(payload["state_code"])
     ```
   - Maintained database connection pool at a safe, sustainable `pool_size=25`.
4. **Local Stress & Concurrency Gate**:
   - Executed `repro_runner.py` simulating 200 concurrent threads against a hung mock tax service; 100% of checkouts succeeded within 1.3 seconds using the cached fallback.

## 6. Verification and Test Results
- **Reproduction Benchmark**: Validated that `test_tax_timeout_exhaustion.py` passed deterministically in 1.24s.
- **Canary Deployment**: Deployed the surgical patch to 2 canary pods; response latency plummeted from 30,000ms to 48ms.
- **Production Rollout**: Rolled out across all 16 pods within 18 minutes. Overall 504 error rate dropped from 71.2% to 0.018%.
- **Database Health**: PostgreSQL connection count stabilized at 142 connections (well below the 1,000 limit), and database CPU load dropped from 99% to 18%.

## 7. Benchmark Comparison: Naive vs Structured Workflow

| Metric / Dimension | Naive Single-Prompt Codex | CAE Structured Workflow (Debugging Skill) | Delta / Impact |
| :--- | :--- | :--- | :--- |
| **Outage Resolution Status** | Worsened Outage (DB crash) | Complete Remediation | **Prevented Catastrophe** |
| **Time to Root Cause Identification** | N/A (Hallucinated cause) | 7 minutes via span triangulation | **Targeted Accuracy** |
| **Database Blast Radius** | 8,000 conns (OOM crash) | 142 conns (Stable headroom) | **Zero database risk** |
| **Outbound Network Resilience** | Unhandled indefinite hang | 1.2s bounded socket + cache fallback | **Fault-tolerant** |
| **Deterministic Repro Test** | None authored | `test_tax_timeout_exhaustion.py` passing | **Regression-proof** |
| **Total MTTR (Mean Time to Recover)**| >120 mins (Required DB restore) | 22 minutes total incident duration | **5.4x MTTR reduction** |

## 8. Key Lessons and Reusable Rules for AGENTS.md

### Rule 1: Never Expand Connection Pools to Solve Timeouts
> **CRITICAL**: A connection pool exhaustion error is almost always an effect of slow transactional execution, not insufficient pool capacity. Agents MUST investigate thread holding duration and span waterfalls before altering database pool limits.

### Rule 2: Mandate Explicit Timeouts on All Outbound I/O
> **ENFORCEMENT**: Every outbound network call (HTTP, gRPC, RPC, external cache) must have explicit connect and read timeouts (max connect: 1.0s, max read: 3.0s unless explicitly documented). Any call without timeouts must be flagged as a security and reliability defect by `skills/security-review`.

### Rule 3: Author a Deterministic Reproduction Before Patching
> **PROCESS**: Never accept a bugfix patch without a reproduction test that fails against the current code and passes against the proposed diff under simulated fault conditions.
