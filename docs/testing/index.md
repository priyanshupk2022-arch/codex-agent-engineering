# Testing & Anti-Cheat Verification Gates

Verification is the cornerstone of autonomous agent reliability. A claim of completion without automated test output is treated as zero progress.

---

## 1. The Four-Tier Verification Gate

Every non-trivial code modification must pass through four distinct tiers of verification:

```
Tier 1: Unit Verification (Fast, isolated component tests)
           │
           ▼
Tier 2: Integration Verification (Inter-service contracts, database, API)
           │
           ▼
Tier 3: Red-Team & Security Gate (Input fuzzing, SQLi, permission bypass)
           │
           ▼
Tier 4: Regression & Stress Gate (Full test suite, race condition stress)
```

---

## 2. Anti-Cheat Test Isolation Rules

To prevent agents from "gaming" tests:
1. **Never weaken existing assertions**: If an existing test fails, that is an alarm signal, not a chore to delete.
2. **Never mock the unit under test**: Only mock external network calls or expensive hardware/database dependencies.
3. **Actor-Critic Separation**: In high-assurance workflows, the agent writing the implementation should not be the sole author of the test suite.
4. **Mechanical Exit-0 Proof**: Success requires capturing actual process execution output showing exit code 0 and test counts.
