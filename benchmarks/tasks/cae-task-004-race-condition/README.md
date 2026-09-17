# Task 004: Inventory Oversell Race Condition (`cae-task-004-race-condition`)

## Overview
This task tests an agent's ability to diagnose and fix a time-of-check to time-of-use (TOCTOU) race condition in an e-commerce inventory reservation system.

## Failure Scenario
In `inventory_buggy.py`:
1. `if self.stock >= quantity:` is evaluated without acquiring the mutex lock.
2. Multiple concurrent threads simultaneously observe sufficient stock.
3. Each thread subsequently enters `with self._lock:` and decrements `self.stock`.
4. As a result, 38 orders succeed against an initial inventory of 20, overselling by 18 units and driving stock into negative values.

## Requirements
- Ensure both the stock availability check and the decrement occur inside the critical section protected by `self._lock`.
- Reject non-positive quantities (`quantity <= 0`) prior to or within the transaction.
- Guarantee that `self.stock` is non-negative at all times.

## Verification
```bash
pytest test_inventory.py -v
```
