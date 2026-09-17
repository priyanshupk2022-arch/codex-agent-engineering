import pytest
from user_parser import UserParser

def test_legacy_payload():
    payload = {"full_name": "Ada Lovelace", "email": "ada@example.com"}
    result = UserParser.parse_user(payload)
    assert result == {"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"}

def test_new_payload():
    payload = {"first_name": "Grace", "last_name": "Hopper", "email": "grace@navy.mil"}
    result = UserParser.parse_user(payload)
    assert result == {"first_name": "Grace", "last_name": "Hopper", "email": "grace@navy.mil"}

def test_single_name_legacy():
    payload = {"full_name": "Plato"}
    result = UserParser.parse_user(payload)
    assert result["first_name"] == "Plato"
    assert result["last_name"] == ""

def test_missing_name_raises():
    with pytest.raises(ValueError):
        UserParser.parse_user({"email": "ghost@example.com"})
