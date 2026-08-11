# Skills: internal, external, and tool projections

The brain is a repository people and agents work in daily — it deserves a
working harness, without duplicating the engineering one. Three layers:

## 1. Internal lifecycle skills (`.github/skills/`)

Bootstrap, meeting processing, decisions, runbooks, domain updates, quarterly
review. Source of truth: this template; they evolve with its releases.

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

Each projection carries `.generated-manifest.tsv`. Never edit projections by
hand — edit the source (internal file or the harness) and resync. Commit the
projections so teammates and the Claude desktop app get discovery without
running anything.

## Adding an external skill

1. Add its name to `harness.external_skills` in `brain.config.json`.
2. `make sync-skills` — it searches the harness's `.github/skills-external/`,
   `.github/skills/` (flat), and `.claude/skills/`.
3. Commit: `.github/skills-external/`, `skills-lock.json`, and the three
   projections.
