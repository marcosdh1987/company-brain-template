# Role hubs

A **role hub** is a task-oriented context router for one role — engineering,
sales engineering, delivery, security, etc. It is composition, not a new
source of truth: a hub points to the canonical documents that already exist
elsewhere in the brain (`02-organization/conventions/`, `03-work/`,
`04-architecture/`, `06-decisions/`…) organized around the questions that
role actually asks.

## Rules

1. **A hub never restates canonical content.** If a fact needs to change,
   change it in the canonical document; the hub's link stays valid.
2. **A hub is optional and additive.** Delete one and nothing canonical is
   lost — the underlying documents are still there and still linked from
   `START_HERE.md`.
3. **Name them `<role>-hub.md`**, kebab-case, one per role that repeatedly
   asks the same shape of question.
4. Keep them short: a handful of sections, each linking out, not a rewrite of
   `AGENTS.md` or the module READMEs.

## When to add one

Add a hub when the same role keeps re-deriving the same routing (e.g. "where
do I look for X" gets asked in the same way every time by engineering leads).
Don't add one speculatively — start from `START_HERE.md`'s task table and
only fork out a role hub once it earns its place.

## Examples

This module ships no hubs by default. If your engagement needs them, common
starting points (see the pattern, not the content):

- `engineering-hub.md` — for engineers working across the org's repos.
- `sales-engineering-hub.md` — for pre-sales/solutioning conversations.
- `delivery-hub.md` — for delivery/project leads tracking work units.
- `security-hub.md` — for security review and compliance questions.
