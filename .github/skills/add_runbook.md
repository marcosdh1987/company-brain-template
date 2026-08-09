---
name: add_runbook
description: Use when a procedure was explained ad-hoc (chat, call, incident) for the second time — converts it into a runbook with verification and rollback, executable by a new person or an agent.
---

# Skill: add_runbook

## Purpose

Turn tribal operational knowledge into a runbook in `brain/runbooks/`, written
so a newcomer — or an agent with the right access — can execute it safely.

## Required Input

- The procedure as currently explained (paste the chat/notes), and who performs
  it today (they become the owner unless someone else is named).

## Execution Rules

1. Copy `runbooks/template.md`; name the file by the action, kebab-case.
2. Steps must be verifiable: exact commands, exact UI paths, expected output.
   Rewrite vague steps ("check that it works") into observable checks.
3. Risk and rollback are mandatory. If rollback does not exist, write
   "no rollback — ask <owner> for help before executing" explicitly.
4. Never include secrets — reference the secret manager entry by name.
5. Add the row to `runbooks/README.md` index. Run `make validate`.
6. If possible, have the owner (or the agent, in a sandbox) walk the runbook
   once end-to-end before merging; note the date of that dry run.

## Output Format

- The runbook path, its index row, and any step that could not be verified.
