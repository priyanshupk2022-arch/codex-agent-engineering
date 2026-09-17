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
    # Tests that query with single quote (e.g. O'Reilly) works without crash and finds record
    results = repo.search_products("O'Reilly")
    assert len(results) == 1
    assert results[0][1] == "O'Reilly Book"

def test_sql_injection_or_clause(repo):
    # Exploit payload attempting SQL injection OR condition
    payload = "' OR 1=1 --"
    results = repo.search_products(payload)
    assert len(results) == 0, f"SQL Injection detected! Returned {len(results)} items unexpectedly."

def test_sql_injection_union_probe(repo):
    # Exploit payload attempting UNION-based extraction
    payload = "x' UNION SELECT 999, 'Injected', 0.0 --"
    results = repo.search_products(payload)
    assert len(results) == 0, "UNION injection payload succeeded!"

def test_sql_injection_drop_table(repo):
    # Exploit payload attempting stacked statement injection
    payload = "'; DROP TABLE products; --"
    results = repo.search_products(payload)
    assert len(results) == 0

    # Ensure products table was not dropped
    cur = repo.conn.cursor()
    cur.execute("SELECT count(*) FROM products")
    count = cur.fetchone()[0]
    assert count == 3, "Products table was modified or dropped by injection payload!"

def test_empty_query_matches_all(repo):
    # Empty query should match all products via %%%
    results = repo.search_products("")
    assert len(results) == 3
