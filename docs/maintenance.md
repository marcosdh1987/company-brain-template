# Maintenance: how the brain stays alive

A stale brain is worse than no brain: agents act confidently on outdated
data. Three legs:

## 1. Continuous (with every intake)

Raw material → inbox/meetings/references → processed per the workflow in
`AGENTS.md` → promoted with status + source → source marked `processed--`.
The skills automate it: `process_meeting`, `update_domain_context`,
`record_decision`, `add_runbook`.

## 2. Quarterly (anti-drift)

Skill `quarterly_context_review`, every ~90 days: checks canonical content
against the repos and recent activity, marks `SUPERSEDED`/`PENDING
VALIDATION` where reality moved, measures debt (placeholders, unprocessed
inbox, unsourced decisions), verifies owners, and writes a dated report to
`memory/learnings.md`.

## 3. Automated (gates)

`make validate` in CI on every PR: structure per config, links, duplicate
IDs, unsourced decisions, debt report. Optionally, with the harness lab:
measure which sections agents actually read — never-read content gets merged
or deleted.

## Versioning

Semver tags + `CHANGELOG.md`. The module structure is a public interface
(consumer repos' adapters reference it): renaming modules is `MAJOR` and
requires a DEC.

## Signs it is working

- Domain questions get answered with a link, not a chat explanation.
- Agents' PRs cite BR/DEC/SRC IDs.
- The periodic validation check gets filled by the client without the
  consultant present.
- Onboarding drops from weeks to days (`02-organization/runbooks/onboarding.md`).
