# Skills: internal, external, and tool projections

The brain is a repository people and agents work in daily — it deserves a
working harness, without duplicating the engineering one. Three layers:

## 1. Internal lifecycle skills (`.github/skills/`)

Bootstrap, meeting processing, decisions, runbooks, domain updates, quarterly
review. Source of truth: this template; they evolve with its releases.

An internal skill takes either of two shapes:

| The skill is… | It goes in |
|---|---|
| A single `.md`, no helper files | `.github/skills/<name>.md` |
| Prose plus scripts, templates or references | `.github/skills/<name>/SKILL.md` with the helpers beside it |

The folder shape is what lets a skill ship the thing it runs — a shell script,
a query template, a reference document — instead of describing it in prose and
hoping the agent reconstructs it. A folder without `SKILL.md` is not a skill:
`make sync-skills` reports it and skips it. Executable bits survive the
projection, so a bundled `.sh` stays runnable in every tool's view. Full
authoring procedure: [`.github/skills/README.md`](../.github/skills/README.md).

## 2. External working skills (`.github/skills-external/`)

Non-code skills synced from the engineering harness (`ml-python-base`) —
ideation, planning, research, writing, retrospectives. Declared in
`brain.config.json`:

```json
"harness": {
  "source": "../ml-python-base",
  "external_skills": ["brainstorming", "brainstorm_quick", "writing-plans",
                      "writing-clearly-and-concisely", "research_current_info",
                      "retrospective"]
}
```

`make sync-skills` copies them from the harness (sibling clone by default —
the workspace layout — or any local path) and records a sha256 per skill in
`skills-lock.json`. **This is sync, not copy-paste**: the harness stays the
source of truth; an improvement measured in the lab reaches every brain by
re-running the sync. Code-oriented skills (debugging, refactoring, TDD) stay
in code repos — they have no business here.

## 3. Native tool projections (generated)

Skills are only useful if the tool discovers them. The same command
regenerates:

| Tool | Layout |
|---|---|
| Claude Code / Claude app | `.claude/skills/<name>/SKILL.md` |
| Codex | `.codex/skills/<name>/SKILL.md` (+ reads `AGENTS.md` natively) |
| Antigravity | `.agents/skills/<name>/SKILL.md` + `.agents/rules/brain-rules.md` → AGENTS.md |
| OpenCode | `.opencode/skills/<name>/SKILL.md` + the generated block in `OPENCODE.md` |

Each projection carries `.generated-manifest.tsv`. Never edit projections by
hand — edit the source (internal file or the harness) and resync. Commit the
projections so teammates and the Claude desktop app get discovery without
running anything. `OPENCODE.md` is not a projection but it does carry a
generated section: the sync rewrites the skill list between its
`BEGIN/END GENERATED SKILLS` sentinels, so keep those two comments in place.

## Adding an external skill

1. Add its name to `harness.external_skills` in `brain.config.json`.
2. `make sync-skills` — it searches the harness's `.github/skills-external/`,
   `.github/skills/` (flat), and `.claude/skills/`.
3. Commit: `.github/skills-external/`, `skills-lock.json`, and the three
   projections.

## Adding an internal skill

1. Choose the shape: a flat `<name>.md` for prose only, a `<name>/SKILL.md`
   folder when the skill ships scripts, templates or references.
2. Write the YAML frontmatter (`name`, `description`). The `description` is the
   trigger text an agent reads to decide, and it is what lands in the generated
   block of `OPENCODE.md`.
3. `make sync-skills`, then `make validate`.
4. Commit: the source under `.github/skills/`, the four projections, and
   `OPENCODE.md`.

Step-by-step version, including the relative-link and governed-path rules:
[`.github/skills/README.md`](../.github/skills/README.md).
