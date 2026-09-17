import os
from pathlib import Path
from typing import List, Tuple

class SandboxEnforcer:
    def __init__(self, workspace_root: Path, allowed_hosts: List[str] = None):
        self.workspace_root = workspace_root.resolve()
        self.allowed_hosts = set(allowed_hosts or [])

    def validate_write_path(self, target_path: str) -> Tuple[bool, str]:
        resolved = (self.workspace_root / target_path).resolve()
        try:
            resolved.relative_to(self.workspace_root)
            return True, "Path within workspace confinement."
        except ValueError:
            return False, f"SECURITY VIOLATION: Path '{target_path}' attempts traversal outside workspace root '{self.workspace_root}'"

    def validate_network_host(self, host: str) -> Tuple[bool, str]:
        cleaned_host = host.split(":")[0].lower().strip()
        if cleaned_host in self.allowed_hosts:
            return True, f"Host '{cleaned_host}' is permitted by network allowlist."
        return False, f"SECURITY VIOLATION: Outbound network connection to '{cleaned_host}' blocked by sandbox policy."
