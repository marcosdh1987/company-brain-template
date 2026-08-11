# 01-meetings

Two zones with different trust levels:

- `transcripts/` — **raw evidence**: recordings' transcripts, exported
  summaries, PDFs. Never edited, never treated as validated fact.
- `minutes/` — **reviewed summaries** produced from a transcript using
  `minutes/meeting-template.md`. Minutes still cite their transcript.

Naming: `YYYY-MM-DD-short-description.<ext>` for transcripts,
`YYYY-MM-DD-short-description-minutes.md` for minutes. Undated material gets
the `undated-` prefix and a note in the source register.

Processing a meeting end-to-end (extraction order, where each item goes) is
defined in `AGENTS.md` → "Processing workflow", and automated by the skill
`.github/skills/process_meeting.md`.
