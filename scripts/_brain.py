#!/usr/bin/env python3
"""Contracts shared by the brain's generators and its validator.

Everything here exists so a contract has exactly one definition in the repo.
Two scripts that each hardcode the same convention drift; the first thing that
drifts is the one nobody re-reads.

Nothing here writes, prints, or validates — import it freely.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The work-unit page: the entry document of `03-work/<unit>/`.
#
# This template's contract is `<unit>/overview.md`. A future MAJOR moves to
# `<unit>/<unit>.md`, so that an editor tab reads the unit's own name instead
# of a wall of identical "overview" tabs, and a `[[unit]]` wikilink resolves to
# the page rather than the folder. Set `work_unit_page` to "" in
# brain.config.json to opt into that shape early; everything that needs the
# page goes through unit_page(), so the switch is a config edit, never a code
# change.
DEFAULT_WORK_PAGE = "overview.md"


def load_config() -> dict:
    cfg = ROOT / "brain.config.json"
    if not cfg.is_file():
        return {}
    try:
        return json.loads(cfg.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def work_page_name() -> str:
    """The configured unit-page filename, or "" for the `<slug>.md` shape."""
    cfg = load_config()
    return cfg.get("work_unit_page", DEFAULT_WORK_PAGE)


def unit_page(unit_dir: pathlib.Path) -> pathlib.Path:
    """The unit page of a work-unit directory, under either contract."""
    name = work_page_name()
    return unit_dir / (name or f"{unit_dir.name}.md")


def work_units() -> list[pathlib.Path]:
    """Work-unit directories, `_`-prefixed ones excluded.

    `03-work/_templates/` is not a work unit: it is the tier templates. A
    checker that forgets this reports the template set as a malformed unit.
    """
    work = ROOT / "03-work"
    if not work.is_dir():
        return []
    return sorted(d for d in work.iterdir()
                  if d.is_dir() and not d.name.startswith("_"))


def parse_frontmatter(text: str) -> dict[str, str]:
    """Flat scalar YAML frontmatter as a dict. No dependency on PyYAML.

    Deliberately shallow: the brain's frontmatter is flat scalars and short
    inline lists, and a template that needs no third-party package installs
    with nothing but Python.
    """
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not kv:
            continue
        value = kv.group(2).strip()
        # A trailing `# …` comment documents the allowed values right where the
        # field is filled in — the template's own frontmatter uses them — so it
        # is part of the line, never part of the value. Only strip it from an
        # unquoted value, where `#` cannot be meaningful.
        if value[:1] not in ('"', "'"):
            value = re.sub(r"\s+#.*$", "", value).strip()
        fields[kv.group(1)] = value.strip('"').strip("'")
    return fields
