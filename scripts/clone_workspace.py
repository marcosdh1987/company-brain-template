#!/usr/bin/env python3
"""Clone every repo registered in 04-architecture/repos.yaml as a SIBLING of
this brain (hub-and-spoke; see docs/workspace.md). Existing clones are pulled,
not re-cloned. No PyYAML dependency: parses the simple list format used in
repos.yaml."""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARENT = ROOT.parent
REG = ROOT / "04-architecture/repos.yaml"


def parse(path: pathlib.Path):
    repos, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"\s*#", line) or not line.strip():
            continue
        m = re.match(r"\s*-\s+name:\s*(\S+)", line)
        if m:
            cur = {"name": m.group(1)}
            repos.append(cur)
            continue
        m = re.match(r"\s+(\w+):\s*(.+)", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2).strip()
    return [r for r in repos if r.get("workspace", "true").lower() != "false"]


def main() -> int:
    if not REG.is_file():
        print("No repos.yaml found."); return 1
    repos = parse(REG)
    if not repos:
        print("No repos registered (repos: []). Add them to 04-architecture/repos.yaml.")
        return 0
    for r in repos:
        name, url = r["name"], r.get("url")
        dest = PARENT / name
        if dest.exists():
            print(f"[pull ] {name}")
            subprocess.run(["git", "-C", str(dest), "pull", "--ff-only"], check=False)
        elif url:
            print(f"[clone] {name} <- {url}")
            subprocess.run(["git", "clone", url, str(dest)], check=False)
        else:
            print(f"[skip ] {name}: no url")
    print(f"\nWorkspace at: {PARENT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
