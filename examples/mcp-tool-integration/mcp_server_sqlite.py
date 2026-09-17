import sqlite3
import re
from typing import Dict, Any, List

class SqliteMcpServer:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_mock_data()

    def _init_mock_data(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, timestamp TEXT)")
        cur.execute("DELETE FROM users")
        cur.execute("INSERT INTO users (username, role) VALUES ('alice', 'admin'), ('bob', 'developer')")
        self.conn.commit()

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "sqlite_list_tables",
                "description": "List all table names in the database."
            },
            {
                "name": "sqlite_read_query",
                "description": "Execute a read-only SELECT query against the SQLite database.",
                "parameters": {"query": "string"}
            }
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name == "sqlite_list_tables":
            cur = self.conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            return {"success": True, "tables": tables}

        elif name == "sqlite_read_query":
            query = arguments.get("query", "").strip()
            # Security guard: Enforce read-only constraint
            if not re.match(r"(?i)^\s*SELECT\b", query):
                return {"success": False, "error": "SECURITY VIOLATION: Only SELECT queries are permitted by MCP sandbox policy."}
            if re.search(r"(?i)\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)\b", query):
                return {"success": False, "error": "SECURITY VIOLATION: Mutating keyword detected in read query."}
            try:
                cur = self.conn.cursor()
                rows = cur.execute(query).fetchall()
                return {"success": True, "rows": rows}
            except Exception as e:
                return {"success": False, "error": str(e)}

        return {"success": False, "error": f"Unknown tool: {name}"}
