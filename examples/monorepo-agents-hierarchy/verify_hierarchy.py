import os
from pathlib import Path
from typing import List, Dict

class AgentsHierarchyResolver:
    @staticmethod
    def resolve_instructions(root_dir: Path, target_dir: Path) -> List[Dict[str, str]]:
        relative = target_dir.relative_to(root_dir)
        parts = list(relative.parts) if str(relative) != "." else []
        
        current = root_dir
        chain = []
        
        # Check root
        root_agent = current / "AGENTS.md"
        if root_agent.exists():
            chain.append({"path": str(root_agent), "level": "root", "content": root_agent.read_text(encoding="utf8")})
            
        for p in parts:
            current = current / p
            sub_agent = current / "AGENTS.md"
            if sub_agent.exists():
                chain.append({"path": str(sub_agent), "level": f"subdir:{p}", "content": sub_agent.read_text(encoding="utf8")})
                
        return chain

    @staticmethod
    def extract_effective_test_command(chain: List[Dict[str, str]]) -> str:
        effective = "pytest tests/"
        for layer in chain:
            for line in layer["content"].splitlines():
                if "Test Command:" in line:
                    effective = line.split("Test Command:", 1)[1].strip().strip("`")
        return effective
