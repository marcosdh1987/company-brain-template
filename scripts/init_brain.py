#!/usr/bin/env python3
"""Instantiate the company-brain template for one organization.

Usage:
    python3 scripts/init_brain.py --org "Acme Inc." [--profile consulting] [--dry-run]

Profiles preselect active modules in brain.config.json:
  consulting            strategy/oversight work, no code repos yet
  delivery-oversight    validating a vendor's delivery
  development           the org has code repos we work on
  team                  a single team's internal brain, no client dimension
  engineering-management  engineering org context: repos, conventions, delivery
  consulting-company    a consultancy's own brain across clients (capability
                        register on by default)
  client-engagement     a single client engagement, full traceability
  full                  everything on (default)

The script replaces the __ORG_NAME__ placeholder, stamps the founding DEC
date, writes the config, and lists module folders that can be deleted for the
chosen profile (it never deletes them itself).
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

PLACEHOLDER = "__ORG_NAME__"
SKIP_DIRS = {".git", ".venv", "__pycache__", "_to_delete"}
TEXT_EXT = {".md", ".yml", ".yaml", ".toml", ".txt", ".json"}

# Domain modules (beyond the numbered core set) that a profile may switch on.
# Never assumed active — always declared explicitly per profile, per
# brain.config.json. Profiles are expressed as differences from a shared
# baseline so a missing key can't silently slip through unnoticed.
_BASELINE = {"03-work": True, "04-architecture": True, "05-requirements": True,
             "07-delivery": True, "08-vendors": True, "02-organization": True,
             "12-capabilities": False}
_PROFILE_DIFFS: dict[str, dict[str, bool] | None] = {
    "consulting": {},
    "delivery-oversight": {"04-architecture": False, "02-organization": False},
    "development": {"08-vendors": False},
    "team": {"05-requirements": False, "08-vendors": False},
    "engineering-management": {"08-vendors": False},
    "consulting-company": {"12-capabilities": True},
    "client-engagement": {},
    "full": None,  # empty overrides: leave brain.config.json's existing values as-is
}
PROFILES = {name: ({**_BASELINE, **diff} if diff is not None else {})
            for name, diff in _PROFILE_DIFFS.items()}
CORE = ["00-context", "01-meetings", "06-decisions", "09-references", "99-inbox", "memory"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", required=True)
    ap.add_argument("--profile", default="full", choices=sorted(PROFILES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    today = datetime.date.today().isoformat()

    cfg_path = root / "brain.config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["org"] = args.org
    cfg["profile"] = args.profile
    overrides = PROFILES[args.profile]
    for mod in cfg["modules"]:
        if mod in CORE:
            cfg["modules"][mod] = True
        elif overrides:
            cfg["modules"][mod] = overrides.get(mod, False)
    if not args.dry_run:
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    changed = []
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in TEXT_EXT or (set(f.parts) & SKIP_DIRS):
            continue
        text = f.read_text(encoding="utf-8")
        new = text.replace(PLACEHOLDER, args.org)
        if f.name == "decision-log.md":
            new = new.replace("_set at bootstrap_", today)
        if new != text:
            changed.append(f.relative_to(root))
            if not args.dry_run:
                f.write_text(new, encoding="utf-8")

    verb = "Would update" if args.dry_run else "Updated"
    for c in changed:
        print(f"{verb}: {c}")
    off = [m for m, on in cfg["modules"].items() if not on]
    print(f"\nOrganization: {args.org}  ·  Profile: {args.profile}")
    if off:
        print("Inactive modules (folders may be deleted, validator ignores them):")
        for m in off:
            print(f"  {m}/")
    print("\nNext steps:")
    print("  1. Run the bootstrap skill (.github/skills/bootstrap_company_brain.md)")
    print("  2. make validate")
    print("  3. Register code repos in 04-architecture/repos.yaml, then: make workspace")
    return 0


if __name__ == "__main__":
    sys.exit(main())
