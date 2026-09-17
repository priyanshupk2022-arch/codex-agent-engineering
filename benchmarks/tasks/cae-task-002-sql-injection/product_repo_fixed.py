import sqlite3

class ProductRepo:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
        cur.execute("DELETE FROM products")
        cur.execute("INSERT INTO products (name, price) VALUES ('Widget Pro', 29.99), ('Gadget Mini', 9.99), ('O''Reilly Book', 49.99)")
        self.conn.commit()

    def search_products(self, query: str):
        # FIX: Parameterized query with wildcard binding
        cur = self.conn.cursor()
        pattern = f"%{query}%"
        return cur.execute("SELECT id, name, price FROM products WHERE name LIKE ?", (pattern,)).fetchall()
