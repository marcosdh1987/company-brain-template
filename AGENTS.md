# AI Agent Operating Instructions

This repository is the **company brain** for __ORG_NAME__: the persistent,
agent-readable knowledge base for the engagement. It stores durable context,
not application code. This file is the single source of operating rules —
every tool adapter (`CLAUDE.md`, Copilot, etc.) defers to it. For "where do I
look first for this task", see [`START_HERE.md`](START_HERE.md); for "what
is this template", see [`README.md`](README.md).

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
- Work-unit-specific content stays in `03-work/<work-unit>/`, tiered by
  rigor (T0/T1/T2 — see `03-work/README.md`); cross-work-unit content in the
  shared sections.
- Match traceability to tier: a T0 exploration does not need the sourcing
  rigor of a T2 client engagement. Never retrofit — promote the tier instead
  when the work becomes decision-grade or client-facing.
- Numbered folders beyond the core set (`10-management/`, `11-ml-governance/`,
  `12-capabilities/`, `13-security/`, …) are **domain modules**: optional,
  never assumed active, declared in `brain.config.json`.
- A **role hub** (`02-organization/hubs/<role>-hub.md`) is a task-oriented
  context router composed over canonical documents — it is never a new
  source of truth. It points; it does not restate.
- Never store credentials, passwords, API keys, MFA seeds, private keys, or
  unnecessary personal data. Reference secret locations, never values.
- Keep documents concise and actionable.

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
8. Work-unit impacts → `03-work/<work-unit>/`
9. Conflicts with current architecture, roadmap, or decisions → flag them
10. List the canonical files updated (the minutes template has a section for it)

Then mark the source as processed (see `99-inbox/README.md`) — evidence stays
for traceability, but its extraction is done.

## Skills

Two kinds, one discovery surface:

- **Internal (lifecycle)** — source of truth `.github/skills/*.md`: bootstrap,
  process_meeting, record_decision, add_runbook, update_domain_context,
  quarterly_context_review. Distributed with this template's releases.
- **External (working skills)** — synced from the engineering harness into
  `.github/skills-external/` per the `harness` section of `brain.config.json`
  (default set: brainstorming, brainstorm_quick, writing-plans,
  writing-clearly-and-concisely, research_current_info, retrospective).
  Source of truth is the harness — improve them there, resync here.

`make sync-skills` refreshes the external set (lockfile: `skills-lock.json`)
and regenerates the native projections `.claude/skills/`, `.codex/skills/`,
`.agents/skills/` so Claude Code, Codex, and Antigravity discover every skill.
Projections are generated — never edit them by hand.

## Exit gate

`make validate` must pass before any merge. It checks structure (per
`brain.config.json`), links, duplicate IDs, decisions without sources, and
reports status-marker debt.
