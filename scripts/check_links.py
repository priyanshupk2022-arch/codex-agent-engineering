import re
import sys
from pathlib import Path

def check_markdown_links(root_dir: Path) -> bool:
    all_valid = True
    md_files = list(root_dir.glob("**/*.md"))
    # Filter out hidden or build directories
    md_files = [f for f in md_files if not any(part.startswith(".") or part == "node_modules" for part in f.parts)]

    print(f"[*] Checking internal links across {len(md_files)} markdown files...")
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^http\:][^\)#]+)(?:#[^\)]+)?\)')

    for mf in md_files:
        content = mf.read_text(encoding="utf8", errors="ignore")
        matches = link_pattern.findall(content)
        for text, target in matches:
            target = target.strip()
            if not target or target.startswith("mailto:") or target.startswith("#"):
                continue
            
            # Resolve target relative to mf parent
            if target.startswith("/"):
                resolved = root_dir / target.lstrip("/")
            else:
                resolved = (mf.parent / target).resolve()

            if not resolved.exists():
                print(f"[BROKEN LINK] in {mf.relative_to(root_dir)}: [{text}]({target}) -> {resolved}")
                all_valid = False

    if all_valid:
        print("[OK] All relative markdown links resolve successfully.")
    return all_valid

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    success = check_markdown_links(root)
    sys.exit(0 if success else 1)
