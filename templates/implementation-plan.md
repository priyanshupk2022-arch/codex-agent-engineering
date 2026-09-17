# Implementation Plan: [Task / Feature Name]

## 1. Architectural Strategy
[Summary of technical approach, trade-offs evaluated, and affected components.]

## 2. File Modification Map
| File | Action (Create / Modify / Delete) | Substance of Change |
| :--- | :--- | :--- |
| `src/...` | Modify | Add schema validation |
| `tests/...` | Create | Unit test coverage for boundary inputs |

## 3. Atomic Task Sequence
1. Task 1: [Define schema interfaces] -> Verify with `mypy`
2. Task 2: [Implement core handler] -> Verify with `pytest tests/test_new.py`
3. Task 3: [Full regression run] -> Verify with `pytest`
