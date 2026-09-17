import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from verify_hierarchy import AgentsHierarchyResolver

def test_root_resolution():
    root = Path(__file__).parent
    chain = AgentsHierarchyResolver.resolve_instructions(root, root)
    assert len(chain) == 1
    assert chain[0]["level"] == "root"
    test_cmd = AgentsHierarchyResolver.extract_effective_test_command(chain)
    assert test_cmd == "pytest tests/"

def test_subsystem_override_billing():
    root = Path(__file__).parent
    target = root / "packages" / "billing"
    chain = AgentsHierarchyResolver.resolve_instructions(root, target)
    assert len(chain) == 2
    assert chain[0]["level"] == "root"
    assert chain[1]["level"] == "subdir:billing"
    test_cmd = AgentsHierarchyResolver.extract_effective_test_command(chain)
    assert test_cmd == "pytest packages/billing/tests/ -v"

def test_subsystem_override_analytics():
    root = Path(__file__).parent
    target = root / "packages" / "analytics"
    chain = AgentsHierarchyResolver.resolve_instructions(root, target)
    assert len(chain) == 2
    test_cmd = AgentsHierarchyResolver.extract_effective_test_command(chain)
    assert test_cmd == "pytest packages/analytics/tests/ -v"
