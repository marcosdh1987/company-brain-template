# Adoption: connecting code repos to the brain

Each code repo imports two context layers: the **harness** (via
`template-sync` from the governance template) and this **brain** (referenced
from the repo's adapters). This guide covers the latter. The physical layout
(sibling clones, `make workspace`) is documented in `docs/workspace.md`.

## Option A — Sibling clone (default)

The brain is cloned next to the working repos (the workspace model). In each
code repo's `CLAUDE.md`/`AGENTS.md`, add the block from
`examples/repo-claude-md-snippet.md`. Claude Code resolves `@path` imports;
for Codex/OpenCode/Copilot the same block works as a reading instruction.

Working *inside* the brain, OpenCode is a first-class runtime rather than just
a reader: `OPENCODE.md` is its adapter and `opencode.json` maps the providers.
It uses the same `.env` variable contract as the engineering harness, so a
single `.env` — this repo's, or the harness's, which `make opencode` falls back
to — drives both. Check it with `make opencode-doctor`.

## Option B — CI / remote reference

Where a sibling clone is impossible (CI pipelines, cloud agents): check out
the brain as a second repo, or sync the key files (`AGENTS.md`,
`02-organization/`, the sections the repo needs) into a `context/` folder of
the consuming repo. Less fresh, more portable.

## Rules

1. Repos **read** the brain; changes go through PRs to the brain (with its
   skills), never by editing local copies.
2. Import selectively: `AGENTS.md` + what the repo's domain needs.
3. If the brain contradicts the repo's reality, flag it (`PENDING
   VALIDATION` / conflict note via PR) — never silently "fix" the brain from
   a code repo.

## Per-repo checklist

- [ ] Import block added to `CLAUDE.md` / `AGENTS.md`
- [ ] Repo registered in `04-architecture/repos.yaml` and the systems map
- [ ] Tested: the agent answers a domain/convention question from the brain
- [ ] The team knows how to propose changes to the brain
