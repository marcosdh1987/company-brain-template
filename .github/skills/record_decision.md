---
name: record_decision
description: Use when a cross-repo decision was made (or is being proposed) and must be recorded as an organizational ADR — numbers it, writes it from the template, and updates the index and any superseded ADR.
---

# Skill: record_decision

## Purpose

Capture one organizational decision as a durable, numbered ADR in
`brain/decisions/`, correctly linked to what it supersedes.

## Required Input

- The decision (or proposal), who made it, when, and the alternatives that were
  on the table. Ask for what is missing; do not invent alternatives.

## Execution Rules

1. Confirm scope is organizational (affects >1 repo). Single-repo decisions go
   to that repo's `docs/adr/` — say so and stop.
2. Next sequential number; copy `template.md`; status `proposed` unless the
   decision is already in effect (`accepted`).
3. Context section states facts and forces, not opinions. Consequences include
   at least one cost, not only benefits.
4. If it supersedes an ADR: mark the old one `superseded by NNNN` — never
   edit its content.
5. Update the index table in `decisions/README.md`. Run `make validate`.

## Output Format

- The new ADR path and its one-line summary; the superseded ADR if any.
