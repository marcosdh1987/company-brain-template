# Changelog

Semver by tags (`vX.Y.Z`). `MINOR` = new sections/templates; `PATCH` = content
fixes; `MAJOR` = folder restructures that break consumer adapters.

## [2.3.0]

Mechanisms backported from a live instance after ~34 commits of real operation.
Every entry below answers a failure that instance actually hit; the reason is
stated so the next reader does not have to rediscover it. Design notes and the
full deferred list: `docs/superpowers/specs/2026-09-15-instance-backport-design.md`.

### Added
- `docs/privacy-boundaries.md` — the single place the restricted categories and
  the person-page field allowlist are written down. Previously the boundary
  lived inside the README of an off-by-default module and was restated in seven
  other files, so no file was authoritative. It lives in `docs/` rather than in
  `02-organization/` for a concrete reason: `docs/` is not a module, so no
  profile can turn it off, and ten files link to it. A boundary that disappears
  when someone deselects a module is not a boundary. Includes the
  corporate-system redirect table, whose `PENDING VALIDATION — system name
  intentionally not assumed` is the mechanism, not a gap: "we do not know which
  system owns this" is a recorded state, while a guessed vendor name is an
  invented fact someone will later act on.
- `02-organization/automation-map.md` — one zone per class of automated update,
  with a uniform contract whose load-bearing row is **Forbidden**. An agent that
  may write anywhere will eventually write the right fact into the wrong file.
- Bitácora layer for recurring meetings: `01-meetings/minutes/series-bitacora-template.md`
  and `one-on-one-bitacora-template.md`, plus the two-kinds-of-folder model in
  `01-meetings/README.md` and the workflow exemption in `AGENTS.md`. The
  template previously had no recurring-meeting concept at all: every session
  became a dated file, so nothing carried over between them.
- `Home.md` — a reader's door that renders in Obsidian, on the code host, and in
  any editor. `docs/obsidian.md` was sending non-technical readers to a Canvas
  file, which renders nowhere else.
- `.github/skills/query_system_of_record.md` — a read-only bridge to an external
  system of record, fully parameterised (`_PENDING_` host, endpoints and scope).
  Its three preconditions are the generalizable part: liveness is not readiness,
  reachability is not permission, writes are out of scope by construction.
- Portable Obsidian defaults: `.obsidian/app.json`, `core-plugins.json`,
  `graph.json` and `snippets/brain-navigation.css` now ship, while
  `workspace.json` and `appearance.json` stay ignored. A fresh clone previously
  got no vault configuration at all, despite `docs/obsidian.md` telling the
  reader to open the repo as a vault.
- `.engobs.toml.example` + `docs/telemetry.md` — telemetry documented as opt-in,
  with **no endpoint shipped**. A template that phones home by default sends one
  organization's usage data to whoever set it up.
- `scripts/_brain.py` — the contracts both the validator and the index builder
  read, so each has exactly one definition. Two scripts that hardcode the same
  convention drift, and the first thing that drifts is the one nobody re-reads.
- `make validate` now also checks work-unit frontmatter, Canvas text-card links,
  and index freshness, and reports work-unit and possible-secret debt.
- `work_unit_page` and `fail_on_secrets` as **code defaults**, not shipped
  config keys. An instance may add either to `brain.config.json` to opt out.
  They stay out of the shipped file on purpose: that file is the one an instance
  owns and edits, so every key the template adds to it becomes a merge conflict
  in every fork, forever.
- `docs/upgrading.md` — how an instance takes a new release: fork with shared
  history, `git merge upstream/main`, re-run `make init`, and the table of what
  the template owns versus what the instance owns. Verified by simulation: a
  customized fork took this entire release with one trivial conflict, and its
  own content, profile and conventions survived intact.
- `org-layer` profile (see below).
- `make init` prunes `Home.md`'s entries for modules the chosen profile turned
  off, and says so. Home's rows are real Markdown links, so a link into a folder
  the owner may delete would be a hard `make validate` error — this keeps an
  instance green whether or not they delete the folders.
- `make init` also substitutes `{{COMPANY_NAME}}` alongside `__ORG_NAME__`, so
  content authored against either convention is filled in.
- `make init` no longer substitutes into `CHANGELOG.md`: it is the template's
  own release history, and injecting an organization name into it made every
  future upstream edit to the file a merge conflict for every instance.
- `org-layer` profile — the shared organization brain: company context,
  conventions, policy and org-wide decisions, with no work units, no delivery
  and no architecture. It exists so a team's brain can *reference* the org layer
  as a source of record rather than copy it; N copies of the company context
  drift within a week. This is also the first profile that turns `03-work` off,
  which is what surfaced the `Home.md` table-cell case above.

### Changed
- **Rigor now follows a work unit's `type`, not its `tier`** ([DEC-002](06-decisions/decision-log.md)).
  Tier was answering two independent questions at once — how many documents a
  unit holds, and how much traceability each claim owes — and both failure modes
  showed up in practice: a one-page client opportunity had to grow empty files
  to earn the right to cite a source, while a large internal initiative sat
  permanently in debt for claims nobody would audit. Two floors bound the
  change, so nothing that mattered under rigor-by-tier stops mattering.
- `AGENTS.md` gained: the five-layer model and the systems-of-record rule (store
  links, summaries and a **verification date**, never a copy); the work-unit
  model, phrased so it does not name the unit-page filename; graduated rigor;
  the language rule; the link convention; the privacy rule; the bitácora
  exemption; automation zones; and nine routing rows. The source-of-truth list,
  the status vocabulary, the six Canvas rules and the nine original routing rows
  are unchanged, byte for byte.
- `OPENCODE.md` shrank: its runtime-rules block had grown into a second rule
  set, which `.github/brain-governance.md` forbids, and its language bullet
  would have contradicted the new language rule. It now points at `AGENTS.md`.
- `01-meetings/minutes/meeting-template.md` gained an optional "People
  mentioned" line, so a note surfaces in a person's backlinks.
- `make validate` is a single command. It previously ran the index check first,
  and because make aborts on the first failure, one stale index hid the entire
  debt report.
- `make sync-skills` now exits non-zero when it keeps a local skill because the
  upstream copy lost frontmatter keys. The instance's version exited 0 there, so
  its guard was invisible in CI — which defeats the purpose of having it. This
  is the release's only new failure mode; `--force` overrides.

### Fixed
- `make validate` no longer walks a nested git checkout. A `git worktree add`
  inside the repo — which this template's own skills encourage — put a second
  copy of every canonical file on disk, so every ID was reported as a duplicate
  and the build was red for a reason that had nothing to do with content.
- `make sync-skills` clears a projection through its `.generated-manifest.tsv`
  instead of `rmtree`. A projection directory belongs to a tool, not to the
  script: a loose config file or a hand-authored skill beside the generated ones
  was being deleted.
- Markdown and Canvas link targets are percent-decoded before resolving, so a
  correct link to a filename containing a space no longer reports as broken.

### Deferred (and why)
- **A canvas generator.** Blocked by a numbered rule in `AGENTS.md` and a
  guarantee published in 2.2.0, not by the code — a config flag does not unsay a
  changelog. Also the instance's most coupled script, and its output path would
  overwrite a hand-authored canvas this template ships.
- **The `home.canvas` launcher gate.** Impossible as written: it fails this
  template's own `home.canvas` on two rules simultaneously, and requires a file
  that was gitignored. Documented in `docs/obsidian.md` as an optional,
  deliberately unvalidated convention.
- **Domain modules** and an account entity model — out of scope; their portable
  rules were backported instead.
- **`.base` views** and three portfolio/review skills — each coupled to a
  contract or a module the template does not have.
- **A hand-maintained anchor index in the decision log** — the template already
  generates that table; a second one by hand is drift by construction.
- **The instance's "human-first document shape"** — it puts status in an
  appendix last, contradicting this template's header-table-first convention.
  Two rules about where status lives is worse than one imperfect rule; the
  tension is recorded in the design spec instead.

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
