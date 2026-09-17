# Implementation Plan: Token Bucket Rate Limiter

## Phase 1: In-Memory Token Bucket Core
- Implement `RateLimiter` class with `acquire(key: str, cost: int = 1) -> bool`.
- Store per-client state: `tokens: float`, `last_updated: float`, `lock: threading.Lock`.
- Calculate token replenishment: `min(capacity, tokens + elapsed * refill_rate)`.

## Phase 2: Verification Strategy
- Unit test: Single client token consumption up to capacity.
- Rate limit test: Immediate subsequent request rejected after bucket depletion.
- Refill test: Verification that tokens replenish correctly after sleep interval.
