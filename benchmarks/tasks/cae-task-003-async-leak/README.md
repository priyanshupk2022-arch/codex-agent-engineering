# Task 003: Unclosed Resource Leak in Async Stream (`cae-task-003-async-leak`)

## Overview
This task tests an agent's ability to ensure deterministic cleanup of asynchronous network/file stream resources in Python, avoiding file descriptor or socket leaks when mid-stream exceptions occur.

## Failure Scenario
In `stream_processor_buggy.py`:
1. `res = MockResource()` opens an async resource.
2. An error occurs while iterating over chunks (`should_fail=True`).
3. The exception bubbles up immediately, skipping the trailing `await res.close()`.
4. `MockResource.active_instances` remains positive, indicating an open leak.

## Requirements
- Ensure `res.close()` is guaranteed to execute whether `process_stream` completes normally or raises an exception.
- Wrap the consumption loop in `try...finally: await res.close()`.
- Re-raise original exceptions without alteration.

## Verification
```bash
pytest test_stream_processor.py -v
```
