# Task 001: Concurrency Lock Inversion Deadlock (`cae-task-001-deadlock`)

## Overview
This task evaluates an agent's ability to diagnose and repair a classic dining philosophers / lock-inversion deadlock in a multi-threaded financial transfer service.

## Failure Scenario
In the buggy implementation (`transfer_service_buggy.py`):
1. Thread 1 locks Account 1, then attempts to lock Account 2.
2. Thread 2 locks Account 2, then attempts to lock Account 1.
3. Both threads block indefinitely awaiting the other lock.
4. Additionally, when `source.id == target.id` (self-transfer), attempting to acquire the same `threading.Lock()` a second time deadlocks on the single thread.

## Requirements
- Modify `transfer_service.py` to establish deterministic lock acquisition order (e.g. by comparing account IDs).
- Detect and handle self-transfers (`source.id == target.id`) without acquiring duplicate locks.
- Reject invalid (negative) transfer amounts.
- Preserve account balance conservation invariant under heavy concurrency.

## Verification
```bash
pytest test_transfer.py -v
```
