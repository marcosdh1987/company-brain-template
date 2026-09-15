# AI Agent Operating Instructions

This repository is the **company brain** for __ORG_NAME__: the persistent,
agent-readable knowledge base for the engagement. It stores durable context,
not application code. This file is the single source of operating rules —
every tool adapter (`CLAUDE.md`, Copilot, etc.) defers to it. For "where do I
look first for this task", see [`START_HERE.md`](START_HERE.md); for "what
is this template", see [`README.md`](README.md); a human reader starts at
[`Home.md`](Home.md). The hard boundary on what may be recorded about a person
is [`docs/privacy-boundaries.md`](docs/privacy-boundaries.md).

## What this brain is — and is not

| Layer | Description | Examples |
|---|---|---|
| **Corporate official sources** | Authoritative systems of record. The brain references these; it does NOT replace them. | issue tracker, wiki, code host, HR system, incident tracker |
| **Evidence collected** | Raw material ingested: transcripts, docs, tickets, emails. | `99-inbox/`, `01-meetings/transcripts/` |
| **Validated knowledge** | Confirmed facts extracted from evidence and approved. | `00-context/`, `06-decisions/`, `05-requirements/` |
| **Notes and hypotheses** | Working context, INFERRED or PENDING VALIDATION. | `07-delivery/`, `memory/` |
| **Approved decisions** | Immutable decisions recorded with source and status. | `06-decisions/decision-log.md` |

When a corporate tool is the official record for something, this brain stores
**links, references, summaries and a verification date** — never a copy. A
summary without a verification date is undated debt, not knowledge.

## Source-of-truth priority

When documents disagree, higher wins. Raw material never outranks canonical
documents.

1. `06-decisions/` — recorded decisions
2. `05-requirements/` — validated requirements and business rules
3. `00-context/` — company context, scope, glossary
4. `02-organization/` — ways of working, conventions, AI policy, ownership
5. `03-work/` — per-work-unit canonical documents
6. `04-architecture/` — systems, repos, integrations
7. `07-delivery/` — status, roadmap, action items
8. `01-meetings/minutes/` — reviewed summaries
9. `01-meetings/transcripts/` — raw evidence
10. `99-inbox/` — unprocessed material

`maps/`, `Home.md` and `.obsidian/` are **views, not sources**. They rank below
every layer above. No rule, decision or fact may live only there; an agent that
ignores all three loses nothing.

## The work-unit model

Anything with an owner, a timeline, and a deliverable is a **work unit** and
lives in `03-work/<work-unit>/`, whatever its type and stage. Its entry
document is the **unit page** (`overview.md` in this template) and it opens with
YAML frontmatter, which is the machine-readable layer the indexes and the rigor
rules both read:

```yaml
---
type: client | internal-product | initiative | opportunity
stage: exploring | active | paused | closed
tier: 0 | 1 | 2
owner: <name>
updated: YYYY-MM-DD
---
```

`type` sets the rigor owed. `stage` records where the work stands. `tier` sets
how many documents the unit carries — see `03-work/README.md` for the shape of
each tier and the templates under `03-work/_templates/`.

`stage` records where the work stands. An opportunity becomes a project by
changing `stage`, **never** by moving the folder — nothing that links to it may
break because the work got approved.

A canonical document carries two surfaces and keeps both. The `| Field | Value |`
header table is what a reader reads and what a source register cites; the
frontmatter is what the tooling and an agent parse. **Keep the two
non-overlapping** — the table carries status, last review date and the source
register; the frontmatter carries `type`, `stage`, `tier`, `owner`, `updated`. A
field duplicated across both surfaces will drift, and there is no rule that says
which one wins.

Short notes about a submodule, component or service go in the unit's `notes/`
folder. Diagrams and images go in the unit's `assets/` folder.

### Graduated rigor

`tier` sets how many documents a work unit carries. `type` sets the rigor each
claim inside it owes. The two are independent: a one-page opportunity owes full
traceability, and a large internal initiative does not.

This table applies **inside `03-work/` only**. Everything else in the brain
keeps full rigor without exception.

| Type | Rigor owed |
|---|---|
| `client`, `opportunity` | Full: a status marker on every non-obvious claim, a citation into `09-references/`, an entry in a source register. A third party is involved and traceability is the deliverable. |
| `internal-product` | Status markers wherever a claim leaves the team — commitments, metrics, commercial positioning. |
| `initiative` | `owner` and `updated`. No status markers, no sources required. |
| `notes/` under any parent | `owner` and `updated`, even under a `client`. **In exchange, a note is never citable as canonical**: promote the finding into a canonical document, with its source, before anything depends on it. |

**Two floors that no type lowers.** Any claim that (a) feeds `06-decisions/`,
`05-requirements/` or a commercial document, or (b) leaves the organization,
carries full rigor regardless of `type` or `tier`. And a unit owner may pin a
higher bar in the unit page's header table; the table never lowers the bar, only
raises it.

Recorded as [DEC-002](06-decisions/decision-log.md).

## Information status vocabulary

Mark the status of every non-obvious statement as exactly one of:

- `CONFIRMED` — validated against a source or approved by the client.
- `PENDING VALIDATION` — plausible, awaiting confirmation. Never present as fact.
- `INFERRED` — deduced by the consultant/agent; the reasoning must be stated.
- `SUPERSEDED` — replaced by newer evidence; keep it, point to what replaced it.
- `BLOCKED` — must not be acted on; name the prerequisite that unblocks it.

Statuses live in header tables, inline in bullets (`- **CONFIRMED:** …`), or
per table row. A visible gap (`_PENDING_` placeholder with an owner) always
beats plausible invention.

## Rules

- Raw transcripts and inbox material are **evidence, not validated facts**.
- Never invent missing business or technical facts.
- If new information conflicts with existing knowledge, **flag the conflict
  explicitly — never silently overwrite**. Record it in the source register.
- Decisions are immutable: supersede with a new `DEC-XXX`, never edit.
- Preserve traceability: every decision, requirement, and confirmed fact cites
  its source (meeting, contract, email, repo, register ID).
- Separate **current state / target state / consultant recommendation /
  client-approved decision** — never blur these four.
- Prefer updating the authoritative document over creating a duplicate note.
- Work-unit-specific content stays in `03-work/<work-unit>/`; cross-work-unit
  content in the shared sections.
- Rigor follows the unit's `type`, not its `tier` — see "Graduated rigor" above.
  Never retrofit traceability onto a unit whose type never owed it; if the work
  became decision-grade or client-facing, its `type` changed, and that is what
  raises the bar.
- A tier **rises** by adding files, and the promotion is logged in the unit's
  change log. It never falls. Files from an abandoned tier stay where they are,
  marked `SUPERSEDED` — deleting them destroys the record of what was once
  believed.
- **Language.** This brain has one canonical language and may have more than one
  working language (`language` and, if set, `languages` in
  `brain.config.json`). The canonical language is mandatory for file and folder
  names, frontmatter keys **and values**, status markers, IDs, and the generated
  indexes. A working language is first-class for: (a) **verbatim evidence** —
  never translate a quote, transcript line or message when recording it; record
  it as said and add a short gloss in the canonical language beside it, because
  preserving the wording is the entire job of a source register; (b) working
  notes, agendas and `notes/`; (c) conversation — answer in the language the
  user wrote in. A canonical page in one language plus a reader-facing brief in
  another is two documents that will drift within a week: one page in the
  language of the person who maintains it beats two.
- **Links.** Wikilinks (`[[slug]]`) appear only in the frontmatter relation
  fields that the Obsidian graph reads. Everywhere else the standard is a
  relative Markdown link, because that is what `make validate` resolves and what
  renders outside Obsidian. The two exceptions are image embeds and prose inside
  `notes/`.
- Numbered folders beyond the core set (`10-management/`, `11-ml-governance/`,
  `12-capabilities/`, `13-security/`, `14-people/`, …) are **domain modules**:
  optional, never assumed active, declared in `brain.config.json`. `maps/` is
  an unnumbered presentation-layer module governed the same way (declared in
  `brain.config.json`, never assumed active).
- A **role hub** (`02-organization/hubs/<role>-hub.md`) is a task-oriented
  context router composed over canonical documents — it is never a new
  source of truth. It points; it does not restate.
- Never store credentials, passwords, API keys, MFA seeds, private keys, or
  unnecessary personal data. Reference secret locations, never values.
- **Privacy.** Never store individual performance ratings, compensation, medical
  information, disciplinary records, candidate records, or confidential
  one-on-one content. An agent asked to store any of it refuses, records only an
  approved system reference, and asks the human owner to handle it in the
  corporate system. The categories and the person-page field allowlist are
  defined once, in
  [`docs/privacy-boundaries.md`](docs/privacy-boundaries.md).
- Keep documents concise and actionable.

## Views (`maps/`) are not knowledge

`maps/` is an optional presentation layer (Obsidian Canvas) over this
same Markdown, and `Home.md` is its plain-Markdown equivalent. They exist for
humans who navigate by clicking instead of by path. The rules are
architectural, not stylistic:

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

## What to read per task

The full routing table lives in [`START_HERE.md`](START_HERE.md) — the
context router. Summary:

| If the task is… | Read |
|---|---|
| Any work (always) | `02-organization/ai-policy.md` |
| Understanding the business or vocabulary | `00-context/` + `00-context/glossary.md` |
| Working inside a code repo | `02-organization/conventions/`, `04-architecture/repos.yaml` |
| Reading or planning tickets | `02-organization/conventions/ticketing.md` |
| A change that crosses systems | `04-architecture/systems-map.md`, `integrations.md` |
| Touching requirements or rules | `05-requirements/` |
| Making or checking a decision | `06-decisions/decision-log.md` |
| Status, next steps, who owns what | `07-delivery/`, `02-organization/ownership.md` |
| Processing raw material | `99-inbox/README.md`, `07-delivery/validation-matrix.md` |
| Starting or retyping a work unit | `03-work/README.md`, `03-work/_templates/` (pick the tier) |
| A recurring meeting vs. a one-off | `01-meetings/README.md` |
| Anything touching a person | `docs/privacy-boundaries.md` |
| Writing something automated | `02-organization/automation-map.md` |
| Content from an external system of record | `.github/skills/query_system_of_record.md` |
| Adding or renaming a canvas view | `maps/README.md`, `docs/obsidian.md` |
| Enabling telemetry | `docs/telemetry.md` |
| Reusable capability notes (if `12-capabilities` active) | `12-capabilities/README.md` |
| Named people or teams (if `14-people` active) | `14-people/README.md` |

Load only the sections the active task needs — never the whole brain.

## Processing workflow (meetings and raw sources)

When processing a transcript, email, or inbox file, extract in this order:

1. Decisions → `06-decisions/decision-log.md`
2. New requirements → `05-requirements/`
3. Changes to existing requirements → update in place, mark old `SUPERSEDED`
4. Open questions → `05-requirements/open-questions.md`
5. Risks → `07-delivery/current-status.md`
6. Action items → `07-delivery/action-items.md`
7. New systems or vendors mentioned → `04-architecture/`, `08-vendors/`
8. Work-unit impacts → `03-work/<work-unit>/`, **and link the work unit from
   every decision, risk, action item and minutes row that concerns it.** That is
   what makes backlinks answer "what is going on with X".
9. Conflicts with current architecture, roadmap, or decisions → flag them
10. List the canonical files updated (the minutes template has a section for it)

Then mark the source as processed (see `99-inbox/README.md`) — evidence stays
for traceability, but its extraction is done.

### Recurring meetings and bitácoras

**Recurring meetings do not go through the workflow above by default.** A series
with continuity keeps a single **bitácora** at
`01-meetings/minutes/<series>/<series>.md`: a header with cadence and
participants, what to raise next call, the pending items that carry over, and a
dated log newest-first. Sessions are headings inside it, not files. Most
sessions are three bullets and stop there.

Run the workflow only when a session earns it — a transcript, or decisions,
risks and actions that must reach the canonical registers — and then link the
resulting dated file from that date's log entry.

**Never duplicate the *Next call* or *Pending* sections into another file.**
Copying them is precisely what stops them carrying over: the copy starts empty
each session and the original stops being read.

A **collection of one-off meetings** (pre-sales calls, interviews, ad-hoc
sessions) is the other shape: one dated file per meeting under its own folder,
each with its own source register, and no bitácora — there is no continuity to
carry. See [`01-meetings/README.md`](01-meetings/README.md).

One-on-one logs live in `01-meetings/minutes/1-1/`, one per direct report,
**named after the person** so the log appears in that person's backlinks.
Operational commitments only; the privacy notice at the top of each file is not
optional.

## Automation zones

An automated update writes inside **one zone at a time**. Each zone in
`02-organization/automation-map.md` (if that module is active)
declares its allowed targets, what to read first, the checks it must run, and —
the row that matters — what is **forbidden**. An agent that can write anywhere
will eventually write the right fact into the wrong file.

No automation writes to a corporate system without documented human approval.

## Skills

Two kinds, one discovery surface:

- **Internal (lifecycle)** — source of truth `.github/skills/`: bootstrap,
  process_meeting, record_decision, add_runbook, update_domain_context,
  quarterly_context_review, query_system_of_record. Distributed with this
  template's releases. Each one is either a flat `<name>.md` or a
  `<name>/SKILL.md` folder bundling the scripts, templates or references it runs.
- **External (working skills)** — synced from the engineering harness into
  `.github/skills-external/` per the `harness` section of `brain.config.json`
  (default set: brainstorming, brainstorm_quick, writing-plans,
  writing-clearly-and-concisely, research_current_info, retrospective).
  Source of truth is the harness — improve them there, resync here.

`make sync-skills` refreshes the external set (lockfile: `skills-lock.json`)
and regenerates the native projections `.claude/skills/`, `.codex/skills/`,
`.agents/skills/`, `.opencode/skills/` so Claude Code, Codex, Antigravity and
OpenCode discover every skill. It also rewrites the generated skill list in
`OPENCODE.md`. Projections are generated — never edit them by hand. A sync that
would drop frontmatter keys from a skill keeps the local copy and reports it;
`--force` overrides.

## Exit gate

`make validate` must pass before any merge. It checks structure (per
`brain.config.json`), links, duplicate IDs, Canvas references, work-unit
frontmatter, index freshness, and decisions without sources, and reports
status-marker, work-unit and possible-secret debt.
