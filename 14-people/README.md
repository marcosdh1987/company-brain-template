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

**Allowed** (shareable, professional, operational):
- role
- team
- public/professional location
- specialty
- project
- assignment
- operational meetings
- work relationships

**Never store here** (this is a hard boundary, not a style preference):
- compensation
- health
- disciplinary records
- private performance feedback
- confidential 1:1 content
- unnecessary personal information

If a fact about a person doesn't fit the allowed list, it doesn't belong
in this module — full stop. Route it to whatever system your
organization already uses for that (HRIS, private 1:1 notes, etc.), and
reference that system's *location* here if you must, never its content.

## Contents

- `_templates/person.md` — one file per person, e.g. `14-people/jane-doe.md`
- `_templates/team.md` — one file per team, e.g. `14-people/machine-learning.md`

Frontmatter is documented inline in each template, not schema-enforced —
consistent with how `03-work/_templates` documents its frontmatter.
Link a person to their team, projects, and assignments with wikilinks
(`"[[Machine Learning]]"`) so Obsidian's Graph and Backlinks make the
org structure explorable without a separate diagram.
