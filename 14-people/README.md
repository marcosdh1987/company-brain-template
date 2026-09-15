# 14-people — Person & Team entities

Optional module. Minimal `person` and `team` entities for **navigation
and context**, not an HRIS. The only reason this module exists is so
Obsidian's Graph and Backlinks — and any agent following wikilinks — can
answer "who's on this, what team are they on, what are they working
on" by clicking or by grep, without a spreadsheet.

Off by default; on by default for the `team`, `engineering-management`,
and `consulting-company` profiles (`brain.config.json` →
`modules["14-people"]`).

## Privacy boundary — read this before adding anyone

The allowlist of fields a person page may carry, and the categories that may
never enter this repository at all, are written down **once**, in
[`docs/privacy-boundaries.md`](../docs/privacy-boundaries.md). Read it before adding a
person.

If a fact about a person doesn't fit the allowlist, it doesn't belong in this
module — full stop. Route it to whatever system your organization already uses
for that, and reference that system's *location* here if you must, never its
content.

Two conventions keep this module honest as it grows:

- **A person's own page is authoritative for their current assignment.** Every
  other page links to it rather than restating it, so there is one place to
  correct when someone moves.
- **Not everyone gets a page.** People outside this brain's scope are named
  where the evidence names them and nothing more: no page, no roster entry, no
  capacity figure. When a working group spans teams, record only the in-scope
  share and say explicitly that the rest sits outside this brain. A page is a
  commitment to keep something current; do not make it for someone whose
  information you do not own.

If your organization also records client relationships as entities, note that
such a record is a *relationship*, not a work unit, and never a substitute for
one — and never infer participation in a work unit from an assignment to a
client. Link a person to a work unit only when a source confirms it.

## Contents

- `_templates/person.md` — one file per person, e.g. `14-people/jane-doe.md`
- `_templates/team.md` — one file per team, e.g. `14-people/machine-learning.md`

Frontmatter is documented inline in each template, not schema-enforced —
consistent with how `03-work/_templates` documents its frontmatter.
Link a person to their team, projects, and assignments with wikilinks
(`"[[Machine Learning]]"`) so Obsidian's Graph and Backlinks make the
org structure explorable without a separate diagram.
