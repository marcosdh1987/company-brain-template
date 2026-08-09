# Brain index — start here

> **Organization:** __ORG_NAME__

> This file is the entry point for agents and people. It says what to read per
> task, so the context is not flooded with the whole brain (rule: inject only
> what is relevant to the active task).

## What to read per task

| If the task is… | Read |
|---|---|
| Any work (always) | `ai-policy.md` — the organization's AI posture |
| Touching business logic | `domain/overview.md`, `domain/business-rules.md`, `glossary.md` |
| Creating or modifying entities/models | `domain/entities.md`, `glossary.md` |
| A change that crosses systems | `architecture/systems-map.md`, `architecture/integrations.md` |
| Creating a branch/commit/PR | `conventions/git-workflow.md`, `conventions/engineering.md` |
| Making or proposing a cross-cutting decision | `decisions/README.md` (and record an ADR from its template) |
| Operating something (deploys, credentials, incidents) | `runbooks/` — search by action name |
| You don't know who to ask | `domain/stakeholders.md`, `team/ownership.md` |

## What this repo is (and is not)

- **It is** the source of truth for organizational context: domain, decisions,
  vocabulary, conventions, systems map, procedures.
- **It is not** the engineering harness (skills, code rules, gates): that
  reaches each repo from the governance template, versioned by releases.
- **It is not** documentation of a specific repo: that lives in each repo.

## Golden rules

1. Stale context is worse than missing context: if you find something outdated,
   fix it or mark it `_STALE_` on the spot.
2. Everything here has an owner (`team/ownership.md`). No owner, no entry.
3. Nothing sensitive: no secrets, no credentials, no customer personal data.
   Agents read this repo; treat it as semi-public.
