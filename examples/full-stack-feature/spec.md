# Feature Specification: Token Bucket Rate Limiter

## 1. Problem Statement
The public API requires protective rate limiting to prevent denial-of-service and fair usage violations across API keys.

## 2. Invariants & Functional Contracts
1. Each client key receives a bucket capacity of $N$ tokens, refilling at $R$ tokens/second.
2. An incoming request consuming 1 token succeeds if `tokens >= 1`, decrementing available tokens.
3. If `tokens < 1`, the request is rejected with `HTTP 429 Too Many Requests`.
4. Bucket capacity must never exceed $N$ tokens regardless of idle duration.
5. All token updates must be atomic and thread-safe.
