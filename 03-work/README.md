# 03-work

One folder per **work unit** — a client engagement, sales opportunity,
internal product, or initiative. Copy the tier template that matches how many
documents it needs (`_templates/t0/`, `t1/`, or `t2/`) to start one. Work-unit
folders hold
the unit's **canonical** documents; their evidence still lands in
`01-meetings/`, `09-references/`, or `99-inbox/` and gets promoted here.

## Work units, not projects

The old model assumed every engagement is a "project" with the same shape.
Real work is not uniform: a client delivery, a sales opportunity being
scoped, an internal tool, and a one-off initiative all deserve a folder here,
but not all of them deserve the same traceability overhead.

Every work unit's `overview.md` starts with frontmatter:

```yaml
---
type: client            # client | opportunity | internal-product | initiative
stage: active           # exploring | active | paused | closed
tier: 1                 # 0 | 1 | 2 — see "Graduated rigor" below
owner: jane@acme.com
updated: 2025-01-15
---
```

`type` and `stage` describe *what* the work is and where it stands. `tier`
sets *how many documents* it carries. Keep `updated` current; it is what
`scripts/build_indexes.py` reads.

**`tier` is size; `type` is rigor.** How much traceability each claim owes is
set by `type`, not by tier, and the table that governs it lives in
[`AGENTS.md`](../AGENTS.md) → "Graduated rigor". A one-page `opportunity` owes
full sourcing at T0; a large internal `initiative` owes `owner` and `updated` at
T2. Do not promote a tier in order to earn the right to cite a source — that
buys ceremony and pays nothing.

## Tiers — the document set

Not every work unit needs the same number of documents. Tier is a judgment call
by the owner, revisited as the work unit grows: a tier **rises** by adding
files, and never falls.

| Tier | Use for | Shape |
|---|---|---|
| **T0** | Internal chats, early exploration, ideas not yet worth structuring | Single `overview.md`: what it's about, notes, next steps. |
| **T1** | Active internal or low-stakes work; opportunities being scoped | `overview.md`, `current-state.md`, `open-questions.md`, `change-log.md`. |
| **T2** | Work large enough to need the full document set — typically a client engagement or anything feeding `06-decisions/` | Full shape below. |

The tier contract *is* the template folder: `make validate` derives the files a
tier owes from `_templates/t<N>/`, so adding a file there enforces it for every
unit at that tier.

T2 (`_templates/t2/`) shape, the proven one from real engagements:

```text
<work-unit>/
├── overview.md         # frontmatter + objective, scope, out-of-scope/BLOCKED, canonical sources
├── current-state.md    # what exists today (observed, cited)
├── target-state.md     # where it should land (approved, not aspirational)
├── plan.md             # how to get there, step by step
├── checklist.md        # execution tracking
├── open-questions.md   # work-unit-scoped Q-<WU>-XXX (rolled up in 05-requirements)
└── change-log.md       # dated log of state changes and superseded facts
```

Keep **current state / target state / recommendation / decision** separate in
every document — blurring them is the #1 source of false confidence,
regardless of tier or type.
