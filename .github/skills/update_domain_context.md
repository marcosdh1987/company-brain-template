---
name: update_domain_context
description: Use when the business changed — new entity, rule, integration or vocabulary — and the brain must absorb it without drifting: locates every affected section, updates them consistently, and records provenance.
---

# Skill: update_domain_context

## Purpose

Absorb one business change into the brain consistently (domain, glossary,
architecture, rules), instead of patching one file and letting the rest drift.

## Required Input

- The change, in one or two sentences, and its source (decision, PR, incident,
  conversation with a named person).

## Execution Rules

1. Classify the change: entity | business rule | integration | vocabulary |
   ownership. One change may touch several.
2. Grep the brain for every mention of the affected concepts; list files to
   touch before editing any.
3. Update each file respecting its format (tables, BR-NNN ids, mermaid maps).
   New rules get the next BR number; renamed terms keep an alias row in the
   glossary pointing to the canonical entry.
4. If the change contradicts an accepted ADR, do not silently edit: flag that a
   superseding ADR is needed (`record_decision`).
5. Run `make validate`. Summarize what changed and cite the source.

## Output Format

- List of files touched with a one-line diff summary each, plus provenance.
- Any ADR flagged as needing supersession.
