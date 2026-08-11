#!/usr/bin/env python3
"""Validate the brain: structure (per brain.config.json), links, and semantics.

Checks:
  structural (exit 1 on failure):
    - required files exist for every ACTIVE module
    - relative markdown links resolve
    - duplicate IDs within a namespace (DEC-001 defined twice, etc.)
  reported as debt (never fail the build):
    - decisions without a Source field
    - status-marker counts (CONFIRMED / PENDING VALIDATION / INFERRED /
      SUPERSEDED / BLOCKED) and `_PENDING_` placeholders per module
    - unprocessed inbox files (no `processed--` prefix)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALWAYS_REQUIRED = ["README.md", "AGENTS.md", "CLAUDE.md", "CHANGELOG.md",
                   "Makefile", "brain.config.json",
                   "memory/learnings.md", "memory/patterns.md"]

MODULE_REQUIRED = {
    "00-context": ["00-context/company-overview.md", "00-context/engagement-scope.md",
                   "00-context/stakeholders.md", "00-context/glossary.md"],
    "01-meetings": ["01-meetings/README.md", "01-meetings/minutes/meeting-template.md"],
    "02-organization": ["02-organization/README.md", "02-organization/ai-policy.md",
                        "02-organization/ownership.md",
                        "02-organization/conventions/engineering.md",
                        "02-organization/conventions/git-workflow.md",
                        "02-organization/conventions/ticketing.md",
                        "02-organization/conventions/communication.md",
                        "02-organization/runbooks/README.md",
                        "02-organization/runbooks/template.md"],
    "03-projects": ["03-projects/README.md"],
    "04-architecture": ["04-architecture/systems-map.md", "04-architecture/repos.yaml",
                        "04-architecture/integrations.md"],
    "05-requirements": ["05-requirements/functional.md", "05-requirements/non-functional.md",
                        "05-requirements/business-rules.md", "05-requirements/open-questions.md"],
    "06-decisions": ["06-decisions/decision-log.md"],
    "07-delivery": ["07-delivery/current-status.md", "07-delivery/action-items.md",
                    "07-delivery/validation-matrix.md",
                    "07-delivery/periodic-validation-check.md"],
    "08-vendors": ["08-vendors/vendor-register.md"],
    "09-references": ["09-references/README.md", "09-references/source-register-template.md"],
    "99-inbox": ["99-inbox/README.md"],
}

STATUSES = ["CONFIRMED", "PENDING VALIDATION", "INFERRED", "SUPERSEDED", "BLOCKED"]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)]*)?\)")
SKIP_PARTS = {".git", "_to_delete", "node_modules"}


def md_files():
    for p in ROOT.rglob("*.md"):
        if not (set(p.parts) & SKIP_PARTS):
            yield p


def main() -> int:
    try:
        cfg = json.loads((ROOT / "brain.config.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: brain.config.json not found"); return 1
    modules = cfg.get("modules", {})
    namespaces = cfg.get("id_namespaces", ["DEC", "SRC", "ACT", "Q", "REQ-FUN", "REQ-NFR", "BR"])

    errors: list[str] = []

    required = list(ALWAYS_REQUIRED)
    for mod, files in MODULE_REQUIRED.items():
        if modules.get(mod, False):
            required += files
    for rel in required:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    # links + IDs + statuses
    id_def_re = re.compile(r"^\s*(?:##\s+|\|\s*)((?:%s)-\d+)\b" % "|".join(namespaces), re.M)
    id_defs: dict[str, list[str]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    pending_by_module: Counter[str] = Counter()

    for md in md_files():
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        module = rel.parts[0] if len(rel.parts) > 1 else rel.name
        pending_by_module[module] += text.count("_PENDING_")
        for s in STATUSES:
            status_counts[s] += len(re.findall(r"\b" + re.escape(s) + r"\b", text))
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).resolve().exists():
                errors.append(f"{rel}: broken link -> {target}")
        if "template" not in md.name and "_project-template" not in str(rel):
            for m in id_def_re.finditer(text):
                id_defs[m.group(1)].append(str(rel))

    for ident, places in sorted(id_defs.items()):
        if len(set(places)) > 1:
            errors.append(f"duplicate ID {ident} defined in: {', '.join(sorted(set(places)))}")

    # decisions without Source
    unsourced = []
    dec = ROOT / "06-decisions/decision-log.md"
    if dec.is_file():
        blocks = re.split(r"^## (?=DEC-\d+)", dec.read_text(encoding="utf-8"), flags=re.M)
        for b in blocks[1:]:
            ident = b.split("—")[0].split("-", 0) or b
            name = b.splitlines()[0].strip()
            if "**Source**" not in b and "**Fuente**" not in b:
                unsourced.append(name)

    # inbox debt
    inbox_debt = []
    inbox = ROOT / "99-inbox"
    if inbox.is_dir():
        for f in inbox.iterdir():
            if f.is_file() and f.name not in ("README.md", ".gitkeep") \
               and not f.name.startswith("processed--"):
                inbox_debt.append(f.name)

    print("Status markers:")
    for s in STATUSES:
        print(f"  {s}: {status_counts[s]}")
    print(f"\n_PENDING_ placeholder debt: {sum(pending_by_module.values())}")
    for mod, n in sorted(pending_by_module.items(), key=lambda kv: -kv[1]):
        if n:
            print(f"  {mod}: {n}")
    if unsourced:
        print(f"\nDecisions without Source ({len(unsourced)}):")
        for u in unsourced:
            print(f"  {u}")
    if inbox_debt:
        print(f"\nUnprocessed inbox files ({len(inbox_debt)}):")
        for f in inbox_debt:
            print(f"  {f}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("\nStructure OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
