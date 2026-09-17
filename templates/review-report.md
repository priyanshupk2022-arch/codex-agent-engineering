# Code Review Report

## Executive Summary
- **Overall Verdict**: [APPROVE / REQUEST_CHANGES / REJECT]
- **Risk Rating**: [LOW / MEDIUM / HIGH / CRITICAL]

## Findings Matrix
| Severity | Category | File & Line | Finding & Remediation |
| :--- | :--- | :--- | :--- |
| **FATAL** | Logic | `src/auth.py:42` | Missing return statement causes unauthorized pass-through. |
| **MAJOR** | Performance | `src/db.py:88` | Unindexed query inside loop generates N+1 database queries. |
| **MINOR** | Cleanliness | `src/utils.py:12` | Deprecated datetime.utcnow() used; prefer datetime.now(timezone.utc). |

## Verification Record
- Tests executed: `pytest` -> [PASS / FAIL]
- Linter executed: `ruff check` -> [PASS / FAIL]
