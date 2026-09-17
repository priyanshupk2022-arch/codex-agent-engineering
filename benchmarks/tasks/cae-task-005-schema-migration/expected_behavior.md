# Expected Behavior & Verification Contract: Task 005

## Behavioral Specification
1. **Dual Schema Support**:
   - Modern schema: When `first_name` is present in `payload` and not `None`, extract `first_name` and `last_name`.
   - Legacy schema: When `first_name` is absent or `None`, but `full_name` is present and not `None`, split `full_name` into `first_name` (first word) and `last_name` (remainder).
2. **Mononym & Whitespace Handling**:
   - Mononyms (single token, e.g., "Cher") result in `last_name = ""`.
   - Redundant spaces (e.g. `"  Ada   Lovelace  "`) are normalized cleanly via whitespace split.
3. **Null & Missing Attributes**:
   - Missing or `None` values for `email` or `last_name` must default to empty string `""`.
   - If neither valid `first_name` nor valid `full_name` is present, or if `full_name.strip()` is empty, raise `ValueError`.
4. **Output Invariant**: The returned dictionary must strictly adhere to the contract:
   `{"first_name": str, "last_name": str, "email": str}`

## Forbidden Shortcuts
- Deleting support for the legacy `full_name` payload.
- Returning mock constant users.
- Swallowing missing-name errors without raising `ValueError`.
