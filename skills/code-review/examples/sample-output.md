# Senior Staff Code Review: PR #142 (Async Event Streaming)

**Reviewer**: CAE Code Review Specialist  
**Commit Range**: `3f8a12d..b9c041e`  
**Verdict**: CHANGES REQUESTED (1 Critical, 1 Warning)  

---

## 1. Summary of Changes
The author introduces an asynchronous event streaming consumer for Kafka using `aiokafka`. The core message dispatch logic is sound, but resource cleanup on consumer cancellation exhibits a socket leak, and a potential SQL injection vulnerability exists in event indexing.

---

## 2. Inline Review Comments

### File: `services/streaming/consumer.py:84`
```python
- sql = f"INSERT INTO events (id, payload) VALUES ('{event.id}', '{event.data}')"
```
> **[CRITICAL] CWE-89: SQL Injection Risk**  
> `event.data` is an untrusted payload string interpolated directly into SQL syntax. If an event contains single quotes, this will crash or permit arbitrary SQL execution.  
> **Fix**: Use parameterized query:  
> `await db.execute("INSERT INTO events (id, payload) VALUES (?, ?)", (event.id, event.data))`

### File: `services/streaming/consumer.py:112`
```python
+ except asyncio.CancelledError:
+     print("Consumer cancelled")
```
> **[WARN] Anti-pattern: Debug print & Missing Rethrow**  
> Printing to stdout in library code bypasses structured logging. Furthermore, catching `CancelledError` without re-raising prevents graceful task teardown.  
> **Fix**: Log with `logger.info(...)` and re-raise `CancelledError`.

---

## 3. Checklist Verification
- [x] Correctness: Verified logic paths.
- [ ] Security: Blocked by CWE-89 finding in `consumer.py:84`.
- [ ] Tests: Missing integration test verifying cancellation cleanup.
