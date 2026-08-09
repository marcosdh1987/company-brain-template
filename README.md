# Company Brain Template

Template for instantiating an organization's **company brain**: the source of
truth for its context — domain, decisions, glossary, conventions, systems map,
and runbooks — structured to be read by AI agents and by people.

It is the **context** layer that complements the **execution** layer (the
engineering harness, [`ml-python-base`](https://github.com/marcosdh1987/ml-python-base)).
The organization's code repositories import both from their adapters:

```text
shared harness (template releases)             ← how work is done (engine, ours)
        +
the organization's company brain (this repo)   ← what the org knows (context, theirs)
        =
effective context of every repo (CLAUDE.md / AGENTS.md point at both)
```

The separation is deliberate: the engine is reused across organizations and
updated through releases; the brain is owned by each organization and evolves
with its business. Everything is versioned Markdown in git — no lock-in.

## When to use it (and when not to)

**This template is the *second* repo's step, not the first one's.** A single-repo
engagement does not need a separate brain: the project brain lives inside the
repo, in the containers the harness already ships (`memory/`, `docs/adr/`,
`.github/domain-boundaries.md`). Instantiating this template there is overhead.

The right trigger is observable: **a second repo of the same project/client
starts duplicating context** (glossary, business rules, conventions). That day,
the shared part is *moved* (not copied) here and both repos point at it. The
guide documents this step by step in "Adopting the Harness in an Existing
Project".

## Quick start

```bash
# 1. Instantiate for an organization
make init ORG="Acme Inc."

# 2. Populate the brain with the bootstrap skill (from your AI assistant)
#    → .github/skills/bootstrap_company_brain.md
#    Mine repos/docs first, interview second, invent nothing.

# 3. Validate
make validate

# 4. Connect the organization's repositories
#    → docs/adoption.md (ready-to-paste snippet in examples/repo-claude-md-snippet.md)
```

## Structure

```text
brain/
├── 00-index.md          # entry point: what to read per task
├── ai-policy.md         # the org's AI posture (mandatory, never left pending)
├── glossary.md          # canonical business vocabulary
├── domain/              # overview, entities, business rules, stakeholders
├── decisions/           # org-level ADRs (single-repo ADRs stay in that repo)
├── conventions/         # engineering, git, communication — the cross-cutting part
├── architecture/        # systems map and external integrations
├── runbooks/            # executable operational procedures
└── team/                # ownership: everything has a human owner
memory/                  # org-level learnings and patterns
docs/                    # repo adoption and anti-drift maintenance
.github/skills/          # brain bootstrap and maintenance (harness skill format)
scripts/ + Makefile      # init, structure/link validation, stats
```

## Principles

1. **Stale context is worse than missing context** — `_PENDING_` markers are
   visible debt, not shame; the quarterly review reduces them.
2. **Everything has a human owner** — no owner in `team/ownership.md`, no entry.
3. **Selective injection** — agents read `brain/00-index.md` and load only what
   the task needs; never "the whole brain".
4. **Nothing sensitive** — no secrets or personal data: agents read this.

## Commands

| Command | What it does |
|---|---|
| `make init ORG="…"` | Instantiates the template for an organization |
| `make validate` | Complete structure, healthy links, `_PENDING_` debt report |
| `make stats` | Content size per section |

## Maintenance

Anti-drift is a process, not a hope: the `quarterly_context_review` skill every
~90 days + per-section owners + `make validate` in CI. Details in
[`docs/maintenance.md`](docs/maintenance.md).
