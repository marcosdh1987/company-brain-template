# Visual Views Layer (`maps/`) — Design

Status: approved (chat), pending self-review pass below.
Author: Marcos Soto + Claude
Date: 2026-09-14

## Problem

Company Brain is agent-readable but not human-navigable without a terminal
and knowledge of the folder layout. Non-technical stakeholders (PMs,
managers, researchers) need a way to browse the same knowledge visually —
without turning Obsidian into a dependency of the brain itself.

## Principle

`Knowledge != Views`. Markdown + frontmatter + wikilinks remain the only
source of truth. Canvas/Obsidian views are optional, disposable, regenerable
navigation aids over that knowledge — never a second source of facts.

```
                 SAME KNOWLEDGE
                      |
          +-----------+-----------+
          |                       |
       Humans                   Agents
       Obsidian               Claude/Codex/OpenCode
     Canvas / Graph            Markdown/Git/CLI
          |                       |
          +-----------+-----------+
                      |
        Markdown + frontmatter
           SOURCE OF TRUTH
```

## Scope

In scope:
- New optional module `maps/` (Obsidian Canvas views + README).
- New optional module `14-people/` (Person/Team entities for navigation).
- Profile wiring for both modules.
- Canvas creation lifecycle that guarantees automation never overwrites a
  user-edited `.canvas` file.
- Lightweight Canvas validation (JSON validity + file-node link resolution
  only — no aesthetic checks).
- Docs: `docs/obsidian.md`, `AGENTS.md` view rules, `START_HERE.md` split,
  README positioning paragraph.

Out of scope (deliberately not built): Obsidian plugins, a Canvas
generator that derives layout from live content, a people/org database,
enforced `.obsidian/` config bundle beyond what's already gitignored.

## Components

### 1. `maps/` module

```
maps/
  README.md                       # what views exist, edit-freely notice, source-of-truth rule
  home.canvas                     # launcher: cards -> real hub files
  brain-overview.canvas           # starter (profile: full)
  portfolio.canvas                # starter (profile: consulting, consulting-company, delivery-oversight, client-engagement)
  management.canvas               # starter (profile: team, engineering-management, consulting-company)
  architecture-capabilities.canvas# starter (profile: development, engineering-management, consulting-company)
```

- Toggled via `brain.config.json.modules.maps` (boolean), default `false`.
- `home.canvas` + `README.md` are the only files always present once the
  module is on. The other four are starter views: copied in at `make init`
  time only if the resolved profile lists them.
- `home.canvas` is a launcher, not a map of everything: one card per major
  section (Context, Work, Decisions, People, Delivery, Capabilities,
  Architecture, Meetings, Inbox), each a real Obsidian **file node**
  pointing at that section's hub/README/overview — not a group containing
  an internal file node, and not a plain text card. Sections whose module
  is inactive are omitted from the generated `home.canvas`, not shown
  disabled.
- Starter Canvas templates live at `scripts/_templates/maps/*.canvas` —
  plain JSON, edited like any other template. `init_brain.py` renders
  `home.canvas` by filtering a fixed card list against active modules;
  the other four are copied byte-for-byte (no templating).

### 2. Canvas lifecycle — the "never silently overwrite" rule

Canvas becomes user-owned the moment it exists. Automation touches a
`.canvas` file only:
- at `make init` (first copy into a fresh brain), and only if the target
  path doesn't already exist — re-running `make init` skips existing
  Canvas files and logs `"maps/x.canvas already exists, skipped"`;
- via a new `make new-view NAME=<slug>` target, which copies
  `scripts/_templates/maps/_blank.canvas` to `maps/<slug>.canvas`, refusing
  if the target exists.

`make validate` and `make index` never write to `maps/`. This is enforced
by construction (neither script touches the `maps/` path) and stated
explicitly in `AGENTS.md`.

### 3. Shared vs personal views

Naming convention, not a folder split: `maps/*.local.canvas` is gitignored
(`.gitignore` gains one line: `maps/*.local.canvas`). Anyone can duplicate
`maps/home.canvas` to `maps/management-marcos.local.canvas` and iterate
without touching version control. Team-shared views are ordinary
`maps/*.canvas` files, committed like any other doc.

### 4. `14-people/` module

Numbered 14 (13 is reserved for `13-security` per `AGENTS.md`'s domain
module list). Toggled via `brain.config.json.modules["14-people"]`,
default `false`.

```
14-people/
  README.md               # purpose + explicit privacy boundaries
  _templates/person.md
  _templates/team.md
```

Frontmatter shapes (documented in the templates, not enforced by schema —
consistent with how `03-work` documents its frontmatter today):

```yaml
---
type: person
name: _PENDING_
role: _PENDING_
team: "[[_PENDING_]]"
assignments: []
projects: []
---
```
```yaml
---
type: team
name: _PENDING_
manager: "[[_PENDING_]]"
members: []
---
```

`README.md` states explicitly:
- Allowed: role, team, public/professional location, specialty, project,
  assignment, operational meetings, work relationships.
- Not allowed: compensation, health, disciplinary records, private
  performance feedback, confidential 1:1 content, unnecessary personal
  information.

No changes to `build_indexes.py` in this pass — People/Team entities are
consumed via wikilinks and the Obsidian graph, not a generated index
table. `management.canvas`'s file nodes point at `14-people/` entries
that exist; the Canvas link-check (below) only verifies referenced files
exist, it doesn't require every person to appear on the canvas.

### 5. Profile wiring (`scripts/init_brain.py`)

Extend `_PROFILE_DIFFS` so each profile also sets `maps` and
`14-people` module flags, and add a parallel `_PROFILE_VIEWS` mapping
(profile -> list of starter view basenames beyond `home`) consulted only
when `maps` is active for that profile:

| Profile | `maps` | `14-people` | Starter views beyond `home` |
|---|---|---|---|
| `full` | on | off | brain-overview |
| `consulting` | on | off | portfolio |
| `consulting-company` | on | on | management, portfolio, architecture-capabilities |
| `engineering-management` | on | on | management, architecture-capabilities |
| `development` | on | off | architecture-capabilities |
| `team` | on | on | management |
| `delivery-oversight` | on | off | portfolio |
| `client-engagement` | on | off | portfolio |

Brains that never re-run `make init` after this change keep
`maps`/`14-people` absent from their `brain.config.json.modules` map,
which `validate_structure.py` and `build_indexes.py` already treat as
"module inactive" (falsy default) — zero behavior change for existing
instances. This is the backwards-compatibility guarantee.

### 6. Validation (`scripts/validate_structure.py`)

New check, gated on `modules.maps` being true, added alongside the
existing per-module `MODULE_REQUIRED` check:

- `MODULE_REQUIRED["maps"] = ["README.md", "home.canvas"]` (existing
  mechanism, no new code needed for this part).
- New `check_canvas_files()`:
  1. For every `maps/*.canvas` (including `*.local.canvas`): must parse
     as JSON — error if not.
  2. For every file-type node (`node.type == "file"`), resolve
     `node.file` relative to repo root — error if the target doesn't
     exist.
  3. No checks on position, color, size, group nodes' contents, or "which
     entities should appear" — Canvas layout is entirely user-owned.

Severity: structural (contributes to exit code 1), matching how broken
markdown links are already treated — a dangling Canvas reference is the
same class of bug as a dangling `[text](path)` link.

### 7. Docs and positioning

- `AGENTS.md`: new section "Views (`maps/`) are not knowledge" stating
  the 6 rules verbatim (views≠source of truth, never derive facts only
  from Canvas, never put canonical info only in Canvas, never silently
  regenerate a user-edited Canvas, Canvas may reference canonical files
  freely, agents that ignore `maps/` still have full access via
  Markdown).
- `START_HERE.md`: short two-line split under the existing "first 60
  seconds" section — "Human/visual: open `maps/home.canvas` in Obsidian"
  vs "Agent/developer: read `AGENTS.md`" — no duplicated routing table.
- `README.md`: one short paragraph reframing the pitch as "one shared
  knowledge layer, multiple interfaces" (Obsidian / Git+Markdown /
  agents), added near the top positioning section, not replacing it.
- New `docs/obsidian.md`: open-as-vault, `home.canvas`, starter views,
  Graph/Backlinks/Properties basics, customizing Canvas freely,
  shared vs `*.local.canvas`, and the source-of-truth rule. Short —
  not an Obsidian manual.
- `maps/README.md`: what each starter view is for, which are automatic
  vs personal, explicit "feel free to duplicate/rearrange/simplify or
  create new Canvas views" language, source-of-truth reminder.

## Data flow / how a human uses it

```
Obsidian opens repo as Vault
  -> maps/home.canvas
     -> card "Team" (file node -> 02-organization/hubs/... or 14-people/README.md)
        -> click person file node -> 14-people/jane.md
           -> wikilink to project -> 03-work/<unit>/overview.md
              -> wikilink to decision -> 06-decisions/decision-log.md#DEC-014
Backlinks panel on any file shows every other note (including Canvas
cards, since Canvas file nodes are real vault references) pointing at it.
```

## Testing plan

- `make validate` and `make index` before/after change, on the template
  repo itself (module off) — must be unaffected.
- `make init ORG="Acme" PROFILE=engineering-management` and
  `make init ORG="Beta" PROFILE=development` (separate scratch clones) —
  confirm `maps/` + expected starter views + (for `engineering-management`)
  `14-people/` are created; confirm `make validate`/`make index` pass on
  both.
- Parse all generated `.canvas` files as JSON; confirm every file-node
  path resolves.
- Hand-edit a generated `home.canvas` (change a node's position), re-run
  `make init` with `--force`-equivalent flag if any, or the same command
  again, confirm the file is untouched (skip-logged).
- Confirm `make validate`/`make index` do not modify any `.canvas` file
  (hash before/after).
- Confirm a brain with `maps` module off (default / all pre-existing
  brains) behaves identically to before this change.
- Confirm brain works with no `.obsidian/` directory present at all
  (already true, but re-confirm nothing in this change assumes it
  exists).

## Backwards compatibility

- Two new module keys default to absent/false; `validate_structure.py`
  and `build_indexes.py` already treat missing module keys as inactive.
- No existing profile's resolved module set changes unless
  `_PROFILE_DIFFS`/`_PROFILE_VIEWS` are read for `maps`/`14-people`,
  which only happens when those keys are present — additive change to
  `init_brain.py`, not a rewrite of existing profile behavior.
- No changes to `03-work`, decisions, requirements, or any existing
  module's required files, frontmatter, or validation rules.

## Version

Minor bump: `2.1.0` -> `2.2.0`. New optional modules and templates, no
breaking changes to folder structure or existing consumer adapters.
