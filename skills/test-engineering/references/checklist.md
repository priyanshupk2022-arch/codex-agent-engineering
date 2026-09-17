# test-engineering Checklist & 4-Tier Test Gate Protocol

## Phase 1: Unit & Component Testing (Tier 1)
- [ ] Every new function, class, and method has dedicated unit test coverage.
- [ ] Boundary tests written for empty, null, zero, negative, and extreme inputs.
- [ ] Mocks and stubs restricted strictly to external I/O and network boundaries.
- [ ] Tests execute deterministically with zero dependence on execution order.

## Phase 2: Integration & Contract Testing (Tier 2)
- [ ] Inter-module interfaces validated against declared Pydantic/dataclass schemas.
- [ ] Database queries tested against realistic in-memory or ephemeral test databases.
- [ ] Error handlers and HTTP status codes verified for all declared failure modes.

## Phase 3: Concurrency & Stress Testing (Tier 3)
- [ ] Multi-threaded code tested under high thread contention (>20 concurrent threads).
- [ ] All thread joins bounded with absolute deadlines (`deadline = time.time() + timeout`).
- [ ] Lock inversion safety verified with bi-directional and self-transfer test scenarios.
- [ ] Asynchronous event loops verified for task cancellation and resource leak cleanup.

## Phase 4: Regression & Benchmark Testing (Tier 4)
- [ ] Bugfixes accompanied by a regression test reproducing the exact failure mode.
- [ ] Benchmark runner tests executed to verify performance invariants.
- [ ] Full suite executed with `pytest -v` across all target Python versions.
