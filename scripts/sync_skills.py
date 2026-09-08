#!/usr/bin/env python3
"""Sync external skills from the engineering harness and regenerate native
tool projections so Claude Code, Codex, Antigravity, and OpenCode discover every
skill.

Config (brain.config.json):
    "harness": {
        "source": "../ml-python-base",
        "external_skills": ["brainstorming", "writing-plans", ...]
    }

What it does:
  1. Pulls each listed skill from the harness source — accepts both shapes:
     flat `.github/skills/<name>.md` or dir `.github/skills-external/<name>/`
     — into this repo's `.github/skills-external/<name>/SKILL.md`, recording
     a sha256 per skill in `skills-lock.json`.
  2. Regenerates `.claude/skills/`, `.codex/skills/`, `.agents/skills/`,
     `.opencode/skills/` from internal skills (`.github/skills/`, either a flat
     `<name>.md` or a `<name>/SKILL.md` folder with its helper files) plus the
     synced external dirs. Each projection carries a `.generated-manifest.tsv`;
     do not edit by hand.
  3. Ensures `.agents/rules/brain-rules.md` points Antigravity at AGENTS.md.
  4. Rewrites the generated skills block in `OPENCODE.md` (between the
     BEGIN/END GENERATED SKILLS sentinels) with the projected skill list.

Idempotent. Run after every harness release adoption.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = ROOT / "brain.config.json"
EXTERNAL = ROOT / ".github" / "skills-external"
INTERNAL = ROOT / ".github" / "skills"
LOCK = ROOT / "skills-lock.json"
PROJECTIONS = [ROOT / ".claude" / "skills",
               ROOT / ".codex" / "skills",
               ROOT / ".agents" / "skills",
               ROOT / ".opencode" / "skills"]
OPENCODE_MD = ROOT / "OPENCODE.md"
SKILLS_BLOCK = re.compile(r"(<!-- BEGIN GENERATED SKILLS[^\n]*-->\n).*?(<!-- END GENERATED SKILLS -->)", re.S)


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(path.rglob("*") if path.is_dir() else [path]):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


def find_in_harness(harness: pathlib.Path, name: str) -> pathlib.Path | None:
    for cand in (harness / ".github" / "skills-external" / name,
                 harness / ".github" / "skills" / f"{name}.md",
                 harness / ".claude" / "skills" / name):
        if cand.exists():
            return cand
    return None


def install_external(src: pathlib.Path, name: str) -> pathlib.Path:
    dest = EXTERNAL / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    if src.is_dir():
        for item in src.iterdir():
            if item.name.startswith("."):
                continue
            (shutil.copytree if item.is_dir() else shutil.copy2)(item, dest / item.name)
        if not (dest / "SKILL.md").exists():
            mds = list(dest.glob("*.md"))
            if mds:
                mds[0].rename(dest / "SKILL.md")
    else:
        shutil.copy2(src, dest / "SKILL.md")
    return dest


def internal_skills():
    """Internal skills in either supported shape, sorted by name.

    Two shapes are accepted under `.github/skills/`:
      - a flat `<name>.md` — a skill that is only prose;
      - a `<name>/` directory with `SKILL.md` as its entry point, bundling the
        scripts, templates or references the skill runs.

    A directory without SKILL.md is not a skill: it is reported and skipped
    rather than silently ignored, because the author would otherwise only find
    out when the skill never triggers.
    """
    if not INTERNAL.is_dir():
        return []
    found = []
    for p in sorted(INTERNAL.iterdir(), key=lambda p: p.name):
        if p.name.startswith("."):
            continue
        if p.is_dir():
            if (p / "SKILL.md").is_file():
                found.append(p)
            else:
                print(f"WARNING: {p.relative_to(ROOT)}/ has no SKILL.md and was IGNORED.")
                print(f"         A folder skill needs {p.name}/SKILL.md as its entry point.")
        elif p.suffix == ".md" and p.name != "README.md":
            found.append(p)
    return found


def regenerate_projections():
    entries = []  # (name, kind, source_path)
    for f in internal_skills():
        entries.append((f.stem, "internal", f))
    if EXTERNAL.is_dir():
        for d in sorted(EXTERNAL.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                entries.append((d.name, "external", d))
    for proj in PROJECTIONS:
        if proj.exists():
            shutil.rmtree(proj)
        proj.mkdir(parents=True)
        rows = []
        for name, kind, src in entries:
            dest = proj / name
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                dest.mkdir()
                shutil.copy2(src, dest / "SKILL.md")
            rows.append(f"{name}\t{kind}\t{src.relative_to(ROOT)}")
        (proj / ".generated-manifest.tsv").write_text(
            "# generated by scripts/sync_skills.py — do not edit\n" + "\n".join(rows) + "\n",
            encoding="utf-8")
    return entries


def ensure_antigravity_rules():
    rules = ROOT / ".agents" / "rules"
    rules.mkdir(parents=True, exist_ok=True)
    f = rules / "brain-rules.md"
    if not f.exists():
        f.write_text(
            "# Workspace rules — Company Brain\n\n"
            "All operating rules for this repository live in `AGENTS.md` at the\n"
            "repo root — read it first and follow it. Skills are projected into\n"
            "`.agents/skills/` (generated; do not edit — run `make sync-skills`).\n",
            encoding="utf-8")


def skill_description(src: pathlib.Path) -> str:
    """Read `description:` from a skill's YAML frontmatter (single-line only)."""
    md = src / "SKILL.md" if src.is_dir() else src
    text = md.read_text(encoding="utf-8") if md.is_file() else ""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    d = re.search(r"^description:\s*(.+)$", m.group(1), re.M)
    return d.group(1).strip().strip("\"'") if d else ""


def render_opencode_skills_block(entries):
    """Rewrite the sentinel-delimited skills list in OPENCODE.md."""
    if not OPENCODE_MD.is_file():
        return
    lines = ["The governed skills below are projected into `.opencode/skills/`. "
             "Internal skills are the source of truth and take precedence over "
             "external synced skills on name conflicts.", ""]
    for kind, title in (("internal", "Internal skills"), ("external", "External synced skills")):
        rows = [(n, skill_description(s)) for n, k, s in entries if k == kind]
        if not rows:
            continue
        lines.append(f"**{title}:**")
        lines.append("")
        lines += [f"- `{n}`" + (f" — {d}" if d else "") for n, d in rows]
        lines.append("")
    lines.append("Refresh this layout with `make sync-skills`.")
    body = "\n".join(lines) + "\n"
    text = OPENCODE_MD.read_text(encoding="utf-8")
    new, n = SKILLS_BLOCK.subn(lambda m: m.group(1) + body + m.group(2), text, count=1)
    if n == 0:
        print("WARNING: OPENCODE.md has no GENERATED SKILLS sentinels; block not written")
    elif new != text:
        OPENCODE_MD.write_text(new, encoding="utf-8")


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8")) if CFG.is_file() else {}
    harness_cfg = cfg.get("harness", {})
    source = harness_cfg.get("source", "../ml-python-base")
    wanted = harness_cfg.get("external_skills", [])
    harness = (ROOT / source).resolve()

    lock = {"source": source, "skills": {}}
    missing = []
    if wanted and not harness.is_dir():
        print(f"WARNING: harness source not found at {harness} — skipping external sync,")
        print("         regenerating projections from what is already present.")
        wanted = []
    for name in wanted:
        src = find_in_harness(harness, name)
        if src is None:
            missing.append(name)
            continue
        dest = install_external(src, name)
        lock["skills"][name] = {"origin": str(src.relative_to(harness)),
                                "sha256": sha256(dest)}
        print(f"[sync] {name}  <-  {src.relative_to(harness)}")
    if wanted:
        LOCK.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

    entries = regenerate_projections()
    ensure_antigravity_rules()
    render_opencode_skills_block(entries)
    print(f"[proj] {len(entries)} skills projected to .claude/ .codex/ .agents/ .opencode/")
    if missing:
        print(f"WARNING: not found in harness: {', '.join(missing)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
