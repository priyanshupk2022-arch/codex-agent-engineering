# Case Study 02: Production Incident RCA Under Time Pressure

## 1. Problem
An e-commerce API experienced cascading 504 Gateway Timeouts during Black Friday traffic surges. Error rates spiked from 0.01% to 38.4%.

## 2. The Naive Approach
On-call engineer prompted an agent: *"Look at these error logs and fix whatever is broken."*
The agent suggested increasing database connection pool size from 20 to 500, which crashed the PostgreSQL database server due to memory exhaustion.

## 3. Revised CAE Workflow
1. **Containment**: Rolled back immediate traffic spike via circuit breaker.
2. **Incident Debugging Workflow**: Triangulated logs using `debugging` workflow. Identified that an external tax calculation API call was hanging for 30 seconds without an HTTP client timeout.
3. **Reproduction Test**: Authored a mock test reproducing the connection starvation under delayed external response.
4. **Surgical Patch**: Applied a 1.5-second timeout with fallback to cached regional tax estimates.
5. **Stress Verification**: Ran local concurrency stress test with 100 concurrent workers; error rate dropped to 0%.

## 4. Outcome & Lessons
- Hotfix deployed within 22 minutes.
- Prevented database server crash.
- **Core Lesson**: Diagnosing timeouts requires tracing resource wait times, not blindly increasing pool capacity.
