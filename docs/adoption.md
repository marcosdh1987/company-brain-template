# Adoption: connecting the organization's repos to the brain

Each code repo imports two context layers: the **harness** (arrives via
`template-sync` from the governance template) and this **brain** (referenced
from the repo's adapters). This guide covers the latter.

## Option A — Submodule or sibling clone (recommended)

The brain is cloned next to the working repos (or as a submodule), and the
adapters reference it with relative paths:

```text
~/work/
├── company-brain/          # clone of the brain instance
├── payments-service/       # code repo
└── frontend-app/           # code repo
```

In the code repo's `CLAUDE.md`, add the block from
`examples/repo-claude-md-snippet.md`. Claude Code resolves imports with
`@path`; for other tools (Codex, OpenCode, Copilot) the same block works as a
reading instruction in `AGENTS.md`.

## Option B — Remote reference only

If the brain cannot be cloned locally (e.g. agents in CI), the adapters
reference the repo URL and the key files are synced into a `context/` folder of
the consuming repo in CI. Less fresh, more portable.

## Rules

1. Repos **read** the brain; changes to the brain go through PRs to the brain
   (with its skills), never by editing local copies.
2. Each repo's adapter declares which sections it imports — typically
   `00-index.md` plus what its domain needs. Avoid importing everything.
3. If an agent detects that the brain contradicts the repo's reality, it does
   not silently "fix" it: it marks `_STALE_` via a PR to the brain or notifies
   the section owner.

## Per-repo checklist

- [ ] Brain block added to `CLAUDE.md` / `AGENTS.md`
- [ ] Tested: the agent correctly answers a domain question that previously
      required manual explanation
- [ ] The team knows the brain exists and how to propose changes to it
