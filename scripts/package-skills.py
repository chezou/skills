#!/usr/bin/env python3
"""Package each skill as a standalone .zip in dist/.

This is the file-handoff install route: upload the archive at claude.ai under
Settings > Capabilities > Skills, or send it to someone who unzips it into their
agent's skills directory. Each archive holds a single top-level folder named
after the skill, which is the shape claude.ai expects on upload.

Usage: python3 scripts/package-skills.py [skill-name ...]   (default: all)
"""

import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules"}

root = Path(__file__).resolve().parent.parent
skills_dir = root / "skills"
dist = root / "dist"


def files_for(skill_dir):
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name in EXCLUDE_NAMES or EXCLUDE_DIRS & set(path.relative_to(skill_dir).parts):
            continue
        yield path


def main():
    if subprocess.call([sys.executable, str(root / "scripts" / "validate-skills.py")]) != 0:
        return 1

    names = sys.argv[1:] or sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
    dist.mkdir(exist_ok=True)

    for name in names:
        skill_dir = skills_dir / name
        if not (skill_dir / "SKILL.md").is_file():
            print(f"no such skill: {name}", file=sys.stderr)
            return 1
        archive = dist / f"{name}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in files_for(skill_dir):
                zf.write(path, path.relative_to(skills_dir))
        print(f"dist/{name}.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
