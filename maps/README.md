# maps/ — visual views

This folder is an optional **presentation layer**, mainly for
[Obsidian](https://obsidian.md). It holds `.canvas` files: visual,
clickable maps over the knowledge that already lives in this repo's
Markdown.

**Knowledge != Views.** The facts live in Markdown + frontmatter +
wikilinks. A Canvas is a navigable arrangement of links to that
knowledge — never a second place a fact can live. If every file in this
folder vanished, nothing in the brain would be lost; you'd just be back
to browsing folders. See `AGENTS.md`'s "Views (`maps/`) are not
knowledge" section for the full rule set.

## What's here

| View | Purpose | Most useful for |
|---|---|---|
| `home.canvas` | Launcher — one card per major section, pointing at its real hub file | every profile |
| `brain-overview.canvas` | Content navigation across evidence and canonical sections | `full` |
| `brain-operating-model.canvas` | Conceptual sources → bridges → human review → knowledge → use | every profile |
| `portfolio.canvas` | Work units, delivery status, roadmap, vendors | `consulting`, `consulting-company`, `delivery-oversight`, `client-engagement` |
| `management.canvas` | Team → person → client/project/meeting navigation | `team`, `engineering-management`, `consulting-company` |
| `architecture-capabilities.canvas` | Systems, repos, integrations, and shipped capabilities | `development`, `engineering-management`, `consulting-company` |

All six ship in every brain regardless of profile — the "most useful
for" column is a suggestion, not an enforced rule. If a card points at a
module your profile left inactive, the linked file still exists (module
folders are never deleted automatically); delete the card, or the whole
canvas, if you don't want it. This mirrors how any other optional
module's folder can be deleted once a profile turns it off.

## Editing is expected

**Feel free to duplicate, rearrange, simplify, or create new Canvas
views.** Different people can have different maps over the exact same
knowledge — that's a feature. Two conventions keep this simple:

- A tracked, team-shared view is a normal `maps/*.canvas` file, committed
  like any other doc.
- A personal view — yours alone, not meant for the team — is named
  `maps/*.local.canvas`. It's gitignored, so it never needs a commit or a
  review.

Example: `maps/management.canvas` (shared) next to
`maps/management-marcos.local.canvas` (personal layout, same underlying
files).

## Creating a new view

```bash
make new-view NAME=my-view   # creates maps/my-view.canvas (blank)
```

This refuses to run if `maps/my-view.canvas` already exists — it never
overwrites a view you've already started editing.

## What never touches these files

`make validate` and `make index` only ever **read** `maps/*.canvas` (to
check it's valid JSON and that file-node links resolve) — they never
write to it. `make init` doesn't open `.canvas` files at all. The only
commands that create or write a Canvas are the one-time template
checkout and `make new-view` above. Once a Canvas exists, it's yours.

## Related

- `docs/obsidian.md` — opening this repo as a Vault, Graph, Backlinks,
  Properties.
- `AGENTS.md` — the architectural rules for views vs. knowledge.
