# Claude Code Adapter — Company Brain

This repository is the organization's **company brain**: context, not code. Use
it as the canonical source of organizational knowledge.

## How to read this repo

- Entry point: `brain/00-index.md` — it says what to read per task.
- **Selective injection:** load only the sections relevant to the active task.
  Do not read the whole brain "just in case".
- `brain/ai-policy.md` ALWAYS applies to any AI-assisted work in this
  organization.

## How to modify this repo

- Governance: `.github/brain-governance.md` (what belongs, what does not, how it
  changes).
- Use the governed skills in `.github/skills/`:
  `bootstrap_company_brain`, `update_domain_context`, `record_decision`,
  `add_runbook`, `quarterly_context_review`.
- Never edit an accepted decision — supersede it with a new ADR.
- Never invent domain facts: leave `_PENDING_` with an owner rather than
  plausible content without a source.
- Exit gate: `make validate` green.

## What NOT to do here

- Do not add product code or single-repo documentation.
- Do not paste secrets, credentials, or personal data.
- Do not delete `_PENDING_`/`_STALE_` markers without actually resolving them.
