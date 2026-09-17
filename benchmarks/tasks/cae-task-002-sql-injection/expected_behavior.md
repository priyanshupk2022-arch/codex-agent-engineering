# Expected Behavior & Verification Contract: Task 002

## Behavioral Specification
1. **Parameterized Query Binding**: All user-supplied input strings passed to `search_products(query)` must be bound using SQLite positional parameter markers (`?`). Raw string concatenation or f-string interpolation into SQL query text is strictly prohibited.
2. **LIKE Pattern Construction**: The wildcard bounding (`%query%`) must be applied in Python application code and passed as a parameter tuple `(f"%{query}%",)`.
3. **Special Character Resilience**: Queries containing legitimate single quotes (`O'Reilly`), double quotes (`"Pro"`), hyphens, and percent signs must execute cleanly without syntax errors and match literal substrings.
4. **SQL Injection Defense**: Exploitative payloads such as `' OR 1=1 --`, `' UNION SELECT ... --`, and `'; DROP TABLE ... --` must be treated as literal search substrings, returning empty result sets when no product contains those exact characters.

## Forbidden Shortcuts
- Stripping or deleting single quotes via `query.replace("'", "")` (destroys search fidelity for terms like `O'Reilly`).
- In-memory regex filtering over the entire database instead of SQL parameterization.
- Suppressing syntax errors with broad `except Exception: return []`.
