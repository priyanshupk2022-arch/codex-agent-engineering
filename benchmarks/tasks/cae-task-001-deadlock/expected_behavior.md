# Expected Behavior & Verification Contract: Task 001

## Behavioral Specification
1. **Deterministic Lock Ordering**: When transferring between two distinct accounts `A` and `B`, the lock of the account with the smaller `id` must ALWAYS be acquired before the lock of the account with the larger `id`.
2. **Self-Transfer Handling**: When transferring where `source.id == target.id`:
   - Acquire the lock exactly once.
   - If `source.balance >= amount` and `amount >= 0`, return `True` with balance unchanged.
   - If `amount > source.balance`, return `False` with balance unchanged.
3. **Negative & Zero Amounts**:
   - Transfers with `amount < 0` must return `False` immediately and make zero balance modifications.
   - Transfers with `amount == 0` must succeed if balance >= 0 and not alter balance.
4. **Conservation of Value**: The sum of balances across all accounts in a closed system must remain constant before, during, and after any number of concurrent transfers.

## Forbidden Shortcuts
- Disabling locks or using non-thread-safe raw mutations.
- Catching exceptions with broad `pass` statements.
- Applying a global process-wide lock that serializes all transfers.
- Adding arbitrary sleeps instead of deterministic hierarchy.
