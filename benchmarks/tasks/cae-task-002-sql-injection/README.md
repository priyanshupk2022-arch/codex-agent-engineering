# Task 002: SQL Injection in Product Search (`cae-task-002-sql-injection`)

## Overview
This task evaluates an agent's ability to secure a dynamic SQL query in a SQLite repository against SQL injection while maintaining full functionality for queries with legitimate special characters (apostrophes, quotes).

## Failure Scenario
In the buggy implementation (`product_repo_buggy.py`):
1. User search queries are concatenated directly into the SQL string (`f"SELECT ... LIKE '%{query}%'"`).
2. Attackers can inject SQL operators (e.g. `' OR 1=1 --`) to leak the entire product database.
3. Legitimate search terms containing apostrophes (e.g. `O'Reilly Book`) terminate the string literal early, causing an unhandled `sqlite3.OperationalError` syntax crash.

## Requirements
- Modify `product_repo.py` to use parameterized queries with SQLite parameter binding (`?`).
- Properly construct the pattern for `LIKE` matches using Python string formatting before binding (e.g. `pattern = f"%{query}%"`).
- Ensure injection payloads return 0 matching products.
- Ensure legitimate queries with apostrophes match accurately without crashing.

## Verification
```bash
pytest test_product_repo.py -v
```
