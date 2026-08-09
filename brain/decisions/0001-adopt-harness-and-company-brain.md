# 0001 — Adopt engineering harness + company brain

- **Status:** accepted
- **Date:** _set at bootstrap_
- **Deciders:** _set at bootstrap_
- **Scope:** all of the organization's repos

## Context

AI-assisted development without foundations amplifies existing problems
(DORA 2025): scattered rules, context re-explained every session, no
measurement. The organization needs (a) a reusable, versioned engineering
governance layer, and (b) an agent-readable source of truth for organizational
context.

## Decision

Adopt the engineering harness (governance template, consumed through semver
releases via selective sync) and this company brain (the organization's own
repo) as the two context layers repos import from their adapters
(`CLAUDE.md` / `AGENTS.md`).

## Alternatives considered

- Rules hand-copied into each repo: immediate drift, no versioning.
- One monolithic repo with everything: mixes client context with the reusable
  engine; impossible to update without friction.
- Assistant memory only (no repo): not auditable, not shareable, gets lost.

## Consequences

- Each repo declares in its adapter which layers it imports and which harness
  version it is on.
- The brain requires ownership and a quarterly review (see `team/ownership.md`).
- Harness improvements arrive measured (lab) before adoption; the brain is
  refined through use.
