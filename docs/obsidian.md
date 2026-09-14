# Using this brain in Obsidian

This brain works with no `.obsidian/` folder at all — nothing here
requires Obsidian. If you'd rather browse visually than by path, this
page is the on-ramp.

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
`portfolio`, `management`, `architecture-capabilities`) — see
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
