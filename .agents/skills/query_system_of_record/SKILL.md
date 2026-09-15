---
name: query_system_of_record
description: Use when a task needs current content from an external system of record (wiki, tracker, CRM, HR system) reachable through a local read-only bridge — fetches the answer, marks it PENDING VALIDATION with a dated citation and its read scope, and never promotes it on its own. Register the bridge in 04-architecture/integrations.md before first use.
---

# Skill: query_system_of_record

## When to use

A task needs something that lives in a corporate system, not in this brain: a
wiki page, a ticket's current state, a CRM record, a roster count.

This is a **read-only** bridge. It never writes to the external system and
never edits brain files by itself. Its answer is evidence, like any other
external source — not a canonical fact until promoted through the normal
ingestion path.

If no bridge is configured, say so and stop. Do not substitute a guess, and do
not reconstruct the answer from stale content already in the brain while
presenting it as current.

## Parameters

Fill these in once, where the table says, and never inline them into this file.

| Parameter | Value | Recorded in |
|---|---|---|
| System of record | _PENDING_ | `04-architecture/integrations.md` |
| Bridge name | _PENDING_ | `04-architecture/integrations.md` |
| Base URL | _PENDING_ | `.env` — never committed |
| Health endpoint | _PENDING_ | `04-architecture/integrations.md` |
| Readiness endpoint | _PENDING_ | `04-architecture/integrations.md` |
| Query endpoint | _PENDING_ | `04-architecture/integrations.md` |
| Read scope | _PENDING_ — one page / one section / whole workspace | `04-architecture/integrations.md` |
| Restricted reads | _PENDING_ | `02-organization/privacy-boundaries.md`, `ai-policy.md` |
| Bridge owner | _PENDING_ | `02-organization/ownership.md` |

## Preconditions

Three things that look equivalent and are not:

- **Liveness is not readiness.** A bridge can answer `200` while its session
  has expired. Confirm it can actually *read* before trusting an answer, and
  never fill a failed read with inference — say the bridge is down and stop.
- **Reachability is not permission.** That the bridge *can* open a page says
  nothing about whether its content may pass through an external model or be
  stored here. Check `ai-policy.md` and `privacy-boundaries.md` first.
- **Writes are out of scope by construction.** If the bridge can write, this is
  the wrong skill: a write to an external system requires documented human
  approval and a different, named procedure.

## How to call it

```bash
# Parameters come from the environment, never from this file.
curl -s --max-time 30 "${BRIDGE_BASE_URL}${READINESS_ENDPOINT}"   # check first
curl -s --max-time 60 "${BRIDGE_BASE_URL}${QUERY_ENDPOINT}" \
     --get --data-urlencode "q=<the question>"
```

## Querying a page that holds restricted categories

Sometimes the answer you need is a count, and the page holding it also holds
things this brain must never store — candidate names, review outcomes, salaries.

Ask only for aggregates: counts, a status distribution, a last-edited date.
State explicitly in the query that you do **not** want individuals listed,
named, described, ranked or summarised.

If the answer volunteers restricted content anyway, do not copy it into a file,
a commit message or a summary. Report only the aggregate that was asked for,
and tell the user the bridge over-answered.

## Files to read

- `04-architecture/integrations.md` — the bridge's registration
- `02-organization/ai-policy.md` — whether this content may be processed at all
- `02-organization/privacy-boundaries.md` — the restricted categories

## Files this skill may modify

**None.** This skill only fetches; it never promotes. Route a fact worth keeping
through `99-inbox/` and then `process_meeting`, `update_domain_context` or
`record_decision`, which is where sourcing and status marking happen.

## Status marking

Never `CONFIRMED` on its own. A bridge answer is a paraphrase of a live read,
not a citation-grade source. Mark it `PENDING VALIDATION`, cite it as
`<system>, via <bridge>, <date>`, and record the read scope whenever the scope
changes how much to trust the answer.

## Closing validations

- Readiness was checked, not just liveness.
- The answer is dated and status-marked.
- No restricted category was requested.
- For a page holding restricted categories, aggregates only.

This is caller-side discipline, not an enforced boundary. If that gap matters
for your setup, record it as an open question in the brain rather than assuming
it is closed.
