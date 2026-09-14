# Changelog

Semver by tags (`vX.Y.Z`). `MINOR` = new sections/templates; `PATCH` = content
fixes; `MAJOR` = folder restructures that break consumer adapters.

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

## [2.1.0]

### Added
- OpenCode runtime: `make opencode` / `make opencode-doctor`, `opencode.json`
  (providers `gateway` / `nvidia` / `ollama` / `lmstudio`, all env-driven),
  `.env.example`, the `OPENCODE.md` adapter with a generated skill block,
  `LOCAL_AGENT.md` for small self-hosted models, and the
  `.opencode/plugin/validate-gate.ts` plugin that runs `make validate` when a
  session goes idle. The `.env` variable contract matches `ml-python-base`, and
  `make opencode` falls back to the harness `.env`, so one file serves both
  repos. `OPENCODE.md` + `opencode.json` are now required by `make validate`.
- Internal skills can be folders: `.github/skills/<name>/SKILL.md` with the
  scripts, templates or references the skill runs beside it — the flat
  `<name>.md` shape still works. Executable bits survive the projection. A
  folder without `SKILL.md` is reported and skipped, never silently ignored.
- Fourth native projection `.opencode/skills/`, so OpenCode discovers every
  skill alongside Claude Code, Codex and Antigravity. `make sync-skills` also
  rewrites the skill list between the `GENERATED SKILLS` sentinels in
  `OPENCODE.md`.

## [2.0.0]

### Changed (BREAKING)
- Renamed `03-projects/` → `03-work/`. Folders are now **work units**
  (`type: client | opportunity | internal-product | initiative`, `stage:
  exploring | active | paused | closed`) instead of an assumed one-shape
  "project". Existing brains on v1.x must rename the folder and add
  frontmatter to each unit's `overview.md` — see `03-work/README.md`.
- Replaced `_project-template/` with tiered templates `_templates/t0/` (light,
  exploratory), `t1/` (medium), `t2/` (full rigor, the old shape) —
  "graduated rigor": traceability now matches the tier, not a single fixed
  bar for every work unit.
- All cross-references to `03-projects` (AGENTS.md, README.md, skills,
  validator, docs) updated to `03-work`.

### Added
- `START_HERE.md` — a context router distinct from `AGENTS.md` (rules) and
  `README.md` (explanation).
- `scripts/build_indexes.py` + `make index` — generates `03-work/INDEX.md`,
  `06-decisions/INDEX.md`, `05-requirements/INDEX.md` from frontmatter/IDs.
  `make validate` now fails if a committed index is stale.
- `make validate` now also fails on README/CHANGELOG version drift.
- Optional `12-capabilities/` module: capability register with maturity
  states `researched → piloted → proven`.
- Profiles: `consulting-company` (enables `12-capabilities` by default),
  `team`, `engineering-management`, `client-engagement`.
- Documented the "role hub" pattern (`02-organization/hubs/<role>-hub.md`) —
  a task-oriented context router composed over canonical docs, never a new
  source of truth.
- `memory/` is now declared as a core module in `brain.config.json` (fixing
  drift with the README, which already listed it as core).

## [1.1.0]

### Added
- Harness skill sync: `brain.config.json` `harness` section + `make
  sync-skills` — pulls non-code working skills from `ml-python-base` into
  `.github/skills-external/` (lockfile `skills-lock.json`) and regenerates
  native tool projections (`.claude/skills/`, `.codex/skills/`,
  `.agents/skills/` + Antigravity rules pointer) so Claude Code, Codex and
  Antigravity discover internal + external skills. `docs/skills.md`.

## [1.0.0]

### Changed (BREAKING)
- Replaced the `brain/` tree with the numbered pipeline structure
  (`00-context` … `99-inbox`), consolidated from two production client brains.
- `AGENTS.md` is now the single source of operating rules; `CLAUDE.md` is a
  pointer. Status vocabulary formalized: CONFIRMED / PENDING VALIDATION /
  INFERRED / SUPERSEDED / BLOCKED.
- Tooling is config-driven (`brain.config.json`): modular validation with
  semantic checks (duplicate IDs, unsourced decisions, status debt), init
  with engagement profiles, `make workspace` for hub-and-spoke repo cloning.

### Added
- `02-organization/` (ways of working, conventions incl. ticketing, AI
  policy, ownership, runbooks), `04-architecture/repos.yaml`, source-register
  template with conflict tracking, meeting minutes template, validation
  matrix, periodic validation check, decision log (`DEC-XXX`), skills
  `process_meeting` and bootstrap v2 with migration mode, `docs/workspace.md`.

## [0.1.0]
- Initial template (`brain/` structure).
