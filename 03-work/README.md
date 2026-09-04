# 03-work

One folder per **work unit** — a client engagement, sales opportunity,
internal product, or initiative. Copy the tier template that matches its
rigor (`_templates/t0/`, `t1/`, or `t2/`) to start one. Work-unit folders hold
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
sets *how much rigor* it carries — see below. Keep `updated` current; it is
what `scripts/build_indexes.py` uses to flag stale work units.

## Graduated rigor (tiers)

Not every work unit needs the same ceremony. Tier is a judgment call by the
owner, revisited as the work unit matures — an exploratory T0 idea that turns
into a client proposal should be promoted to T1/T2, not retrofitted after the
fact.

| Tier | Use for | Shape |
|---|---|---|
| **T0** | Internal chats, early exploration, ideas not yet worth structuring | Single `overview.md`: what it's about, notes, next steps. No source-per-claim requirement. |
| **T1** | Active internal or low-stakes work; opportunities being scoped | `overview.md`, `current-state.md`, `open-questions.md`, `change-log.md`. Cite sources only for claims that are client-facing or feed a decision. |
| **T2** | Client engagements, anything that ends in a commercial proposal, or work that feeds `06-decisions/` | Full shape below. Every non-obvious claim carries a status and a source. |

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
regardless of tier.
