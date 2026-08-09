# Maintenance: how the brain stays alive

A stale brain is worse than no brain: agents act confidently on outdated data.
Maintenance is a process with three legs:

## 1. Continuous (with every business change)

- The business changed → skill `update_domain_context` (locates ALL affected
  sections, not just one).
- Something cross-cutting was decided → skill `record_decision`.
- A procedure was explained for the second time → skill `add_runbook`.

## 2. Quarterly (anti-drift)

Skill `quarterly_context_review`, every ~90 days: checks the brain against the
repos and real activity, marks `_STALE_`, measures marker debt, verifies
owners, and reports health to the owners. The report is dated and stored in
`memory/learnings.md`.

## 3. Automated (gates)

- `make validate` in this repo's CI: healthy structure and links on every PR.
- Optional, with the harness lab: measure which sections agents actually
  consult in their runs — what is never read gets shrunk or deleted. A small,
  accurate brain beats a large, dubious one.

## Versioning

Semver tags + `CHANGELOG.md`. The folder structure is a public interface
(other repos' adapters reference it): renaming folders is `MAJOR` and requires
an ADR.

## Signs it is working

- Domain questions that used to be answered over chat are now answered with a
  link to the brain.
- Agents' PRs cite rules (BR-NNN) and ADRs by number.
- Onboarding a new person drops from weeks to days with
  `runbooks/onboarding-dev.md` + `brain/00-index.md`.
