# The workspace model: brain + code repos

How a company brain coexists with the organization's code repositories. Short
version: **hub-and-spoke with sibling clones — never submodules, never nested.**

## The layout

Everyone (humans and agents) uses the same convention: one folder per
client/organization, with the brain and every code repo cloned **side by
side**:

```text
~/work/acme/                 ← any folder on the developer's machine
├── acme-brain/              ← the hub (instance of this template)
├── api-payments/            ← spoke: a normal, independent git repo
└── web-portal/              ← spoke: same
```

Nothing is nested. There is **no git link** between the repos — the link is a
folder convention plus one text file: `04-architecture/repos.yaml`, the
machine-readable registry of the organization's repos.

## A developer's day 1

```bash
git clone git@github.com:acme/acme-brain.git
cd acme-brain
make workspace        # reads repos.yaml, clones every repo as a sibling
```

Three repos or fifteen: one command. From then on the developer works
**inside a code repo**, never inside the brain — they open `api-payments/`
with their editor and agent, and that repo's `CLAUDE.md`/`AGENTS.md` contains
the import block (see `examples/repo-claude-md-snippet.md`):

```markdown
- Read the operating rules first: @../acme-brain/AGENTS.md
- AI policy (always applies): @../acme-brain/02-organization/ai-policy.md
```

The sibling convention is what makes the relative path `../acme-brain/`
predictable on every machine with zero per-person configuration.

## Why not submodules

Making code repos submodules of the brain (or the brain a submodule of each
repo) looks tidy and fails in practice:

1. **A submodule pins a commit.** The brain would reference stale versions of
   every repo by design — structural drift, the exact thing a brain exists to
   prevent. With siblings, `git pull` in the brain refreshes context and
   `git pull` in a repo refreshes code, independently.
2. **Operational friction.** Heavy clones, per-repo permissions (people who
   read the brain must not necessarily clone all code), and the
   `git submodule update` dance nobody performs.
3. **It inverts the dependency.** Context must not depend on code; code
   consumes context. `repos.yaml` gives the one benefit submodules promised —
   one-command workspace assembly — with none of the coupling.

## Degradation and CI

- **Repo cloned without the brain:** the `@../acme-brain/…` imports simply do
  not resolve; the agent works without organizational context. It degrades,
  it does not break — the snippet tells the agent to ask the user to clone
  the brain alongside.
- **CI / cloud agents** (no sibling folder): check out the brain as a second
  repository in the pipeline, or sync the key files into a `context/` folder
  of the consuming repo. Same content, different delivery
  (see `docs/adoption.md`, option B).
- **Brain-only users** (a stakeholder reading decisions): the brain is
  self-contained; nothing requires the code repos to exist locally.

## Rules of the road

1. Code repos **read** the brain; changes to the brain go through PRs to the
   brain — never by editing an imported copy.
2. The brain never contains code, and `outputs/` style artifacts only enter
   `09-references/` as registered evidence.
3. Each repo's adapter imports `AGENTS.md` plus only the sections its work
   needs (selective injection).
4. New repo in the org → new entry in `repos.yaml` + a row in the systems
   map. That is the whole registration ceremony.
