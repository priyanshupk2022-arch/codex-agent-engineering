# Expected Behavior & Verification Contract: Task 004

## Behavioral Specification
1. **Atomic Check-and-Decrement**: In `order(quantity)`:
   - Check `self.stock >= quantity` and the decrement `self.stock -= quantity` must be strictly atomic under `self._lock`.
   - No context switch or concurrent evaluation can occur between inspection and decrement.
2. **Input Validation**: Orders where `quantity <= 0` must return `False` immediately and leave `self.stock` unaltered.
3. **Inventory Invariant**: The quantity of stock remaining in `InventoryService` must satisfy `0 <= self.stock <= initial_stock` at all times.
4. **Conservation of Orders**: In any concurrent execution with `N` threads attempting single-unit orders against initial stock `S`:
   - Exactly `min(N, S)` orders must succeed (`return True`).
   - Exactly `max(0, N - S)` orders must fail (`return False`).
   - Final stock must equal `max(0, S - N)`.

## Forbidden Shortcuts
- Placing `self._lock` only around the decrement operation while leaving the comparison unlocked.
- Sleep delays to mask timing races.
- Disallowing concurrent thread execution.
