# Snippet for the organization's repos

Paste this block into the `CLAUDE.md` (and/or `AGENTS.md`) of each code repo,
adjusting the path to the brain clone. Assumes Option A of `docs/adoption.md`
(brain cloned as a sibling of the repo).

```markdown
## Organizational context (company brain)

This repo consumes the organization's company brain. Before working:

- Read the index: @../company-brain/brain/00-index.md
- AI policy (always applies): @../company-brain/brain/ai-policy.md
- For business logic: @../company-brain/brain/domain/business-rules.md
  and @../company-brain/brain/glossary.md

Rules:
- The brain is the source of truth for organizational context. If it
  contradicts this repo, flag it — do not edit it from here; changes go
  through PRs to the brain.
- Load only the sections the task needs (selective injection).
```

> Note: in Claude Code, `@path` imports the file into context. In Codex/
> OpenCode/Copilot the same block works as a reading instruction: the agent
> opens the paths with its file tools.
