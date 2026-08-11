---
name: update_domain_context
description: Use when the business changed — entity, rule, integration, vocabulary or scope — and the brain must absorb it without drifting - locates every affected section, updates them consistently with status and source.
---

# Skill: update_domain_context

## Purpose

Absorb one business change consistently (context, glossary, requirements,
architecture) instead of patching one file and letting the rest drift.

## Required Input

- The change, in one or two sentences, and its source (decision, meeting,
  incident, named person).

## Execution Rules

1. Classify: entity | business rule | integration | vocabulary | scope |
   ownership. One change may touch several.
2. Grep the brain for every mention of the affected concepts; list files to
   touch before editing any.
3. Update each file respecting its schema and IDs. New rules take the next
   BR number; renamed terms keep a synonym row pointing to the canonical
   entry; replaced facts are marked `SUPERSEDED`, never deleted.
4. If the change contradicts a recorded decision, do not silently edit —
   flag that a superseding DEC is needed (`record_decision`).
5. `make validate`. Summarize what changed, citing the source.

## Output Format

- Files touched with one-line diffs and provenance; any DEC flagged for
  supersession.
