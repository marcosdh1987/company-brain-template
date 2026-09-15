# Using this brain in Obsidian

This brain works with no `.obsidian/` folder at all — nothing here
requires Obsidian. If you'd rather browse visually than by path, this
page is the on-ramp.

Portable vault defaults **do** ship: `app.json`, `core-plugins.json`,
`graph.json` and `snippets/brain-navigation.css`. Local state does not —
`workspace.json` (one machine's open tabs) and `appearance.json` (one person's
theme) are gitignored. Enable the snippet under *Settings → Appearance → CSS
snippets*; everything it does is cosmetic.

A reader who is not in Obsidian starts at [`Home.md`](../Home.md), which is the
same launcher as plain Markdown.

## Open as a vault

In Obsidian: **Open folder as vault** → pick this repo's root. No plugin
installation is required for anything described below.

## Start at the launcher

Open `maps/home.canvas`. It's a grid of cards, each a real file in this
repo — click one to open the section's hub document. Nothing on this
canvas is "extra" content; it's the same Markdown you'd find browsing
folders, just one click closer.

## Starter views

`maps/` ships a few more starter Canvas files (`brain-overview`,
`brain-operating-model`, `portfolio`, `management`, `architecture-capabilities`) — see
`maps/README.md` for what each is for and which profile it suits best.
None of them are mandatory; delete what you don't want, keep what you
do.

## Graph and Backlinks

Obsidian's built-in **Graph view** and the **Backlinks** panel on any
open file work immediately, because the knowledge here is already
wikilinked Markdown with frontmatter — `[[Some Document]]`-style links
and `type:` fields in `05-requirements/`, `06-decisions/`, `14-people/`,
etc. The more a document links out (rather than just being linked *to*),
the more useful the graph gets.

## Properties

Frontmatter fields (`type`, `stage`, `tier`, `owner`, `updated`, and for
`14-people/`: `role`, `team`, `assignments`) show up in Obsidian's
**Properties** panel automatically — no configuration needed.

## Customizing Canvas — please do

**Feel free to duplicate, rearrange, simplify, or create new Canvas
views.** A Canvas belongs to whoever's editing it. Two conventions:

- Shared, team-useful views: normal `maps/*.canvas`, committed to git.
- Personal views: name them `maps/*.local.canvas` — gitignored, so they
  never need review or a commit.

Create a fresh one with `make new-view NAME=<slug>`.

## The source-of-truth rule

If you ever wonder "is this true because the Canvas says so, or because
a Markdown document says so" — the answer is always the Markdown
document. Canvas is how you got there, not why it's true. See `AGENTS.md`
for the full rule set.


## Two conventions worth knowing

**The full-card launcher.** `Home.md` carries a `cssclasses` value, and the
shipped snippet turns its link table into cards whose whole area is the click
target. This is deliberately **not** validated: the styling is an instance's
own, and a build gate on a CSS class would fail the moment someone redesigns
their own launcher — which `AGENTS.md` says they own. If you restyle it, nothing
breaks.

**If you ever generate a canvas.** Obsidian rewrites a canvas's JSON layout the
moment the file is opened — tabs, one node per line, key order. A generator that
compares bytes will therefore report a file as stale forever and regenerate
something identical. Compare *parsed JSON*, ignoring layout. This is the most
expensive thing to relearn about Canvas, and the reason this template does not
generate one today (see `AGENTS.md` → "Views (`maps/`) are not knowledge",
rule 4).

## Operating model

[How this brain works](../maps/brain-operating-model.canvas) is a conceptual
view with short text cards and arrows. Use it to explain the system; use
[Brain overview](../maps/brain-overview.canvas) to navigate its content.

- **CONFIRMED:** External systems remain authoritative; the brain keeps links,
  summaries and verification dates. See [operating rules](../AGENTS.md).
- **CONFIRMED:** Read-only bridges return evidence pending validation; human
  review precedes promotion into durable Markdown. See
  [query workflow](../.github/skills/query_system_of_record.md) and
  [promotion rules](../AGENTS.md#processing-workflow-meetings-and-raw-sources).
- **CONFIRMED:** Meetings and inbox material provide manual entry points;
  recurring logs retain continuity. See [meetings](../01-meetings/README.md).
- **CONFIRMED:** Canvas and role hubs route readers to canonical documents.
  See [view rules](../AGENTS.md#views-maps-are-not-knowledge).
- **PENDING VALIDATION:** Notion, GitHub, Calendar / Artemis, Slack,
  `query_notion_bot` and `ask_artemis` are illustrative examples from the
  user's canvas proposal (2026-09-15), not registered connections. The
  [integration register](../04-architecture/integrations.md) remains pending.
- **CONFIRMED:** Claude / Codex illustrate assisted maintenance, subject to
  the [AI policy](../02-organization/ai-policy.md). Management and Capabilities
  depend on the instance's enabled modules; this template does not enable
  Capabilities. See [configuration](../brain.config.json).

The five zones distinguish sources, query tools, human capture and review,
canonical knowledge, and use. Blue marks external sources; orange marks
bridges and assistants; gray marks raw material and review; green marks
canonical knowledge; purple marks views and use. This is a reading aid over
the rules above, not an automated pipeline.
