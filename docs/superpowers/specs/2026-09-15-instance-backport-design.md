# Design: backporting mechanisms from a live instance (v2.3.0)

Author: template maintainer
Date: 2026-09-15
Status: implemented

## Problem

A live instance of this template ran ~34 commits operating a real manager's
brain. In doing so it invented mechanisms the template did not have, and hit
failures the template's machinery did not catch. None of that flowed back: the
instance was seeded by **copying files**, not forking, so the two repositories
share no commit — not one SHA, and not one `patch-id`. There is no merge base,
so every backport is a manual, file-level port and a judgment call.

Meanwhile the template evolved in parallel and grew things the instance lacks
(`make new-view`, the version-drift gate, the inactive-module downgrade for
Canvas nodes, the eight-profile refactor, `SKIP_PREFIXES`). Convergence is
therefore bidirectional, and this release only moves one direction.

## Scope of this release

MINOR. Mechanisms only. No new domain modules, and no contract broken.

## The four contract conflicts, and why none was resolved here

| Conflict | Template | Instance | Decision |
|---|---|---|---|
| Unit page filename | `<unit>/overview.md` | `<unit>/<slug>.md` | Template keeps `overview.md`, behind a single seam (`scripts/_brain.py`: `unit_page()`, config key `work_unit_page`). The instance's shape is better — an editor tab reads the unit's name instead of a wall of identical "overview" tabs, and `[[unit]]` resolves to the page — but `overview.md` is a live tooling contract, hardcoded in the index builder, and renaming it breaks every downstream link. The seam makes the future flip a config edit. |
| Index output | three whole `INDEX.md` files | blocks between `<!-- generated:NAME -->` markers in existing hubs | Template keeps the files. The instance's shape is better product (the reader lands on the hub they know, and hand-written context survives beside the generated table), but its `apply_block()` refuses to *create* markers, so the transition is not self-healing. |
| `_templates/` keying | `03-work/_templates/{t0,t1,t2}` | root `_templates/{t0-initiative,t1-opportunity,t2-client}` | Template keeps its own, and makes it load-bearing: `tier_files()` derives what a tier owes from the folder, so the contract and the templates cannot drift. The instance's keying puts *type* inside the *tier* name, which leaves a tier-2 internal product nowhere to go. |
| Canvas policy | user-owned, never regenerated | two canvases generated, staleness fails validate | Template keeps user-owned. The rule is stated in `AGENTS.md` and the guarantee is published in `CHANGELOG.md` 2.2.0; retracting it is MAJOR by definition, and a config flag does not unsay a changelog. |

## What the next MAJOR owes

1. Flip `work_unit_page` to `""`, ship a one-shot migration (`git mv` plus a
   repo-wide link rewrite), rename the three `_templates/t*/overview.md`.
2. Seed `<!-- generated:… -->` markers into the hubs in the same release that
   deletes the `INDEX.md` files; keep the old paths as stubs for one cycle.
3. Distinguish **user canvases** from **declared generated canvases** in
   config, each generated one carrying a visible "do not edit" node, and only
   then port a canvas generator.

## Deferred, with reasons

- **The `home.canvas` launcher gate.** Not merely unwise — impossible as
  written. The template's shipped `home.canvas` has ten nodes, uses `file`
  nodes, and contains zero launcher markers; the instance's check demands 8–12
  marker cards *and* forbids `file` nodes, so it fails the template's own file
  on two rules at once. It is also a CSS class promoted to a build gate, and it
  would go red the moment a user edits the canvas `AGENTS.md` says they own.
  The pattern is documented in `docs/obsidian.md` as an unvalidated convention.
- **A canvas generator.** See the table above. One insight from it is worth
  keeping even though the code is not: **Obsidian rewrites a canvas's JSON
  layout the moment the file is opened**, so any future generator must compare
  parsed JSON, not bytes, or `--check` will demand a regeneration that changes
  nothing. Recorded in `docs/obsidian.md`.
- **Domain modules** (`10-management/`, `11-ml-governance/`, a people/teams/
  accounts entity layer). Out of scope by decision; their generalizable rules
  were backported instead.
- **An account entity model.** Three good rules — an account is a relationship,
  not a work unit; bench is a capacity state, not an account; assignment to a
  client is not work on a project — govern a concept the template does not
  have. Shipped as one conditional sentence in `14-people/README.md` rather
  than a section.
- **`.base` (Obsidian Bases) views.** Coupled to the unit-page contract the
  template does not have; the instance's view orders by filename, which only
  reads well under `<slug>.md`.
- **Portfolio and review skills** (`update_project_status`, `run_monthly_review`,
  `assess_production_readiness`). Each depends on `07-delivery/` files the
  template does not ship or on a domain module, so porting them would smuggle a
  module in.
- **A hand-maintained anchor index in the decision log.** Safe but wrong: the
  template already *generates* `06-decisions/INDEX.md`, so a second table by
  hand is drift by construction.

## Unresolved tension: where does status live?

The instance's `memory/patterns.md` records a "human-first document shape":
orientation blockquote → human introduction → core content → context map →
**appendix last**, carrying the atomic facts, validation tags and source
registers. It explicitly rejects "at a glance" verification blocks at the top —
which is exactly what this template's `| Field | Value |` header table with a
`Status` row is.

Both positions are defensible. A reader wants the trust signal before the
content; an auditor wants the evidence collected in one place at the end. What
is not defensible is shipping both as rules, so **no rule changed here** and the
header table stands.

Worth noting: the instance does not follow its own pattern — its
`privacy-boundaries.md` and `automation-map.md` both open with header tables —
which suggests the pattern is aspirational rather than operating. The question
for a future release: *does status live in a header table a reader hits first,
or in an appendix an auditor hits last?*

## Verification

Eight mechanism tests (T1–T8) plus the regression suite; three prose scenarios
(rigor by type, bitácora continuity, privacy refusal) run against a scratch
brain instantiated with `make init`. See the release's plan document.

## Known risk

`AGENTS.md` grew from 7.8 KB to ~17 KB in this release. `LOCAL_AGENT.md` targets
32 k-context local models, and a single rule file at this size is near the limit
of being held reliably alongside a task. Keep the routing table a router, not a
description. If a local model starts missing the rigor matrix or the bitácora
exemption, that is the first thing to cut back.
