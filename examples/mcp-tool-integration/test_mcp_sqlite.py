import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from mcp_server_sqlite import SqliteMcpServer

def test_list_tools():
    server = SqliteMcpServer()
    tools = server.list_tools()
    assert len(tools) == 2
    tool_names = [t["name"] for t in tools]
    assert "sqlite_list_tables" in tool_names
    assert "sqlite_read_query" in tool_names

def test_list_tables():
    server = SqliteMcpServer()
    res = server.call_tool("sqlite_list_tables", {})
    assert res["success"] is True
    assert "users" in res["tables"]
    assert "audit_logs" in res["tables"]

def test_read_query_allowed():
    server = SqliteMcpServer()
    res = server.call_tool("sqlite_read_query", {"query": "SELECT username, role FROM users WHERE username = 'alice'"})
    assert res["success"] is True
    assert len(res["rows"]) == 1
    assert res["rows"][0] == ("alice", "admin")

def test_write_query_blocked():
    server = SqliteMcpServer()
    res = server.call_tool("sqlite_read_query", {"query": "DROP TABLE users"})
    assert res["success"] is False
    assert "SECURITY VIOLATION" in res["error"]
