# Governance of this repository

## What belongs and what does not

| Belongs | Does not belong |
|---|---|
| Durable engagement context: domain, decisions, requirements, conventions, systems, vendors | Product code |
| Registered evidence (contracts, transcripts, vendor docs) with a source register | Docs of a specific repo (they go in that repo) |
| The organization's AI policy and ways of working | Engineering skills/rules enforcement (that is the harness) |
| | Secrets, credentials, unnecessary personal data |

## How it changes

- Content: normal PR, approved by the module owner
  (`02-organization/ownership.md`). The PR checklist enforces sourcing.
- Decisions: immutable — supersede with a new DEC, never edit.
- Module structure: public interface (consumer adapters reference it) —
  changing it is `MAJOR` and requires a DEC.
- Operating rules live ONLY in `AGENTS.md`; tool adapters point at it.
  Never grow a second rule set in an adapter file.

## Quality

- `make validate` must pass on every PR.
- `_PENDING_` placeholders, unprocessed inbox files, and unsourced decisions
  are visible debt; bootstrap and quarterly reviews drive them down.

## Relationship to the harness

This repo is the **context** layer (what the organization knows and how it
works, declared). The harness is the **execution** layer (how work is done,
enforced). Code repos import both from their adapters.
