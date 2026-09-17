class UserParser:
    @staticmethod
    def parse_user(payload: dict) -> dict:
        # FIX: Handles both new schema and legacy fallback with whitespace normalization
        if "first_name" in payload and payload["first_name"] is not None:
            first = str(payload.get("first_name", "") or "").strip()
            last = str(payload.get("last_name", "") or "").strip()
        elif "full_name" in payload and payload["full_name"] is not None:
            full_name = str(payload.get("full_name", "") or "").strip()
            if not full_name:
                raise ValueError("Payload contains empty full_name")
            parts = full_name.split(None, 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
        else:
            raise ValueError("Payload missing name fields")

        email = str(payload.get("email", "") or "").strip()
        return {"first_name": first, "last_name": last, "email": email}
