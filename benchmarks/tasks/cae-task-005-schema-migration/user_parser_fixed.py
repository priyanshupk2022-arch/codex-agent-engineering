class UserParser:
    @staticmethod
    def parse_user(payload: dict) -> dict:
        # FIX: Handles both new schema and legacy fallback
        if "first_name" in payload:
            first = payload.get("first_name", "")
            last = payload.get("last_name", "")
        elif "full_name" in payload:
            full_name = payload.get("full_name", "").strip()
            parts = full_name.split(" ", 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
        else:
            raise ValueError("Payload missing name fields")

        return {"first_name": first, "last_name": last, "email": payload.get("email", "")}
