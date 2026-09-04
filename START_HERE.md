# Start here

This file is the **context router**. It does not contain rules (that's
[`AGENTS.md`](AGENTS.md)) or an explanation of the template (that's
[`README.md`](README.md)) — it tells you, in one look, where to go for a
given task. Load only the sections the active task needs.

## By task

| If the task is… | Read |
|---|---|
| Any work (always) | [`AGENTS.md`](AGENTS.md), `02-organization/ai-policy.md` |
| Understanding the business or vocabulary | `00-context/` + `00-context/glossary.md` |
| Working on a client engagement, opportunity, product, or initiative | `03-work/<work-unit>/overview.md` (check its `tier` first) |
| Working inside a code repo | `02-organization/conventions/`, `04-architecture/repos.yaml` |
| Reading or planning tickets | `02-organization/conventions/ticketing.md` |
| A change that crosses systems | `04-architecture/systems-map.md`, `integrations.md` |
| Touching requirements or rules | `05-requirements/` |
| Making or checking a decision | `06-decisions/decision-log.md` |
| Status, next steps, who owns what | `07-delivery/`, `02-organization/ownership.md` |
| Processing raw material | `99-inbox/README.md`, `07-delivery/validation-matrix.md` |
| A role-specific question (engineering, sales, delivery, security) | `02-organization/hubs/` if present — a hub composes canonical docs, it does not replace them |
| What capabilities the org has actually shipped | `12-capabilities/capability-register.md` (if active) |

## By role

- **New team member:** `00-context/` → `02-organization/ways-of-working.md` →
  `02-organization/ownership.md`.
- **Consultant/agent starting a session:** `AGENTS.md` → this file's task
  table → the specific canonical document.
- **Someone taking over an engagement:** `06-decisions/decision-log.md` →
  `07-delivery/current-status.md` → the relevant `03-work/<work-unit>/`.

## First 60 seconds in an unfamiliar brain

1. Check `brain.config.json` — which modules are active for this engagement.
2. Skim `07-delivery/current-status.md` — what's happening right now.
3. Open the specific `03-work/<work-unit>/overview.md` for the task at hand.

Everything canonical traces back to a source. If a document doesn't cite one
for a non-obvious claim, treat it as debt, not fact — see `AGENTS.md`.
