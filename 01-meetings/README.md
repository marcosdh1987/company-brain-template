# 01-meetings

Two zones with different trust levels:

- `transcripts/` — **raw evidence**: recordings' transcripts, exported
  summaries, PDFs. Never edited, never treated as validated fact.
- `minutes/` — **reviewed summaries** produced from a transcript using
  `minutes/meeting-template.md`. Minutes still cite their transcript.

Naming: `YYYY-MM-DD-short-description.<ext>` for transcripts,
`YYYY-MM-DD-short-description-minutes.md` for minutes. Undated material gets
the `undated-` prefix and a note in the source register.

## The two kinds of folder under `minutes/`

Not every meeting deserves a file. What a meeting needs depends on whether it
has continuity.

| | Series with continuity | Collection of one-off meetings |
|---|---|---|
| Examples | a weekly team sync, a recurring account call, a 1-1 | pre-sales calls, interviews, ad-hoc sessions |
| Shape | **one bitácora file** per series, or per person: `minutes/<series>/<series>.md` | **one dated file each**: `minutes/<collection>/YYYY-MM-DD-*.md` |
| A session is | a dated heading inside the bitácora | its own file, with its own source register |
| Carries over | yes — that is the whole point | nothing to carry |
| Template | `minutes/series-bitacora-template.md`, or `minutes/one-on-one-bitacora-template.md` | `minutes/meeting-template.md` |

A **series** keeps a single file: a header with cadence and participants, what
to raise next call, the pending items that carry over, and a dated log
newest-first. Most sessions are three bullets and stop there.

**A session only becomes its own dated file when it earns one:** a full
transcript, or decisions, risks and actions that need the formal processing
workflow. Then the bitácora's entry for that date links it.

**Never duplicate the *Next call* or *Pending* sections into another file.**
Copying them is precisely what stops them carrying over — the copy starts empty
each session and the original stops being read.

One-on-one logs live in `minutes/1-1/`, one per direct report, **named after the
person** so the log surfaces in that person's backlinks. Operational
commitments only; the privacy notice at the top of that template is not
optional.

Bitácoras are working notes: write them in the language the meeting runs in, per
the language rule in [`AGENTS.md`](../AGENTS.md).

## Layout

```text
minutes/
├── meeting-template.md                  # one-off meeting -> dated file
├── series-bitacora-template.md          # recurring series -> one bitácora
├── one-on-one-bitacora-template.md
├── <series-slug>/<series-slug>.md       # e.g. team-weekly/team-weekly.md
├── 1-1/<first-last>.md                  # one per direct report
└── <collection>/YYYY-MM-DD-*.md         # e.g. pre-sales/ — one file each
```

---

Processing a meeting end-to-end (extraction order, where each item goes) is
defined in `AGENTS.md` → "Processing workflow", and automated by the skill
`.github/skills/process_meeting.md`. Recurring series are **exempt** from that
workflow by default — see `AGENTS.md` → "Recurring meetings and bitácoras".
