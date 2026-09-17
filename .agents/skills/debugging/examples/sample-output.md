# Root Cause Analysis (RCA): Database Connection Pool Exhaustion

**Incident ID**: INC-8402  
**Date**: 2026-09-17  
**Investigator**: CAE Debugging Lead  
**Component**: `services/analytics/exporter.py`  
**Root Cause**: Unclosed async generator leaving PostgreSQL transaction locks open  

---

## 1. Symptom Description
During batch export jobs, the analytics worker pool crashed after ~120 requests with:
`asyncpg.exceptions.TooManyConnectionsError: sorry, too many clients already`

---

## 2. Reproduction Evidence
Ran `python skills/debugging/scripts/repro_runner.py pytest tests/test_exporter_leak.py`:
- 5/5 runs failed with 100% reproduction rate.
- Active connection gauge climbed monotonically from 5 to 100 max pool limit.

---

## 3. Root Cause Analysis
- **Location**: `services/analytics/exporter.py:42-58`
- **Mechanism**: The async generator `stream_records()` acquired an async connection from the pool via `async with pool.acquire()`. When downstream consumers threw an exception or cancelled the iterator early (`break`), the generator was never resumed, bypassing connection release back to the pool.
- **Root Cause**: Generator lacked `finally: await conn.close()` block and was not wrapped in an `asynccontextmanager`.

---

## 4. Remediation & Verification
- Wrapped generator lifecycle in `contextlib.asynccontextmanager`.
- Added explicit connection release in `finally:` block.
- Ran `repro_runner.py` for 10 iterations: 10/10 PASSED with 0 connection leaks.
