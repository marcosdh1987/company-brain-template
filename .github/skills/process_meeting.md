---
name: process_meeting
description: Use after a meeting — takes a transcript or raw notes from 01-meetings/transcripts/ or 99-inbox/ and produces reviewed minutes plus fully promoted knowledge (decisions, requirements, questions, risks, actions), leaving the source marked processed.
---

# Skill: process_meeting

## Purpose

Run one source through the promotion pipeline end to end, so no decision or
requirement stays trapped in a transcript.

## Required Input

- The transcript/notes file (path), meeting date and participants if not in
  the file.

## Execution Rules

1. If the source is not yet in `01-meetings/transcripts/` (e.g. inbox), move
   it there with the `YYYY-MM-DD-…` naming; add it to a source register if it
   will be cited (`SRC-XXX`).
2. Create minutes from `01-meetings/minutes/meeting-template.md`, named
   `YYYY-MM-DD-<topic>-minutes.md`. Fill every section — an empty section is
   written as "None identified", not deleted.
3. Extract in the canonical order (AGENTS.md → Processing workflow):
   decisions → `DEC-XXX` entries (immutable, sourced); requirements →
   `05-requirements/` (changes mark the old value `SUPERSEDED`); open
   questions → the right `open-questions.md`; risks →
   `07-delivery/current-status.md`; actions → `ACT-XXX` rows with one named
   owner and one date; vendors/systems → registers; project impacts →
   `03-projects/<p>/` (including `change-log.md`).
4. **Conflicts are findings, not obstacles:** anything that contradicts an
   existing DEC, requirement, or architecture statement gets flagged in the
   minutes' conflicts section and, if source-level, in the source register.
5. Complete "Canonical files updated" in the minutes with every file
   touched. Mark the inbox original `processed--` if it came from there.
6. `make validate` green.

## Output Format

- The minutes path; the list of promoted items by ID (DEC/REQ/Q/ACT); the
  conflicts flagged; the files updated.
