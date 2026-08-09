---
name: quarterly_context_review
description: Use every ~90 days (or after major org changes) to fight drift — audits the whole brain against reality, marks stale content, reduces _PENDING_ debt, and reports brain health to the owners.
---

# Skill: quarterly_context_review

## Purpose

Keep the brain trustworthy: stale context is worse than missing context. This
review compares each section against current reality and produces a fix list.

## Required Input

- Read access to the organization's repos and recent activity (merged PRs,
  incidents, new services) since the last review.

## Execution Rules

1. **Freshness pass.** For each brain file: does anything contradict what repos
   and recent activity show? Mark contradictions `_STALE_` in place
   and list them.
2. **Debt pass.** Count `_PENDING_` and `_STALE_` markers per
   section; compare against the previous review (git log of this file's
   report).
3. **Ownership pass.** Every section owner in `team/ownership.md` still exists
   and still owns it? Orphaned sections are the top finding.
4. **Usage pass.** If the harness lab / gateway logs are available: which brain
   files do agents actually read? Sections never consulted are candidates to
   merge or delete — a smaller, accurate brain beats a large stale one.
5. Fix what is mechanical in the same PR; open issues (with owner and date) for
   what needs humans. Run `make validate`.
6. Write the report to `memory/learnings.md` (dated entry) and notify owners.

## Output Format

- Health report: markers count by section, contradictions found, orphaned
  sections, top 3 fixes with owner and date.
