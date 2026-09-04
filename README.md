# Company Brain Template — v2.0

Template for instantiating a **company brain**: the persistent, agent-readable
knowledge base for an engagement with one organization — its context,
decisions, requirements, conventions, systems, vendors, and evidence. It is
the **context** layer that complements the **execution** layer (the
engineering harness, [`ml-python-base`](https://github.com/marcosdh1987/ml-python-base)).

This structure is not theoretical: it consolidates what two real client brains
converged on independently, plus the traceability patterns they developed
(status vocabulary, source registers, promotion pipeline).

Three files, three purposes — read them in this order:

- **[`START_HERE.md`](START_HERE.md)** — context router: where to look first
  for a given task.
- **[`AGENTS.md`](AGENTS.md)** — the operating rules.
- **`README.md`** (this file) — what the template is and how it fits together.

## The core idea: an evidence → knowledge pipeline

```text
raw material           promotion               canonical knowledge
99-inbox/          →   analyze, extract,   →   06-decisions/  05-requirements/
01-meetings/           validate, cite          00-context/    03-work/ …
09-references/
```

Raw material is **evidence, not facts**. Everything promoted into canonical
documents carries a status (`CONFIRMED` / `PENDING VALIDATION` / `INFERRED` /
`SUPERSEDED` / `BLOCKED`) and a source. The full rules live in
[`AGENTS.md`](AGENTS.md) — the single source of operating instructions.

## When to use it (and when not to)

**Not on day one of a single-repo project.** There, the project brain lives
inside the code repo (`memory/`, `docs/adr/`). This template earns its place
when the engagement spans **more than one repo, more than one work unit, or a
consulting relationship** where evidence and decisions must outlive any single
codebase. Full progression: the harness guide's "Adopting the Harness in an
Existing Project".

## Quick start

```bash
# 1. Instantiate (choose an engagement profile)
make init ORG="Acme Inc." PROFILE=consulting
#    profiles: consulting | delivery-oversight | development | full |
#              team | engineering-management | consulting-company |
#              client-engagement

# 2. Populate with the bootstrap skill (from your AI assistant)
#    → .github/skills/bootstrap_company_brain.md
#    Mine sources first, interview second, invent nothing.
#    Taking over an org with history? The skill has a migration mode:
#    everything into 99-inbox → source register → gradual promotion.

# 3. Validate
make validate

# 4. If the org has code repos: register them and clone the workspace
#    → 04-architecture/repos.yaml, then: make workspace
```

## Structure (modules)

Modules are activated per engagement in `brain.config.json`; the validator
only enforces active ones. Core modules are always on. Numbered folders
beyond the core set (`10-management/`, `11-ml-governance/`, `12-capabilities/`,
`13-security/`, …) are **domain modules**: optional, never assumed, declared
one place — `brain.config.json`.

| Module | Core | Contents |
|---|---|---|
| `00-context/` | ✔ | company overview, engagement scope, stakeholders, glossary |
| `01-meetings/` | ✔ | transcripts (evidence) + minutes (reviewed) + intake template |
| `02-organization/` | | ways of working, conventions (engineering, git, ticketing, communication), AI policy, ownership, org-level runbooks, role hubs |
| `03-work/` | | one folder per work unit, tiered T0/T1/T2 by rigor (`_templates/` shows each shape) |
| `04-architecture/` | | systems map, `repos.yaml` (code repo registry), integrations |
| `05-requirements/` | | functional, non-functional, business rules, open questions |
| `06-decisions/` | ✔ | `decision-log.md` — immutable `DEC-XXX` register |
| `07-delivery/` | | status, roadmap, action items, validation matrix, periodic check |
| `08-vendors/` | | vendor register + evaluations |
| `09-references/` | ✔ | primary sources (contracts, vendor docs) + **source registers** |
| `12-capabilities/` | | optional — capability register (`researched → piloted → proven`), on by default for `consulting-company` |
| `99-inbox/` | ✔ | landing zone for unprocessed material |
| `memory/` | ✔ | org-level learnings and patterns (quarterly review reports land here) |

## Working with code repos: the workspace model

The brain never contains code and code repos are **never submodules** of the
brain. The layout is hub-and-spoke with sibling clones:

```text
~/work/acme/
├── acme-brain/          ← this repo (the hub)
├── api-payments/        ← code repo, its CLAUDE.md imports ../acme-brain/…
└── web-portal/          ← code repo, same
```

Day 1 for a developer: clone the brain, run `make workspace` — it reads
`04-architecture/repos.yaml` and clones every registered repo alongside.
Full rationale, CI variant, and degradation behavior: [`docs/workspace.md`](docs/workspace.md).

## Commands

| Command | What it does |
|---|---|
| `make init ORG="…" [PROFILE=…]` | Instantiate for an organization with an engagement profile |
| `make validate` | Structure (per config), links, duplicate IDs, unsourced decisions, status debt, index staleness, README/CHANGELOG version match |
| `make index` | Regenerate `03-work/INDEX.md` (and other module indexes) from frontmatter |
| `make workspace` | Clone all code repos from `repos.yaml` as siblings of this repo |
| `make stats` | Content stats per active module |
| `make sync-skills` | Sync working skills from the harness + regenerate `.claude/` `.codex/` `.agents/` projections |

## Skills and multi-tool discovery

The brain ships its 6 lifecycle skills and **syncs working skills**
(brainstorming, planning, research, writing, retrospectives) from the
engineering harness — declared in `brain.config.json`, locked in
`skills-lock.json`. `make sync-skills` also regenerates native projections so
**Claude Code/app, Codex, and Antigravity** all discover every skill. Details:
[`docs/skills.md`](docs/skills.md).

## Principles

1. **Evidence ≠ knowledge.** Raw material lands in inbox/meetings/references;
   only cited, statused content becomes canonical.
2. **Stale context is worse than missing context** — the quarterly review
   (skill `quarterly_context_review`) exists to fight drift.
3. **Everything has a human owner** (`02-organization/ownership.md`).
4. **Decisions are immutable** — supersede, never edit.
5. **Nothing sensitive** — agents read this; reference secrets, never store them.
