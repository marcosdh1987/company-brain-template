---
name: record_decision
description: Use when a decision was made (or proposed) that affects the engagement — records it as an immutable DEC entry in the decision log with mandatory source, handling supersession and status correctly.
---

# Skill: record_decision

## Purpose

Capture one decision as a durable, numbered entry in
`06-decisions/decision-log.md`, correctly linked to what it supersedes.

## Required Input

- The decision (or proposal), who made it, when, its source, and the
  alternatives considered. Ask for what is missing; never invent.

## Execution Rules

1. Confirm scope: engagement/organization level. Single-repo technical
   decisions go to that repo's `docs/adr/` — say so and stop.
2. Next sequential `DEC-XXX`; copy the entry template at the bottom of the
   log. Status `PENDING` unless evidence records agreement (`ACCEPTED`);
   contractual decisions stay `PENDING` until execution is confirmed.
3. The **Source** field is mandatory — the validator reports unsourced
   decisions. Impact includes at least one cost.
4. If it supersedes: mark the old entry's Status `SUPERSEDED by DEC-XXX` —
   never edit its content.
5. `make validate`.

## Output Format

- The new DEC id and one-line summary; the superseded DEC if any.
