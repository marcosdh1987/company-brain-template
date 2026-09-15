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

`maps` (Obsidian Canvas views) defaults on for every profile; `14-people`
(Person/Team navigation entities) defaults on only for `team`,
`engineering-management`, and `consulting-company`. Both ship their files
statically — this script only flips the config flag, same as
`12-capabilities`.

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
# Content authored against the other common convention substitutes too, so a
# migration doesn't leave half the placeholders standing.
PLACEHOLDER_ALT = "{{COMPANY_NAME}}"
SKIP_DIRS = {".git", ".venv", "__pycache__", "_to_delete"}
# The template's own release history, not this instance's content. Substituting
# into it would also make every future upstream edit to the file a merge
# conflict for every instance.
SKIP_SUBSTITUTION = {"CHANGELOG.md"}
TEXT_EXT = {".md", ".yml", ".yaml", ".toml", ".txt", ".json"}

# Domain modules (beyond the numbered core set) that a profile may switch on.
# Never assumed active — always declared explicitly per profile, per
# brain.config.json. Profiles are expressed as differences from a shared
# baseline so a missing key can't silently slip through unnoticed.
_BASELINE = {"03-work": True, "04-architecture": True, "05-requirements": True,
             "07-delivery": True, "08-vendors": True, "02-organization": True,
             "12-capabilities": False, "maps": True, "14-people": False}
_PROFILE_DIFFS: dict[str, dict[str, bool] | None] = {
    "consulting": {},
    "delivery-oversight": {"04-architecture": False, "02-organization": False},
    "development": {"08-vendors": False},
    "team": {"05-requirements": False, "08-vendors": False, "14-people": True},
    "engineering-management": {"08-vendors": False, "14-people": True},
    "consulting-company": {"12-capabilities": True, "14-people": True},
    "client-engagement": {},
    # The shared organization layer: company context, conventions, policy and
    # org-wide decisions. No work units — a team's work lives in that team's own
    # brain, which references this one as a source of record.
    "org-layer": {"03-work": False, "04-architecture": False,
                  "05-requirements": False, "07-delivery": False,
                  "08-vendors": False},
    "full": None,  # empty overrides: leave brain.config.json's existing values as-is
}
PROFILES = {name: ({**_BASELINE, **diff} if diff is not None else {})
            for name, diff in _PROFILE_DIFFS.items()}
CORE = ["00-context", "01-meetings", "06-decisions", "09-references", "99-inbox", "memory"]


def _inactive(target: str, modules: dict) -> bool:
    """True if a link target points into a module this profile turned off."""
    module = target.split("/", 1)[0]
    return module in modules and not modules.get(module, False)


def prune_home_optional_links(root: pathlib.Path, modules: dict,
                              dry_run: bool) -> bool:
    """Remove Home.md's links to modules this profile turned off.

    Both shapes are handled, because a module can appear in either: a standalone
    link line is dropped, and a table cell is emptied so the grid survives.

    Home.md is a reader's door, so its rows are real Markdown links — and a
    link to a folder the user may now delete is a hard `make validate` error,
    unlike a dangling Canvas node, which is only reported as debt. Pruning here
    means an instance is green whether or not the owner deletes the folders.
    """
    home = root / "Home.md"
    if not home.is_file():
        return False
    lines = home.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    skip_next_blank = False
    for line in lines:
        stripped = line.strip()
        if skip_next_blank and not stripped:
            skip_next_blank = False
            continue  # the paragraph break that belonged to the dropped entry
        skip_next_blank = False
        if stripped.startswith("|"):
            # A table row: empty the cells that point at an inactive module,
            # keeping the row so the grid does not collapse.
            cells = line.split("|")
            for idx, cell in enumerate(cells):
                if "](" not in cell:
                    continue
                target = cell.split("](", 1)[1].split(")", 1)[0]
                if _inactive(target, modules):
                    cells[idx] = " "
            out.append("|".join(cells))
            continue
        if stripped.startswith("[") and "](" in stripped:
            target = stripped.split("](", 1)[1].split(")", 1)[0]
            if _inactive(target, modules):
                skip_next_blank = True
                continue  # this profile has no such module
        out.append(line)
    new = "".join(out)
    text = "".join(lines)
    if new == text:
        return False
    if not dry_run:
        home.write_text(new, encoding="utf-8")
    return True


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
        if f.name in SKIP_SUBSTITUTION:
            continue
        text = f.read_text(encoding="utf-8")
        new = text.replace(PLACEHOLDER, args.org).replace(PLACEHOLDER_ALT, args.org)
        if f.name == "decision-log.md":
            new = new.replace("_set at bootstrap_", today)
        if new != text:
            changed.append(f.relative_to(root))
            if not args.dry_run:
                f.write_text(new, encoding="utf-8")

    if prune_home_optional_links(root, cfg["modules"], args.dry_run):
        changed.append(pathlib.Path("Home.md"))

    verb = "Would update" if args.dry_run else "Updated"
    for c in changed:
        print(f"{verb}: {c}")
    off = [m for m, on in cfg["modules"].items() if not on]
    print(f"\nOrganization: {args.org}  ·  Profile: {args.profile}")
    if off:
        print("Inactive modules (folders may be deleted, validator ignores them).")
        print("If you delete one, remove any Markdown link into it — a dangling")
        print("link is a hard error, unlike a dangling Canvas node. Home.md was")
        print("pruned for you:")
        for m in off:
            print(f"  {m}/")
    print("\nNext steps:")
    print("  1. Run the bootstrap skill (.github/skills/bootstrap_company_brain.md)")
    print("  2. make validate")
    print("  3. Register code repos in 04-architecture/repos.yaml, then: make workspace")
    return 0


if __name__ == "__main__":
    sys.exit(main())
