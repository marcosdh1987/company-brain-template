---
name: quarterly_context_review
description: Use every ~90 days (or after major changes) to fight drift — audits canonical content against reality, marks SUPERSEDED/PENDING VALIDATION where the world moved, measures debt, and reports brain health to the owners.
---

# Skill: quarterly_context_review

## Purpose

Keep the brain trustworthy: stale context is worse than missing context.

## Required Input

- Read access to the organization's repos/systems and activity since the
  last review (merged PRs, incidents, new services, new contracts).

## Execution Rules

1. **Freshness pass.** Per canonical file: does anything contradict current
   reality? Mark moved facts `SUPERSEDED` (pointing to the replacement) or
   downgrade to `PENDING VALIDATION`; record source-level conflicts in the
   register.
2. **Debt pass.** Run `make validate`; compare `_PENDING_` counts, unsourced
   decisions, and unprocessed inbox against the previous report.
3. **Ownership pass.** Every owner in `02-organization/ownership.md` still
   exists and still owns it? Orphaned modules are the top finding.
4. **Usage pass.** If gateway/lab logs exist: which sections do agents
   actually read? Never-read content is a candidate to merge or delete.
5. Fix the mechanical in the same PR; open issues (owner + date) for the
   rest. `make validate` green.
6. Write the dated report to `memory/learnings.md` and notify owners.

## Output Format

- Health report: status/debt counts vs last review, contradictions found,
  orphaned modules, top 3 fixes with owner and date.
