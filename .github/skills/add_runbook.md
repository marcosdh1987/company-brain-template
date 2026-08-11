---
name: add_runbook
description: Use when a procedure was explained ad-hoc for the second time — converts it into a runbook with verification and rollback. Org-level procedures go to 02-organization/runbooks/, project-specific ones to the project folder.
---

# Skill: add_runbook

## Purpose

Turn tribal operational knowledge into a runbook a newcomer — or an agent
with the right access — can execute safely.

## Required Input

- The procedure as currently explained (paste chat/notes) and who performs
  it today (default owner).

## Execution Rules

1. Decide the home: applies across the org →
   `02-organization/runbooks/`; specific to one project →
   `03-projects/<p>/`. Copy the runbook template; kebab-case action name.
2. Steps must be verifiable: exact commands, exact UI paths, expected
   output. Rewrite vague steps into observable checks.
3. Risk and rollback are mandatory; if no rollback exists, write "no
   rollback — ask <owner> before executing".
4. Never include secrets — reference the secret manager entry by name.
5. Index it (runbooks README or project overview). `make validate`.
6. If possible, walk it once end-to-end before merging; note the dry-run
   date.

## Output Format

- The runbook path, its index row, any step that could not be verified.
