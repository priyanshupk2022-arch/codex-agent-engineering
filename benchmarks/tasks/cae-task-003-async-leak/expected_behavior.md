# Expected Behavior & Verification Contract: Task 003

## Behavioral Specification
1. **Deterministic Async Cleanup**: Whenever a `MockResource` instance is allocated inside `process_stream()`, its `.close()` coroutine must be awaited prior to exiting the function scope under all execution paths.
2. **Exception Propagation**: Any exceptions encountered during chunk reading (such as `RuntimeError`, `IOError`, or custom exceptions) must not be suppressed. They must propagate cleanly to the caller after resource closure.
3. **Multi-iteration State Conservation**: Successive or concurrent stream processing cycles must never leak resources; `MockResource.active_instances` must return to `0` upon completion of each call.

## Forbidden Shortcuts
- Catching exceptions with broad `try ... except Exception: pass` to allow execution to fall through to `res.close()`.
- Directly reassigning `MockResource.active_instances = 0` to fake zero leaks.
- Omitting exception triggering when `should_fail=True`.
