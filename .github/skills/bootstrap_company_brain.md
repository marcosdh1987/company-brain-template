---
name: bootstrap_company_brain
description: Use when instantiating the company-brain template for an organization — fresh start or migration of an org with existing history. Guides profile selection, source mining, interviews, and initial promotion, replacing _PENDING_ placeholders only with verified, cited content.
---

# Skill: bootstrap_company_brain

## Purpose

Turn a clone of `company-brain-template` into a populated, owned brain for
one organization. Mine real sources first; interview humans only for what
mining cannot answer; never invent domain facts.

## Required Input

- Organization name, engagement profile (`consulting` /
  `delivery-oversight` / `development` / `full`), and the contact who will
  own the brain.
- Read access to available sources: repos, docs, contracts, transcripts.
- 60–90 min of interview time with 1–2 senior people (can be async).

## Execution Rules

1. **Init.** `make init ORG=<name> PROFILE=<profile>`. This writes
   `brain.config.json` and lists inactive modules. Never skip it.
2. **Choose the mode:**
   - **Fresh start** — little prior material: go to rule 3.
   - **Migration (org with history)** — contracts, transcripts, old docs
     exist: first move *everything* into `99-inbox/` and
     `09-references/`, create a **source register** from the template
     (IDs `SRC-XXX`, classification, known conflicts with precedence
     rules), and only then promote gradually. Evidence is never edited;
     conflicts are recorded, not resolved by overwriting.
3. **Mine before asking.** Per section, extract candidates from real
   sources with provenance: context/glossary ← docs, contracts, recurring
   terms; conventions ← observed branch names, PR templates, actual merge
   behavior; systems/repos ← repo list, IaC, CI configs; ownership ←
   CODEOWNERS, top committers.
4. **Interview to close gaps** — one focused list per section; ask about
   contradictions explicitly ("docs say X, code does Y — which is true?").
5. **Write with each file's own format and statuses.** `_PENDING_` with an
   owner beats plausible invention. Every promoted fact carries status and
   source.
6. **Mandatory before done:** `02-organization/ai-policy.md` filled and
   approved (when the module is active); every active module's owner named
   in `ownership.md`; DEC-001 completed with real date and deciders; if the
   org has code repos, `04-architecture/repos.yaml` populated.
7. **Gate.** `make validate` green. Hand the team the adoption snippet
   (`examples/`) and, for development profiles, run `make workspace` once to
   verify the layout.

## Output Format

- Populated brain with per-section provenance (mined vs interviewed).
- Remaining `_PENDING_` items, each with proposed owner and date.
- For migration mode: the source register with its conflicts table.
- Next step: schedule `quarterly_context_review` 90 days out.
