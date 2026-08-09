# Governance of this repository

## What belongs and what does not

| Belongs | Does not belong |
|---|---|
| Durable organizational context (domain, decisions, conventions, systems map, runbooks, glossary) | Product code |
| Cross-cutting learnings and patterns (`memory/`) | Docs of a specific repo (they go in that repo) |
| The organization's AI policy | Engineering skills/rules (they go in the harness) |
| | Secrets, credentials, personal data |

## How it changes

- Content changes: normal PR, approved by the section owner
  (`brain/team/ownership.md`).
- Decisions: an accepted one is never edited; it is superseded by a new ADR.
- Folder structure: it is a public interface (other repos' adapters reference
  it) — changing it is `MAJOR` and requires an ADR.

## Quality

- `make validate` must pass on every PR: complete structure, no broken links.
- `_PENDING_` markers are visible debt: the goal of the bootstrap and the
  quarterly reviews is to drive them to zero in active sections.

## Relationship to the harness

This repo is the **context** layer (what the organization knows). The harness is
the **execution** layer (how work is done). Code repos import both from their
adapters. The `bootstrap_company_brain` skill and the maintenance skills are
distributed with the harness; this repo only references them.
