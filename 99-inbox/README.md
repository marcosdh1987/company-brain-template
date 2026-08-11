# 99-inbox — raw input landing zone

Anything unprocessed lands here: transcripts before minutes, copied emails,
screenshots, brain-dumps, vendor docs pending review.

> **Nothing in `99-inbox/` is validated knowledge.** It is evidence — it may
> contain contradictions, outdated or unconfirmed statements.

## Promotion workflow

1. Review the raw file; register it in a source register (`09-references/`)
   if it will be cited.
2. Extract per the processing workflow in `AGENTS.md` (decisions,
   requirements, questions, risks, actions, impacts, conflicts).
3. **Mark the file as processed**: rename with the `processed--` prefix
   (e.g. `processed--2026-08-09-vendor-email.md`) or move it to its
   permanent home in `09-references/` / `01-meetings/transcripts/`.
   The validator reports unprocessed files as debt.

## Naming

`YYYY-MM-DD-short-description.<ext>` — `undated-` prefix if the date is
unknown.
