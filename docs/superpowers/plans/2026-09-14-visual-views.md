# Visual Views Layer (`maps/`) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an optional, purely-presentational Obsidian Canvas views layer (`maps/`) and an optional `14-people/` navigation-entity module to the company-brain-template, without changing behavior for any brain that doesn't opt in.

**Architecture:** Both additions follow the exact pattern the repo already uses for `12-capabilities/`: the module's files ship statically in the template repo; a boolean in `brain.config.json.modules` only controls whether `validate_structure.py` requires/checks it and whether `make init`'s existing "inactive modules" report lists it. No canvas is ever generated or rewritten by code — `make init`'s placeholder-replacement loop already skips `.canvas` (not in `TEXT_EXT`), and `make validate`/`make index` never open `maps/` for writing. The only new write path is an explicit `make new-view NAME=<slug>` target that refuses to overwrite an existing file.

**Tech Stack:** Python 3 (stdlib only: `json`, `pathlib`, `re`), Make, JSON Canvas format (`.canvas` = JSON with `nodes`/`edges`), Markdown + YAML frontmatter.

**Spec:** `docs/superpowers/specs/2026-09-14-visual-views-design.md`

## Global Constraints

- Canvas files are never generated, templated, or filtered by profile — they are static, hand-authored starters shipped in git, same as every other module's default content.
- No code may open a `.canvas` file for writing except `make new-view`, and only when the target path does not already exist.
- `make validate` and `make index` must not modify any file under `maps/` — verified by hash comparison in the final task.
- Canvas validation checks only: valid JSON, and every `type: "file"` node's `file` path resolves to an existing file relative to repo root. No checks on position, size, color, group contents, or "which entities should appear."
- `14-people/` frontmatter is documented inline in the templates (not schema-enforced), consistent with how `03-work/_templates` documents its frontmatter today.
- `14-people/README.md` must state the allowed field list (role, team, public/professional location, specialty, project, assignment, operational meetings, work relationships) and the disallowed list (compensation, health, disciplinary records, private performance feedback, confidential 1:1 content, unnecessary personal information) verbatim from the spec.
- Backwards compatibility: existing brains whose `brain.config.json` lacks the `maps`/`14-people` keys must continue to validate exactly as before — both `validate_structure.py` and `build_indexes.py` already treat a missing module key as inactive (`modules.get(mod, False)`).
- Version bump: `2.1.0` -> `2.2.0` (README header + CHANGELOG entry), per the repo's semver rule (`MINOR` = new sections/templates).

---

### Task 1: `maps/` static content — README, five starter Canvas views, blank template

**Files:**
- Create: `maps/README.md`
- Create: `maps/home.canvas`
- Create: `maps/brain-overview.canvas`
- Create: `maps/portfolio.canvas`
- Create: `maps/management.canvas`
- Create: `maps/architecture-capabilities.canvas`
- Create: `maps/_templates/blank.canvas`

**Interfaces:**
- Produces: the file set `MODULE_REQUIRED["maps"]` (Task 3) will point at:
  `maps/README.md`, `maps/home.canvas`, `maps/_templates/blank.canvas`.
- Produces: file-node targets used across all five canvases must already
  exist in this repo today (they do — `00-context/company-overview.md`,
  `03-work/README.md`, `06-decisions/decision-log.md`,
  `07-delivery/current-status.md`, `07-delivery/roadmap.md`,
  `12-capabilities/README.md`, `12-capabilities/capability-register.md`,
  `04-architecture/systems-map.md`, `04-architecture/repos.yaml`,
  `04-architecture/integrations.md`, `01-meetings/README.md`,
  `99-inbox/README.md`, `09-references/README.md`,
  `05-requirements/functional.md`, `00-context/stakeholders.md`,
  `02-organization/ownership.md`, `08-vendors/vendor-register.md`) —
  except `14-people/README.md`, which Task 2 creates before this task's
  validation step runs.

- [ ] **Step 1: Create `maps/home.canvas`**

```json
{
  "nodes": [
    {"id": "home-title", "type": "text", "x": -40, "y": -220, "width": 940, "height": 130,
     "text": "# Company Brain — Home\n\nThis canvas is a **launcher**, not a copy of the knowledge. Click a card to open the real Markdown hub for that section — editing happens there, not here. If Canvas ever disappears, nothing is lost: every card below is a real file already in this repo."},
    {"id": "home-context", "type": "file", "file": "00-context/company-overview.md", "x": 0, "y": 0, "width": 260, "height": 100},
    {"id": "home-work", "type": "file", "file": "03-work/README.md", "x": 300, "y": 0, "width": 260, "height": 100},
    {"id": "home-decisions", "type": "file", "file": "06-decisions/decision-log.md", "x": 600, "y": 0, "width": 260, "height": 100},
    {"id": "home-people", "type": "file", "file": "14-people/README.md", "x": 0, "y": 140, "width": 260, "height": 100},
    {"id": "home-delivery", "type": "file", "file": "07-delivery/current-status.md", "x": 300, "y": 140, "width": 260, "height": 100},
    {"id": "home-capabilities", "type": "file", "file": "12-capabilities/README.md", "x": 600, "y": 140, "width": 260, "height": 100},
    {"id": "home-architecture", "type": "file", "file": "04-architecture/systems-map.md", "x": 0, "y": 280, "width": 260, "height": 100},
    {"id": "home-meetings", "type": "file", "file": "01-meetings/README.md", "x": 300, "y": 280, "width": 260, "height": 100},
    {"id": "home-inbox", "type": "file", "file": "99-inbox/README.md", "x": 600, "y": 280, "width": 260, "height": 100}
  ],
  "edges": []
}
```

- [ ] **Step 2: Create `maps/brain-overview.canvas`**

```json
{
  "nodes": [
    {"id": "bo-title", "type": "text", "x": -40, "y": -220, "width": 1200, "height": 110,
     "text": "# Evidence -> Knowledge Pipeline\n\nLeft column is raw evidence. Right column is canonical, statused knowledge. Promotion (analyze, validate, cite a source) is what turns one into the other — never a silent copy."},
    {"id": "bo-inbox", "type": "file", "file": "99-inbox/README.md", "x": 0, "y": 0, "width": 260, "height": 90},
    {"id": "bo-meetings", "type": "file", "file": "01-meetings/README.md", "x": 0, "y": 130, "width": 260, "height": 90},
    {"id": "bo-references", "type": "file", "file": "09-references/README.md", "x": 0, "y": 260, "width": 260, "height": 90},
    {"id": "bo-decisions", "type": "file", "file": "06-decisions/decision-log.md", "x": 560, "y": 0, "width": 260, "height": 90},
    {"id": "bo-requirements", "type": "file", "file": "05-requirements/functional.md", "x": 560, "y": 130, "width": 260, "height": 90},
    {"id": "bo-context", "type": "file", "file": "00-context/company-overview.md", "x": 560, "y": 260, "width": 260, "height": 90},
    {"id": "bo-work", "type": "file", "file": "03-work/README.md", "x": 560, "y": 390, "width": 260, "height": 90}
  ],
  "edges": [
    {"id": "bo-e1", "fromNode": "bo-inbox", "fromSide": "right", "toNode": "bo-decisions", "toSide": "left", "label": "promoted"},
    {"id": "bo-e2", "fromNode": "bo-meetings", "fromSide": "right", "toNode": "bo-requirements", "toSide": "left", "label": "promoted"},
    {"id": "bo-e3", "fromNode": "bo-references", "fromSide": "right", "toNode": "bo-context", "toSide": "left", "label": "promoted"}
  ]
}
```

- [ ] **Step 3: Create `maps/portfolio.canvas`**

```json
{
  "nodes": [
    {"id": "pf-title", "type": "text", "x": -40, "y": -160, "width": 900, "height": 90,
     "text": "# Portfolio\n\nStarter view for consulting/delivery profiles. Duplicate this canvas per client, or add one file node per active work unit under `03-work/`."},
    {"id": "pf-work", "type": "file", "file": "03-work/README.md", "x": 0, "y": 0, "width": 260, "height": 100},
    {"id": "pf-status", "type": "file", "file": "07-delivery/current-status.md", "x": 300, "y": 0, "width": 260, "height": 100},
    {"id": "pf-roadmap", "type": "file", "file": "07-delivery/roadmap.md", "x": 600, "y": 0, "width": 260, "height": 100},
    {"id": "pf-vendors", "type": "file", "file": "08-vendors/vendor-register.md", "x": 0, "y": 140, "width": 260, "height": 100},
    {"id": "pf-stakeholders", "type": "file", "file": "00-context/stakeholders.md", "x": 300, "y": 140, "width": 260, "height": 100}
  ],
  "edges": []
}
```

- [ ] **Step 4: Create `maps/management.canvas`**

```json
{
  "nodes": [
    {"id": "mg-title", "type": "text", "x": -40, "y": -220, "width": 1000, "height": 150,
     "text": "# Management\n\nStarter view for team-shaped brains. Add one file node per real person/team under `14-people/` (duplicate `_templates/person.md` and `_templates/team.md`), then link them here — Company -> Team -> Person -> Client/Project/Meeting. Nothing about compensation, health, or private feedback belongs in `14-people/` — see `14-people/README.md`."},
    {"id": "mg-people", "type": "file", "file": "14-people/README.md", "x": 0, "y": 0, "width": 260, "height": 100},
    {"id": "mg-ownership", "type": "file", "file": "02-organization/ownership.md", "x": 300, "y": 0, "width": 260, "height": 100},
    {"id": "mg-work", "type": "file", "file": "03-work/README.md", "x": 600, "y": 0, "width": 260, "height": 100},
    {"id": "mg-stakeholders", "type": "file", "file": "00-context/stakeholders.md", "x": 0, "y": 140, "width": 260, "height": 100},
    {"id": "mg-meetings", "type": "file", "file": "01-meetings/README.md", "x": 300, "y": 140, "width": 260, "height": 100}
  ],
  "edges": []
}
```

- [ ] **Step 5: Create `maps/architecture-capabilities.canvas`**

```json
{
  "nodes": [
    {"id": "ac-title", "type": "text", "x": -40, "y": -160, "width": 900, "height": 90,
     "text": "# Architecture & Capabilities\n\nStarter view for engineering-shaped brains: what systems exist, and what the org can actually ship, by maturity."},
    {"id": "ac-systems", "type": "file", "file": "04-architecture/systems-map.md", "x": 0, "y": 0, "width": 260, "height": 100},
    {"id": "ac-repos", "type": "file", "file": "04-architecture/repos.yaml", "x": 300, "y": 0, "width": 260, "height": 100},
    {"id": "ac-integrations", "type": "file", "file": "04-architecture/integrations.md", "x": 600, "y": 0, "width": 260, "height": 100},
    {"id": "ac-capabilities", "type": "file", "file": "12-capabilities/README.md", "x": 0, "y": 140, "width": 260, "height": 100},
    {"id": "ac-register", "type": "file", "file": "12-capabilities/capability-register.md", "x": 300, "y": 140, "width": 260, "height": 100}
  ],
  "edges": []
}
```

- [ ] **Step 6: Create `maps/_templates/blank.canvas`**

```json
{
  "nodes": [],
  "edges": []
}
```

- [ ] **Step 7: Create `maps/README.md`**

```markdown
# maps/ — visual views

This folder is an optional **presentation layer**, mainly for
[Obsidian](https://obsidian.md). It holds `.canvas` files: visual,
clickable maps over the knowledge that already lives in this repo's
Markdown.

**Knowledge != Views.** The facts live in Markdown + frontmatter +
wikilinks. A Canvas is a navigable arrangement of links to that
knowledge — never a second place a fact can live. If every file in this
folder vanished, nothing in the brain would be lost; you'd just be back
to browsing folders. See `AGENTS.md`'s "Views (`maps/`) are not
knowledge" section for the full rule set.

## What's here

| View | Purpose | Most useful for |
|---|---|---|
| `home.canvas` | Launcher — one card per major section, pointing at its real hub file | every profile |
| `brain-overview.canvas` | The evidence → knowledge pipeline as a diagram | `full` |
| `portfolio.canvas` | Work units, delivery status, roadmap, vendors | `consulting`, `consulting-company`, `delivery-oversight`, `client-engagement` |
| `management.canvas` | Team → person → client/project/meeting navigation | `team`, `engineering-management`, `consulting-company` |
| `architecture-capabilities.canvas` | Systems, repos, integrations, and shipped capabilities | `development`, `engineering-management`, `consulting-company` |

All five ship in every brain regardless of profile — the "most useful
for" column is a suggestion, not an enforced rule. If a card points at a
module your profile left inactive, the linked file still exists (module
folders are never deleted automatically); delete the card, or the whole
canvas, if you don't want it. This mirrors how any other optional
module's folder can be deleted once a profile turns it off.

## Editing is expected

**Feel free to duplicate, rearrange, simplify, or create new Canvas
views.** Different people can have different maps over the exact same
knowledge — that's a feature. Two conventions keep this simple:

- A tracked, team-shared view is a normal `maps/*.canvas` file, committed
  like any other doc.
- A personal view — yours alone, not meant for the team — is named
  `maps/*.local.canvas`. It's gitignored, so it never needs a commit or a
  review.

Example: `maps/management.canvas` (shared) next to
`maps/management-marcos.local.canvas` (personal layout, same underlying
files).

## Creating a new view

```bash
make new-view NAME=my-view   # creates maps/my-view.canvas (blank)
```

This refuses to run if `maps/my-view.canvas` already exists — it never
overwrites a view you've already started editing.

## What never touches these files

`make validate` and `make index` only ever **read** `maps/*.canvas` (to
check it's valid JSON and that file-node links resolve) — they never
write to it. `make init` doesn't open `.canvas` files at all. The only
commands that create or write a Canvas are the one-time template
checkout and `make new-view` above. Once a Canvas exists, it's yours.

## Related

- `docs/obsidian.md` — opening this repo as a Vault, Graph, Backlinks,
  Properties.
- `AGENTS.md` — the architectural rules for views vs. knowledge.
```

- [ ] **Step 8: Verify each `.canvas` file is valid JSON with resolvable file-node paths**

Run (from repo root):
```bash
python3 -c "
import json, pathlib
root = pathlib.Path('.')
for p in sorted(root.glob('maps/**/*.canvas')):
    data = json.loads(p.read_text())
    for n in data.get('nodes', []):
        if n.get('type') == 'file':
            target = root / n['file']
            assert target.exists(), f'{p}: missing {n[\"file\"]}'
    print(f'OK {p}')
"
```
Expected: `OK maps/architecture-capabilities.canvas`, `OK maps/brain-overview.canvas`,
`OK maps/home.canvas`, `OK maps/management.canvas`, `OK maps/portfolio.canvas`,
`OK maps/_templates/blank.canvas` — no `AssertionError`. (`home.canvas` and
`management.canvas` reference `14-people/README.md`, which doesn't exist
yet — this step will fail with a clear `AssertionError` until Task 2 is
done; that's expected. Note it and continue; the plan's Task 2 must land
before this check can pass, so run it again at the end of Task 2 instead
of insisting it pass here.)

- [ ] **Step 9: Commit**

```bash
git add maps/
git commit -m "Add optional maps/ visual views layer (starter Canvas views)"
```

---

### Task 2: `14-people/` static content — README and Person/Team templates

**Files:**
- Create: `14-people/README.md`
- Create: `14-people/_templates/person.md`
- Create: `14-people/_templates/team.md`

**Interfaces:**
- Produces: `MODULE_REQUIRED["14-people"]` (Task 3) will point at these
  three files.
- Produces: `type: person` and `type: team` frontmatter shapes that
  `maps/management.canvas` (Task 1) and `maps/home.canvas` (Task 1)
  reference via `14-people/README.md`.

- [ ] **Step 1: Create `14-people/README.md`**

```markdown
# 14-people — Person & Team entities

Optional module. Minimal `person` and `team` entities for **navigation
and context**, not an HRIS. The only reason this module exists is so
Obsidian's Graph and Backlinks — and any agent following wikilinks — can
answer "who's on this, what team are they on, what are they working
on" by clicking or by grep, without a spreadsheet.

Off by default; on by default for the `team`, `engineering-management`,
and `consulting-company` profiles (`brain.config.json` →
`modules["14-people"]`).

## Privacy boundary — read this before adding anyone

**Allowed** (shareable, professional, operational):
- role
- team
- public/professional location
- specialty
- project
- assignment
- operational meetings
- work relationships

**Never store here** (this is a hard boundary, not a style preference):
- compensation
- health
- disciplinary records
- private performance feedback
- confidential 1:1 content
- unnecessary personal information

If a fact about a person doesn't fit the allowed list, it doesn't belong
in this module — full stop. Route it to whatever system your
organization already uses for that (HRIS, private 1:1 notes, etc.), and
reference that system's *location* here if you must, never its content.

## Contents

- `_templates/person.md` — one file per person, e.g. `14-people/jane-doe.md`
- `_templates/team.md` — one file per team, e.g. `14-people/machine-learning.md`

Frontmatter is documented inline in each template, not schema-enforced —
consistent with how `03-work/_templates` documents its frontmatter.
Link a person to their team, projects, and assignments with wikilinks
(`"[[Machine Learning]]"`) so Obsidian's Graph and Backlinks make the
org structure explorable without a separate diagram.
```

- [ ] **Step 2: Create `14-people/_templates/person.md`**

```markdown
---
type: person
name: _PENDING_
role: _PENDING_
team: "[[_PENDING_]]"
assignments: []
projects: []
---

# _PENDING_

Copy this file to `14-people/<first-last>.md`, fill in the frontmatter,
then link it from their team's `members` list and from any work unit or
client they're assigned to.

Only the fields above and free-form professional notes belong here — see
the privacy boundary in `14-people/README.md` before adding anything
else.
```

- [ ] **Step 3: Create `14-people/_templates/team.md`**

```markdown
---
type: team
name: _PENDING_
manager: "[[_PENDING_]]"
members: []
---

# _PENDING_

Copy this file to `14-people/<team-name>.md`, fill in the frontmatter,
then link each member back to this team via their own `team:` field so
Obsidian's Graph shows the relationship from both directions.
```

- [ ] **Step 4: Re-run the Task 1 Canvas link check — it must now pass fully**

Run:
```bash
python3 -c "
import json, pathlib
root = pathlib.Path('.')
for p in sorted(root.glob('maps/**/*.canvas')):
    data = json.loads(p.read_text())
    for n in data.get('nodes', []):
        if n.get('type') == 'file':
            target = root / n['file']
            assert target.exists(), f'{p}: missing {n[\"file\"]}'
    print(f'OK {p}')
"
```
Expected: `OK` printed for all six `.canvas` files, no `AssertionError`.

- [ ] **Step 5: Commit**

```bash
git add 14-people/
git commit -m "Add optional 14-people/ module: Person/Team navigation entities"
```

---

### Task 3: Wire config, init profiles, and validator

**Files:**
- Modify: `brain.config.json`
- Modify: `scripts/init_brain.py:38-52`
- Modify: `scripts/validate_structure.py:2-14` (docstring), `:30-55` (`MODULE_REQUIRED`), add `check_canvas_files()` after `check_version_drift()`, and its call site in `main()`
- Modify: `Makefile` (new `new-view` target, `validate` help text)
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `maps/README.md`, `maps/home.canvas`, `maps/_templates/blank.canvas` (Task 1); `14-people/README.md`, `14-people/_templates/person.md`, `14-people/_templates/team.md` (Task 2).
- Produces: `brain.config.json.modules["maps"] = true`, `modules["14-people"] = false` as shipped defaults; `_BASELINE` and `_PROFILE_DIFFS` in `init_brain.py` carrying the two new keys for every profile; `check_canvas_files() -> list[str]` in `validate_structure.py`, called from `main()`.

- [ ] **Step 1: Add the two new module flags to `brain.config.json`**

In `brain.config.json`, inside `"modules"`, add two keys (after `"12-capabilities": false`):

```json
    "12-capabilities": false,
    "maps": true,
    "14-people": false
```

- [ ] **Step 2: Extend `_BASELINE` and `_PROFILE_DIFFS` in `scripts/init_brain.py`**

Replace lines 38-50:

```python
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
    "full": None,  # empty overrides: leave brain.config.json's existing values as-is
}
```

Also update the module docstring at the top of the file (lines 7-16) to
mention the two new modules by adding one line after the `full` line:

```python
"""...
  full                  everything on (default)

`maps` (Obsidian Canvas views) defaults on for every profile; `14-people`
(Person/Team navigation entities) defaults on only for `team`,
`engineering-management`, and `consulting-company`. Both ship their files
statically — this script only flips the config flag, same as
`12-capabilities`.
...
"""
```

- [ ] **Step 3: Add Canvas validation to `scripts/validate_structure.py`**

Update the module docstring (lines 4-13) — add one line to the structural
checks list:

```python
"""...
  structural (exit 1 on failure):
    - required files exist for every ACTIVE module
    - relative markdown links resolve
    - duplicate IDs within a namespace (DEC-001 defined twice, etc.)
    - Canvas files under maps/ are valid JSON and every file-node path
      resolves (layout, color, and node content are never checked — a
      Canvas belongs to whoever edits it)
  reported as debt (never fail the build):
...
"""
```

Add to `MODULE_REQUIRED` (after the `"12-capabilities"` entry, line 54):

```python
    "12-capabilities": ["12-capabilities/README.md", "12-capabilities/capability-register.md"],
    "maps": ["maps/README.md", "maps/home.canvas", "maps/_templates/blank.canvas"],
    "14-people": ["14-people/README.md", "14-people/_templates/person.md",
                  "14-people/_templates/team.md"],
```

Add a new function after `check_version_drift()` (i.e. after line 92,
before `def main()`):

```python
def check_canvas_files() -> list[str]:
    """Canvas is a view, not a source of truth: validate that it opens and
    every file-node link resolves. Never validate layout, color, group
    contents, or 'which entities should appear' — that's user-owned."""
    errs: list[str] = []
    maps_dir = ROOT / "maps"
    if not maps_dir.is_dir():
        return errs
    for canvas in sorted(maps_dir.rglob("*.canvas")):
        rel = canvas.relative_to(ROOT)
        try:
            data = json.loads(canvas.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{rel}: invalid JSON ({e})")
            continue
        for node in data.get("nodes", []):
            if node.get("type") != "file":
                continue
            target = node.get("file", "")
            # Canvas file paths are vault-relative to the repo root —
            # unlike markdown links, which resolve relative to the
            # linking file's own directory.
            if target and not (ROOT / target).exists():
                errs.append(f"{rel}: node {node.get('id', '?')} "
                            f"references missing file -> {target}")
    return errs
```

Wire it into `main()` — after the `errors += check_version_drift()` line
(line 104), add:

```python
    if modules.get("maps", False):
        errors += check_canvas_files()
```

- [ ] **Step 4: Add `make new-view` to the `Makefile`**

Add `new-view` to the `.PHONY` line (line 3):

```makefile
.PHONY: help init validate index workspace stats sync-skills opencode opencode-doctor new-view
```

Update the `validate` help comment (line 16) to mention Canvas:

```makefile
validate:  ## Structure (per config), links, duplicate IDs, Canvas link resolution, unsourced decisions, status debt, index staleness
```

Add a new target after `sync-skills` (after line 33):

```makefile
new-view:  ## Create a new empty Canvas view: make new-view NAME=my-view
	@test -n "$(NAME)" || (echo "Usage: make new-view NAME=my-view" && exit 1)
	@if [ -f "maps/$(NAME).canvas" ]; then echo "maps/$(NAME).canvas already exists — pick another name or edit it directly"; exit 1; fi
	@mkdir -p maps
	@cp maps/_templates/blank.canvas "maps/$(NAME).canvas"
	@echo "Created maps/$(NAME).canvas — open it in Obsidian and start editing."
```

- [ ] **Step 5: Add the personal-view gitignore convention**

Add to `.gitignore`, after the `.obsidian/` line:

```
maps/*.local.canvas
```

- [ ] **Step 6: Run `make validate` — must pass**

Run: `make validate`
Expected: exits 0, ends with `Structure OK.`, and prints no `ERRORS:`
block. (This repo's own `brain.config.json` now has `modules.maps: true`,
so the new Canvas check runs against the real `maps/` folder created in
Task 1/2 and must find every file-node link resolvable.)

- [ ] **Step 7: Exercise `make new-view`, confirm refuse-to-overwrite**

Run:
```bash
make new-view NAME=scratch-test
test -f maps/scratch-test.canvas && echo "created: OK"
make new-view NAME=scratch-test
```
Expected: first run prints `Created maps/scratch-test.canvas...` and
`created: OK`; second run exits non-zero and prints `maps/scratch-test.canvas
already exists — pick another name or edit it directly` without touching
the file (confirm with `git status --porcelain maps/scratch-test.canvas`
showing no changes between the two runs). Then remove the scratch file:
`rm maps/scratch-test.canvas` (it was never committed).

- [ ] **Step 8: Commit**

```bash
git add brain.config.json scripts/init_brain.py scripts/validate_structure.py Makefile .gitignore
git commit -m "Wire maps/ and 14-people/ modules into config, profiles, and validator"
```

---

### Task 4: Documentation — AGENTS.md, START_HERE.md, README.md, docs/obsidian.md, CHANGELOG.md

**Files:**
- Modify: `AGENTS.md`
- Modify: `START_HERE.md`
- Modify: `README.md`
- Create: `docs/obsidian.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: nothing new from earlier tasks beyond the module/flag names already established (`maps`, `14-people`, `make new-view`).
- Produces: nothing consumed by later tasks — this is documentation only.

- [ ] **Step 1: Add the "Views" architectural rule to `AGENTS.md`**

Insert a new section immediately after the `## Rules` section (i.e.,
right before `## What to read per task`):

```markdown
## Views (`maps/`) are not knowledge

`maps/` is an optional presentation layer (Obsidian Canvas) over this
same Markdown. It exists for humans who navigate by clicking instead of
by path. The rules are architectural, not stylistic:

1. Canvas/`maps/` are views, not knowledge — they never carry a fact
   that isn't already in a canonical Markdown document.
2. Never derive an authoritative fact exclusively from a Canvas file.
3. Never put canonical information only in Canvas — if it matters, it
   has a Markdown home first.
4. Never silently regenerate a user-edited Canvas file. Canvas becomes
   user-owned the moment it's created; automation only creates one at
   template checkout or via `make new-view`, never as a side effect of
   `make validate` or `make index`.
5. Canvas may reference canonical files freely (file nodes pointing at
   any Markdown in the repo) — that's its entire job.
6. An agent that never opens `maps/` still has complete access to every
   fact in the brain — Canvas is additive, never a required read path.

See `maps/README.md` and `docs/obsidian.md` for the human-facing side of
this.
```

- [ ] **Step 2: Add the human/agent split to `START_HERE.md`**

Insert a new section right after the intro paragraph (after line 6, the
"Load only the sections the active task needs." line) and before `## By
task`:

```markdown
## Human / visual vs. agent / developer

- **Human / visual:** open this repo as an Obsidian vault, then
  [`maps/home.canvas`](maps/home.canvas) — a clickable launcher into the
  same Markdown below. See [`docs/obsidian.md`](docs/obsidian.md).
- **Agent / developer:** keep reading — [`AGENTS.md`](AGENTS.md) and this
  file's task table are the entry point either way.
```

- [ ] **Step 3: Update `README.md` — header version, positioning paragraph, module table, commands table**

Bump the header (line 1):
```markdown
# Company Brain Template — v2.2
```

Insert a new paragraph after the "Three files, three purposes" list
(after line 18, before `## The core idea: an evidence → knowledge
pipeline`):

```markdown
Company Brain provides one shared knowledge layer with multiple
interfaces: [Obsidian](docs/obsidian.md) (Canvas, Graph, backlinks) for
visual/human navigation, Git + Markdown for portability and diffing, and
Claude Code / Codex / OpenCode for agentic work. All three read and
write the same Markdown — nothing important ever lives only in one of
them.
```

Add two rows to the module table (after the `12-capabilities/` row,
before `99-inbox/`):

```markdown
| `maps/` | | optional — Obsidian Canvas views (`home.canvas` launcher + starter maps) over the same Markdown; on by default for every profile, never a source of truth |
| `14-people/` | | optional — minimal Person/Team entities for navigation, not an HRIS; off by default, on for `team`, `engineering-management`, `consulting-company`; strict privacy boundary in `14-people/README.md` |
```

Add a row to the Commands table (after the `make sync-skills` row):

```markdown
| `make new-view NAME=<slug>` | Create a new empty Canvas view at `maps/<slug>.canvas` (refuses to overwrite an existing one) |
```

- [ ] **Step 4: Create `docs/obsidian.md`**

```markdown
# Using this brain in Obsidian

This brain works with no `.obsidian/` folder at all — nothing here
requires Obsidian. If you'd rather browse visually than by path, this
page is the on-ramp.

## Open as a vault

In Obsidian: **Open folder as vault** → pick this repo's root. No plugin
installation is required for anything described below.

## Start at the launcher

Open `maps/home.canvas`. It's a grid of cards, each a real file in this
repo — click one to open the section's hub document. Nothing on this
canvas is "extra" content; it's the same Markdown you'd find browsing
folders, just one click closer.

## Starter views

`maps/` ships a few more starter Canvas files (`brain-overview`,
`portfolio`, `management`, `architecture-capabilities`) — see
`maps/README.md` for what each is for and which profile it suits best.
None of them are mandatory; delete what you don't want, keep what you
do.

## Graph and Backlinks

Obsidian's built-in **Graph view** and the **Backlinks** panel on any
open file work immediately, because the knowledge here is already
wikilinked Markdown with frontmatter — `[[Some Document]]`-style links
and `type:` fields in `05-requirements/`, `06-decisions/`, `14-people/`,
etc. The more a document links out (rather than just being linked *to*),
the more useful the graph gets.

## Properties

Frontmatter fields (`type`, `stage`, `tier`, `owner`, `updated`, and for
`14-people/`: `role`, `team`, `assignments`) show up in Obsidian's
**Properties** panel automatically — no configuration needed.

## Customizing Canvas — please do

**Feel free to duplicate, rearrange, simplify, or create new Canvas
views.** A Canvas belongs to whoever's editing it. Two conventions:

- Shared, team-useful views: normal `maps/*.canvas`, committed to git.
- Personal views: name them `maps/*.local.canvas` — gitignored, so they
  never need review or a commit.

Create a fresh one with `make new-view NAME=<slug>`.

## The source-of-truth rule

If you ever wonder "is this true because the Canvas says so, or because
a Markdown document says so" — the answer is always the Markdown
document. Canvas is how you got there, not why it's true. See `AGENTS.md`
for the full rule set.
```

- [ ] **Step 5: Add the `[2.2.0]` entry to `CHANGELOG.md`**

Insert a new section at the top, immediately after the `## [2.1.0]`
header's parent line (i.e. before `## [2.1.0]`, after the intro
paragraph on line 4):

```markdown
## [2.2.0]

### Added
- Optional visual views layer `maps/` (Obsidian Canvas): `home.canvas`
  launcher plus four starter views (`brain-overview`, `portfolio`,
  `management`, `architecture-capabilities`), `maps/README.md`, and
  `maps/_templates/blank.canvas` for `make new-view NAME=<slug>`. Canvas
  files are shipped statically and never regenerated — `make
  validate`/`make index` never write to `maps/`, and `make init`'s
  placeholder replacement skips `.canvas` files by construction (not in
  `TEXT_EXT`). `validate_structure.py` checks Canvas JSON validity and
  that every file-node path resolves — never layout, color, or "which
  entities should appear." `maps/*.local.canvas` is gitignored for
  personal, unshared views.
- Optional `14-people/` module: minimal `person`/`team` frontmatter
  templates for navigation and org context — explicitly not an HRIS.
  `14-people/README.md` states the allowed field list (role, team,
  project, assignment) and the disallowed one (compensation, health,
  disciplinary records, private feedback) as a hard boundary.
- New profile-derived module flags: `maps` on by default for every
  profile, `14-people` on for `team`, `engineering-management`,
  `consulting-company`.
- `docs/obsidian.md` and a short human/agent split in `START_HERE.md`
  and `README.md` — same knowledge, two navigation interfaces (Obsidian
  vs. Git and agents).
```

- [ ] **Step 6: Run `make validate` — version drift check must pass**

Run: `make validate`
Expected: exits 0, `Structure OK.`, no version-drift error (README now
says `v2.2`, CHANGELOG's latest entry is `[2.2.0]`).

- [ ] **Step 7: Commit**

```bash
git add AGENTS.md START_HERE.md README.md docs/obsidian.md CHANGELOG.md
git commit -m "Document the maps/ views layer and 14-people module"
```

---

### Task 5: End-to-end verification across two profiles

**Files:** none modified — this task only runs commands against scratch
clones and reports/fixes anything broken.

**Interfaces:**
- Consumes: the complete feature from Tasks 1-4.

- [ ] **Step 1: Init a management-oriented profile in a scratch clone**

```bash
rm -rf /tmp/brain-mgmt && cp -R . /tmp/brain-mgmt && cd /tmp/brain-mgmt
python3 scripts/init_brain.py --org "Acme Mgmt" --profile engineering-management
cd -
```
Expected: output lists `Organization: Acme Mgmt  ·  Profile:
engineering-management`; `brain.config.json` in `/tmp/brain-mgmt` now has
`"maps": true` and `"14-people": true`.

- [ ] **Step 2: Init a technical profile in a second scratch clone**

```bash
rm -rf /tmp/brain-dev && cp -R . /tmp/brain-dev && cd /tmp/brain-dev
python3 scripts/init_brain.py --org "Acme Dev" --profile development
cd -
```
Expected: `brain.config.json` in `/tmp/brain-dev` has `"maps": true` and
`"14-people": false`.

- [ ] **Step 3: Validate both scratch brains**

```bash
(cd /tmp/brain-mgmt && python3 scripts/build_indexes.py --check && python3 scripts/validate_structure.py)
(cd /tmp/brain-dev && python3 scripts/build_indexes.py --check && python3 scripts/validate_structure.py)
```
Expected: both end with `Structure OK.` and exit 0.

- [ ] **Step 4: Confirm `init` never touched `.canvas` files**

```bash
diff <(git -C . show HEAD:maps/home.canvas 2>/dev/null || cat maps/home.canvas) /tmp/brain-mgmt/maps/home.canvas
diff <(git -C . show HEAD:maps/home.canvas 2>/dev/null || cat maps/home.canvas) /tmp/brain-dev/maps/home.canvas
```
Expected: no output from either `diff` (byte-identical — `__ORG_NAME__`
never appears inside `home.canvas`, so placeholder replacement had
nothing to change there anyway, and the extension-based skip means it
was never even opened for writing).

- [ ] **Step 5: Hand-edit a Canvas, re-run init, confirm it survives**

```bash
cd /tmp/brain-mgmt
python3 -c "
import json, pathlib
p = pathlib.Path('maps/home.canvas')
data = json.loads(p.read_text())
data['nodes'][1]['x'] = 9999
p.write_text(json.dumps(data, indent=2))
"
cp maps/home.canvas /tmp/home-canvas-before.json
python3 scripts/init_brain.py --org "Acme Mgmt Renamed" --profile engineering-management
diff /tmp/home-canvas-before.json maps/home.canvas
cd -
```
Expected: the `diff` prints no output — the hand-edit (`x: 9999`)
survives the second `init` run untouched.

- [ ] **Step 6: Confirm `make validate`/`make index` don't touch `maps/`**

```bash
cd /tmp/brain-mgmt
sha256sum maps/*.canvas maps/_templates/*.canvas > /tmp/before.sha256
python3 scripts/build_indexes.py
python3 scripts/validate_structure.py
sha256sum maps/*.canvas maps/_templates/*.canvas > /tmp/after.sha256
diff /tmp/before.sha256 /tmp/after.sha256
cd -
```
Expected: no diff output — every Canvas file's hash is unchanged.

- [ ] **Step 7: Confirm a legacy brain (no `maps`/`14-people` keys) still validates cleanly**

```bash
cd /tmp/brain-dev
python3 -c "
import json, pathlib
p = pathlib.Path('brain.config.json')
cfg = json.loads(p.read_text())
del cfg['modules']['maps']
del cfg['modules']['14-people']
p.write_text(json.dumps(cfg, indent=2))
"
python3 scripts/validate_structure.py
cd -
```
Expected: `Structure OK.`, exit 0 — a `brain.config.json` predating this
feature (missing both keys) validates exactly as it did before, because
`modules.get("maps", False)` and `modules.get(mod, False)` both default
missing keys to inactive.

- [ ] **Step 8: Clean up scratch clones**

```bash
rm -rf /tmp/brain-mgmt /tmp/brain-dev /tmp/home-canvas-before.json /tmp/before.sha256 /tmp/after.sha256
```

- [ ] **Step 9: Final full validation of the template repo itself**

```bash
make validate
make index
git status --porcelain
```
Expected: `make validate` and `make index` both succeed; `git status
--porcelain` shows no unexpected changes (only whatever this task's own
edits produced, if any — expected: none, since Task 5 only touches
`/tmp` scratch clones).

- [ ] **Step 10: Commit (only if Step 9 surfaced a fix)**

If any step above required a code fix (it shouldn't, if Tasks 1-4 were
followed exactly), commit that fix now with a message describing what
the end-to-end pass caught. Otherwise, this task produces no commit —
its job was verification.
