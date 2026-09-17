import sqlite3
import pytest
from product_repo import ProductRepo

@pytest.fixture
def repo():
    conn = sqlite3.connect(":memory:")
    return ProductRepo(conn)

def test_legitimate_search(repo):
    results = repo.search_products("Widget")
    assert len(results) == 1
    assert results[0][1] == "Widget Pro"

def test_search_with_apostrophe(repo):
    # Tests that query with single quote (e.g. O'Reilly) works without crash
    results = repo.search_products("O'Reilly")
    assert len(results) == 1
    assert results[0][1] == "O'Reilly Book"

def test_sql_injection_defense(repo):
    # Exploit payload attempting SQL injection union or OR condition
    payload = "' OR 1=1 --"
    results = repo.search_products(payload)
    # Under parameterized search, this searches for literal string and matches 0
    assert len(results) == 0, f"SQL Injection detected! Returned {len(results)} items unexpectedly."
