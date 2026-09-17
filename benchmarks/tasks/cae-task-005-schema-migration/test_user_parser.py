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

def test_multi_part_legacy_name():
    payload = {"full_name": "John Ronald Reuel Tolkien", "email": "jrrt@oxford.ac.uk"}
    result = UserParser.parse_user(payload)
    assert result["first_name"] == "John"
    assert result["last_name"] == "Ronald Reuel Tolkien"

def test_missing_name_raises():
    with pytest.raises(ValueError):
        UserParser.parse_user({"email": "ghost@example.com"})

def test_empty_payload_raises():
    with pytest.raises(ValueError):
        UserParser.parse_user({})

def test_whitespace_only_name_raises():
    with pytest.raises(ValueError):
        UserParser.parse_user({"full_name": "     "})

def test_whitespace_normalization():
    payload = {"full_name": "  Ada    Lovelace  ", "email": "ada@example.com"}
    result = UserParser.parse_user(payload)
    assert result["first_name"] == "Ada"
    assert result["last_name"] == "Lovelace"

def test_none_values_handling():
    payload = {"first_name": "Alan", "last_name": None, "email": None}
    result = UserParser.parse_user(payload)
    assert result["first_name"] == "Alan"
    assert result["last_name"] == ""
    assert result["email"] == ""

def test_payload_with_extra_fields():
    payload = {
        "first_name": "Margaret",
        "last_name": "Hamilton",
        "email": "margaret@nasa.gov",
        "role": "Director of Software",
        "apollo_mission": 11
    }
    result = UserParser.parse_user(payload)
    assert result == {
        "first_name": "Margaret",
        "last_name": "Hamilton",
        "email": "margaret@nasa.gov"
    }
