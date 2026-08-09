#!/usr/bin/env python3
"""Instantiate the company-brain template for one organization.

Usage:
    python3 scripts/init_brain.py --org "Acme S.A." [--dry-run]

Replaces the organization placeholder across the repo, stamps today's date in the
founding ADR, resets the CHANGELOG, and prints the bootstrap checklist. Idempotent:
running it twice is safe.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

PLACEHOLDER = "__ORG_NAME__"
SKIP_DIRS = {".git", ".venv", "__pycache__"}
TEXT_EXT = {".md", ".yml", ".yaml", ".toml", ".txt"}


def iter_files(root: pathlib.Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in TEXT_EXT and not (set(p.parts) & SKIP_DIRS):
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", required=True, help="Organization name")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    today = datetime.date.today().isoformat()
    changed = []

    for f in iter_files(root):
        text = f.read_text(encoding="utf-8")
        new = text.replace(PLACEHOLDER, args.org)
        if f.name == "0001-adopt-harness-and-company-brain.md":
            new = new.replace("_set at bootstrap_", today)
        if new != text:
            changed.append(f.relative_to(root))
            if not args.dry_run:
                f.write_text(new, encoding="utf-8")

    verb = "Would update" if args.dry_run else "Updated"
    for c in changed:
        print(f"{verb}: {c}")
    print(f"\nOrganization: {args.org}")
    print("Next steps (see .github/skills/bootstrap_company_brain.md):")
    print("  1. Run the bootstrap skill with your AI assistant to populate the brain")
    print("  2. make validate   # must pass before sharing")
    print("  3. Point client repos at this brain (docs/adoption.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
