# Task 005: Backward-Compatible Schema Parser (`cae-task-005-schema-migration`)

## Overview
This task tests an agent's ability to evolve a data ingestion contract without breaking backward compatibility for existing callers.

## Failure Scenario
In `user_parser_buggy.py`:
1. The parser directly indexes `payload["full_name"]`.
2. When modern microservices submit payloads with `first_name` and `last_name`, a fatal `KeyError` crashes ingestion.
3. Additionally, strings with trailing or leading whitespace, single mononyms (e.g. "Plato"), or multi-part middle names are parsed improperly.

## Requirements
- Modify `user_parser.py` to inspect available payload keys.
- If `first_name` is present, use modern fields (`first_name`, `last_name`).
- If `full_name` is present, fall back to parsing and splitting `full_name`.
- Strip leading/trailing whitespace.
- Handle `None` values safely (coercing to empty string `""`).
- Raise `ValueError` if neither name field is provided or if full_name is purely whitespace.

## Verification
```bash
pytest test_user_parser.py -v
```
