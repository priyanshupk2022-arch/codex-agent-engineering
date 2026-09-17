import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sandbox_enforcer import SandboxEnforcer

def test_workspace_write_permitted():
    root = Path(__file__).parent
    enforcer = SandboxEnforcer(root)
    allowed, msg = enforcer.validate_write_path("src/app.py")
    assert allowed is True

def test_path_traversal_blocked():
    root = Path(__file__).parent
    enforcer = SandboxEnforcer(root)
    allowed, msg = enforcer.validate_write_path("../../etc/shadow")
    assert allowed is False
    assert "SECURITY VIOLATION" in msg

def test_allowed_network_host():
    root = Path(__file__).parent
    enforcer = SandboxEnforcer(root, allowed_hosts=["github.com", "pypi.org"])
    allowed, msg = enforcer.validate_network_host("pypi.org")
    assert allowed is True

def test_blocked_network_host():
    root = Path(__file__).parent
    enforcer = SandboxEnforcer(root, allowed_hosts=["github.com", "pypi.org"])
    allowed, msg = enforcer.validate_network_host("evil-exfiltration.com")
    assert allowed is False
    assert "SECURITY VIOLATION" in msg
