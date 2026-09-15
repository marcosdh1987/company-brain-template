#!/usr/bin/env python3
"""Validate the brain: structure (per brain.config.json), links, and semantics.

Checks:
  structural (exit 1 on failure):
    - required files exist for every ACTIVE module
    - relative markdown links resolve
    - duplicate IDs within a namespace (DEC-001 defined twice, etc.)
    - Canvas files under maps/ are valid JSON, and every file-node path and
      every markdown link inside a text card resolves (layout, color, and
      node content are never checked — a Canvas belongs to whoever edits it)
    - work units carry a unit page with complete, in-vocabulary frontmatter
    - the generated indexes are not stale
  reported as debt (never fail the build):
    - decisions without a Source field
    - status-marker counts (CONFIRMED / PENDING VALIDATION / INFERRED /
      SUPERSEDED / BLOCKED) and `_PENDING_` placeholders per module
    - unprocessed inbox files (no `processed--` prefix)
    - Canvas references pointing at a module that is currently inactive
      (deleted on purpose per `make init`'s own advice)
    - work-unit debt: `_PENDING_` frontmatter, no `aliases`, missing tier
      files, and missing status markers where the unit's type owes them
    - possible secrets (path and category only, never the value); set
      `fail_on_secrets: true` in brain.config.json to make them fail
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import urllib.parse
from collections import Counter, defaultdict

from _brain import ROOT, parse_frontmatter, unit_page, work_units

ALWAYS_REQUIRED = ["README.md", "START_HERE.md", "AGENTS.md", "CLAUDE.md",
                   "OPENCODE.md", "CHANGELOG.md", "Makefile", "brain.config.json",
                   "opencode.json",
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
    "03-work": ["03-work/README.md"],
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
    "12-capabilities": ["12-capabilities/README.md", "12-capabilities/capability-register.md"],
    "maps": ["maps/README.md", "maps/home.canvas", "maps/_templates/blank.canvas"],
    "14-people": ["14-people/README.md", "14-people/_templates/person.md",
                  "14-people/_templates/team.md"],
}

STATUSES = ["CONFIRMED", "PENDING VALIDATION", "INFERRED", "SUPERSEDED", "BLOCKED"]
PENDING = "_PENDING_"

# Work-unit frontmatter: the vocabularies live in AGENTS.md and 03-work/README.md.
WORK_FRONTMATTER = ["type", "stage", "tier", "owner", "updated"]
WORK_TYPES = {"client", "opportunity", "internal-product", "initiative"}
WORK_STAGES = {"exploring", "active", "paused", "closed"}
# Rigor follows type, not tier (see AGENTS.md, "Graduated rigor"): these are the
# types whose every non-obvious claim owes a status marker.
RIGOROUS_TYPES = {"client", "opportunity"}
TIER_TEMPLATES = ROOT / "03-work" / "_templates"

# Generators that own their own freshness check. Each must accept `--check` and
# print what is stale; a script that is absent is skipped, so an instance can
# add a generator without editing this file.
CHECKED_GENERATORS = ("build_indexes.py",)

# Heuristics, not a secret scanner: a secret already committed is not fixed by
# failing a build, so this reports for a human to look at. Paths and categories
# only — never the matched value, which would put the secret in the log too.
SECRET_PATTERNS = (
    (re.compile(r"(?i)\bapi[_-]?key\b\s*[:=]\s*[^\s\|<>_`]{12,}"), "API key"),
    (re.compile(r"(?i)\bpassword\b\s*[:=]\s*[^\s\|<>_`]{8,}"), "password"),
    (re.compile(r"(?i)\b(?:secret|token)\b\s*[:=]\s*[^\s\|<>_`]{12,}"), "secret or token"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|xoxb-[A-Za-z0-9-]{20,}|ghp_[A-Za-z0-9]{20,})\b"),
     "provider token"),
)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)]*)?\)")
SKIP_PARTS = {".git", ".superpowers", "_to_delete", "node_modules", "worktrees"}
# Process artifacts (specs/plans), not canonical brain content — they quote
# markdown-with-links as example text, which isn't meant to resolve here.
SKIP_PREFIXES = ("docs/superpowers/",)


def nested_checkout(p: pathlib.Path) -> bool:
    """True if p sits inside a subtree that is its own git checkout.

    A `git worktree add` inside the repo — or a vendored clone — puts a second
    copy of every canonical file on disk. We walk the filesystem, not the git
    index, so without this every ID is a duplicate and every relative link in
    the copy is reported twice. Prune the subtree instead.
    """
    for parent in p.parents:
        if parent == ROOT:
            return False
        if (parent / ".git").exists():
            return True
    return False


def md_files():
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT).as_posix()
        if (set(p.parts) & SKIP_PARTS) or rel.startswith(SKIP_PREFIXES):
            continue
        if nested_checkout(p):
            continue
        yield p


def check_version_drift() -> list[str]:
    """README's `# Company Brain Template — vX.Y` must match CHANGELOG's
    latest `## [X.Y.Z]` entry (major.minor only — patches don't bump it)."""
    errs: list[str] = []
    readme = ROOT / "README.md"
    changelog = ROOT / "CHANGELOG.md"
    if not (readme.is_file() and changelog.is_file()):
        return errs
    readme_m = re.search(r"^#\s+Company Brain Template\s+[-—]\s+v(\d+\.\d+)",
                          readme.read_text(encoding="utf-8"), re.M)
    changelog_m = re.search(r"^##\s+\[(\d+)\.(\d+)\.\d+\]",
                            changelog.read_text(encoding="utf-8"), re.M)
    if not readme_m:
        errs.append("README.md: missing '# Company Brain Template — vX.Y' header")
        return errs
    if not changelog_m:
        errs.append("CHANGELOG.md: missing a '## [X.Y.Z]' entry")
        return errs
    changelog_version = f"{changelog_m.group(1)}.{changelog_m.group(2)}"
    if readme_m.group(1) != changelog_version:
        errs.append(
            f"version drift: README.md says v{readme_m.group(1)}, "
            f"CHANGELOG.md latest entry is {changelog_m.group(1)}.{changelog_m.group(2)}.x"
        )
    return errs


def check_canvas_files(modules: dict) -> tuple[list[str], list[str]]:
    """Canvas is a view, not a source of truth: validate that it opens and
    every file-node link resolves. Never validate layout, color, group
    contents, or 'which entities should appear' — that's user-owned.

    Two kinds of reference are checked, and they resolve differently: a file
    node's path is vault-relative to the repo root, while a markdown link
    inside a text card resolves relative to the canvas's own directory. Both
    are normalised to a repo-relative path before the verdict, because the
    verdict keys on the first path segment — split them into two checkers and
    one copy of that rule drifts.

    A dangling reference is a hard error UNLESS its target's first path
    segment names a module that is currently INACTIVE per brain.config.json —
    that's expected/harmless (the user deliberately turned the module off and
    deleted its folder, per make init's own "Inactive modules (folders may be
    deleted)" advice), so it's reported as debt instead."""
    errs: list[str] = []
    debt: list[str] = []
    maps_dir = ROOT / "maps"
    if not maps_dir.is_dir():
        return errs, debt
    for canvas in sorted(maps_dir.rglob("*.canvas")):
        rel = canvas.relative_to(ROOT)
        try:
            data = json.loads(canvas.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{rel}: invalid JSON ({e})")
            continue

        def verdict(rel_target: str, node_id: str, kind: str) -> None:
            msg = f"{rel}: node {node_id} {kind} -> {rel_target}"
            first_segment = rel_target.split("/", 1)[0]
            if first_segment in modules and not modules.get(first_segment, False):
                debt.append(f"{msg} (module '{first_segment}' is inactive)")
            else:
                errs.append(msg)

        for node in data.get("nodes", []):
            if node.get("type") == "file":
                target = urllib.parse.unquote(node.get("file", ""))
                if target and not (ROOT / target).exists():
                    verdict(target, node.get("id", "?"), "references missing file")
            elif node.get("type") == "text":
                for m in LINK_RE.finditer(node.get("text", "")):
                    target = urllib.parse.unquote(m.group(1))
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    resolved = (canvas.parent / target).resolve()
                    if resolved.exists():
                        continue
                    try:
                        rel_target = resolved.relative_to(ROOT).as_posix()
                    except ValueError:
                        rel_target = target
                    verdict(rel_target, node.get("id", "?"), "broken link")
    return errs, debt


def tier_files(tier: str) -> list[str] | None:
    """The files a tier owes, derived from the shipped template folder.

    The tier contract *is* `03-work/_templates/t<N>/`, so the two cannot drift,
    and an instance that adds a file to its own tier template gets it enforced
    for free. Returns None when the tier has no template at all — which is what
    makes "unknown tier" an actionable message instead of a vocabulary error.
    """
    d = TIER_TEMPLATES / f"t{tier}"
    if not d.is_dir():
        return None
    page = unit_page(d).name
    return sorted(f.name for f in d.glob("*.md") if f.name != page)


def check_work_units() -> tuple[list[str], list[str]]:
    """Every work unit has a unit page whose frontmatter is complete and in
    vocabulary. Incompleteness is an error; a `_PENDING_` placeholder is debt.

    The distinction matters: copying a tier template is the documented first
    step of creating a work unit, and the templates ship `_PENDING_`. Treating
    that as an error would fail the build for doing the right thing.
    """
    errors: list[str] = []
    debt: list[str] = []
    for unit in work_units():
        page = unit_page(unit)
        rel = page.relative_to(ROOT).as_posix()
        if not page.is_file():
            errors.append(f"03-work/{unit.name}: missing unit page {page.name}")
            continue
        fm = parse_frontmatter(page.read_text(encoding="utf-8"))
        if not fm:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        for key in WORK_FRONTMATTER:
            value = fm.get(key, "")
            if not value:
                errors.append(f"{rel}: frontmatter missing `{key}`")
            elif value == PENDING:
                debt.append(f"{rel}: `{key}` is still {PENDING}")
        if not fm.get("aliases"):
            debt.append(f"{rel}: no `aliases` (the display name an index shows)")

        utype = fm.get("type", "")
        if utype and utype != PENDING and utype not in WORK_TYPES:
            errors.append(f"{rel}: unknown type `{utype}` "
                          f"(expected one of: {', '.join(sorted(WORK_TYPES))})")
        stage = fm.get("stage", "")
        if stage and stage != PENDING and stage not in WORK_STAGES:
            errors.append(f"{rel}: unknown stage `{stage}` "
                          f"(expected one of: {', '.join(sorted(WORK_STAGES))})")

        tier = fm.get("tier", "")
        if tier and tier != PENDING:
            owed = tier_files(tier)
            if owed is None:
                errors.append(f"{rel}: unknown tier `{tier}` "
                              f"(no 03-work/_templates/t{tier}/ to define it)")
            else:
                absent = [f for f in owed if not (unit / f).is_file()]
                if absent:
                    debt.append(f"03-work/{unit.name} (tier {tier}): "
                                f"missing {', '.join(absent)}")

        # Rigor follows type: only these owe a status marker on every document.
        if utype in RIGOROUS_TYPES:
            for md in sorted(unit.rglob("*.md")):
                text = md.read_text(encoding="utf-8")
                if not any(s in text for s in STATUSES):
                    debt.append(f"{md.relative_to(ROOT).as_posix()} "
                                f"(type {utype}): no status marker")
    return errors, debt


def check_indexes() -> list[str]:
    """Delegate index freshness to each generator's own `--check` mode.

    `make validate` is one command on purpose: running the generators first
    would abort make before the debt report, so a single stale index would
    hide every other finding.
    """
    errs: list[str] = []
    for name in CHECKED_GENERATORS:
        script = ROOT / "scripts" / name
        if not script.is_file():
            continue
        proc = subprocess.run([sys.executable, str(script), "--check"],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            errs.append((proc.stdout + proc.stderr).strip()
                        or f"{name} --check failed")
    return errs


def main() -> int:
    try:
        cfg = json.loads((ROOT / "brain.config.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: brain.config.json not found"); return 1
    modules = cfg.get("modules", {})
    namespaces = cfg.get("id_namespaces", ["DEC", "SRC", "ACT", "Q", "REQ-FUN", "REQ-NFR", "BR"])

    errors: list[str] = []
    canvas_debt: list[str] = []
    errors += check_version_drift()
    errors += check_indexes()
    if modules.get("maps", False):
        canvas_errs, canvas_debt = check_canvas_files(modules)
        errors += canvas_errs

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
    secret_debt: list[str] = []

    for md in md_files():
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        module = rel.parts[0] if len(rel.parts) > 1 else rel.name
        pending_by_module[module] += text.count("_PENDING_")
        for status in STATUSES:
            status_counts[status] += len(
                re.findall(r"\b" + re.escape(status) + r"\b", text))
        # One finding per file: the point is that a human looks at the file.
        category = next((c for pat, c in SECRET_PATTERNS if pat.search(text)), None)
        if category:
            secret_debt.append(f"{rel}: possible {category}")
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            # Editors percent-encode a link to a filename with spaces or an
            # em-dash; the link is correct, so decode before resolving.
            if not (md.parent / urllib.parse.unquote(target)).resolve().exists():
                errors.append(f"{rel}: broken link -> {target}")
        if "template" not in md.name and "_templates" not in str(rel) and md.name != "INDEX.md":
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

    work_errors, work_debt = check_work_units()
    errors += work_errors

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
    if canvas_debt:
        print(f"\nCanvas nodes pointing at inactive modules ({len(canvas_debt)}):")
        for c in canvas_debt:
            print(f"  {c}")
    if work_debt:
        print(f"\nWork-unit debt ({len(work_debt)}):")
        for w in work_debt:
            print(f"  {w}")
    if secret_debt:
        print(f"\nPossible secrets ({len(secret_debt)}) — review and remove:")
        for w in secret_debt:
            print(f"  {w}")
        if cfg.get("fail_on_secrets", False):
            errors += secret_debt

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("\nStructure OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
