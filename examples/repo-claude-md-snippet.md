# Snippet for the organization's code repos

Paste into each code repo's `CLAUDE.md` (and/or `AGENTS.md`), adjusting the
brain folder name. Assumes the sibling layout from `docs/workspace.md`.

```markdown
## Organizational context (company brain)

This repo consumes the organization's company brain, cloned as a sibling
(`../<org>-brain/`). Before working:

- Operating rules (always): @../<org>-brain/AGENTS.md
- AI policy (always): @../<org>-brain/02-organization/ai-policy.md
- Conventions for this work: @../<org>-brain/02-organization/conventions/engineering.md
- For tickets: @../<org>-brain/02-organization/conventions/ticketing.md
- For business logic: @../<org>-brain/05-requirements/business-rules.md
  and @../<org>-brain/00-context/glossary.md

Rules:
- The brain is the source of truth for organizational context. If it
  contradicts this repo, flag it — changes go through PRs to the brain.
- If `../<org>-brain/` does not exist, tell the user to clone it alongside
  this repo (`make workspace` from the brain automates the full layout).
- Load only the sections the task needs (selective injection).
```

> In Claude Code, `@path` imports the file into context. In Codex/OpenCode/
> Copilot the same block works as a reading instruction via file tools.
