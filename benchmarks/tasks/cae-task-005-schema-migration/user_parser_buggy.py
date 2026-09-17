class UserParser:
    @staticmethod
    def parse_user(payload: dict) -> dict:
        # BUG: Only parses legacy full_name, crashes on new schema
        full_name = payload["full_name"]
        parts = full_name.strip().split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
        return {"first_name": first, "last_name": last, "email": payload.get("email", "")}
