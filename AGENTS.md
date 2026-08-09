# Cross-Tool Adapter — Company Brain

This repository is an organization's **company brain**: context, not code. It is
the canonical source of organizational knowledge for AI agents and humans.

## Reading

- Entry point: `brain/00-index.md` — maps tasks to the sections worth loading.
- Selective injection: load only what the active task needs, never the whole brain.
- `brain/ai-policy.md` applies to ALL AI-assisted work in this organization.

## Writing

- Governance: `.github/brain-governance.md`.
- Use the governed skills in `.github/skills/` (bootstrap, domain updates,
  decisions, runbooks, quarterly review).
- Accepted decisions are immutable — supersede, never edit.
- Never invent domain facts; a visible `_PENDING_` beats plausible fiction.
- Exit gate: `make validate` green.

## Out of scope

Product code, single-repo docs, secrets, personal data.
