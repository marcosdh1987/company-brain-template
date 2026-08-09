#!/usr/bin/env python3
"""Validate the brain's structure and internal links.

Checks: required files exist, relative markdown links resolve, and reports
_PENDING_ / _STALE_ debt per section. Exit code 1 on structural
errors or broken links; markers are reported but do not fail the build.
"""
from __future__ import annotations

import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED = [
    "README.md", "CLAUDE.md", "AGENTS.md", "CHANGELOG.md", "Makefile",
    "brain/00-index.md", "brain/ai-policy.md", "brain/glossary.md",
    "brain/domain/overview.md", "brain/domain/entities.md",
    "brain/domain/business-rules.md", "brain/domain/stakeholders.md",
    "brain/decisions/README.md", "brain/decisions/template.md",
    "brain/conventions/engineering.md", "brain/conventions/git-workflow.md",
    "brain/conventions/communication.md",
    "brain/architecture/systems-map.md", "brain/architecture/integrations.md",
    "brain/runbooks/README.md", "brain/runbooks/template.md",
    "brain/team/ownership.md",
    "memory/learnings.md", "memory/patterns.md",
    "docs/adoption.md", "docs/maintenance.md",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#]+)(#[^)]*)?\)")


def main() -> int:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    markers: Counter[str] = Counter()
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        section = rel.parts[0] if len(rel.parts) > 1 else rel.name
        markers[section] += text.count("_PENDING_") + text.count("_STALE_")
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).resolve().exists():
                errors.append(f"{rel}: broken link -> {target}")

    total = sum(markers.values())
    print(f"Marker debt (_PENDING_/_STALE_): {total}")
    for section, n in sorted(markers.items(), key=lambda kv: -kv[1]):
        if n:
            print(f"  {section}: {n}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("\nStructure OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
