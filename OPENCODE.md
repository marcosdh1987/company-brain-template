# OpenCode Adapter — Company Brain

All operating rules for this repository live in **`AGENTS.md`** — read it
first and follow it. Do not maintain rules here; this file exists only so
OpenCode finds its entry point, its skills, and the runtime it runs on.

## Skills

Each skill exposes a `SKILL.md` with purpose, required input, output format, and
execution rules. When a task matches a skill, read its `SKILL.md` before acting.

<!-- BEGIN GENERATED SKILLS (managed by scripts/sync_skills.py; do not edit) -->
_Not generated yet — run `make sync-skills` to fill this block with the skills
projected into `.opencode/skills/`._
<!-- END GENERATED SKILLS -->

## Runtime rules (brain-specific, not a second rule set)

- This repository is markdown, not code. The only gate is `make validate`; it
  must pass before any work is called done. There is no linter or test suite.
- Run `make index` after adding or retyping a work unit in `03-work/`;
  `make validate` fails on a stale index.
- Never invent business or technical facts. A `_PENDING_` placeholder with an
  owner beats a plausible guess. Mark every non-obvious claim with the status
  vocabulary from `AGENTS.md`.
- Raw material in `99-inbox/` and `01-meetings/transcripts/` is evidence, not
  validated fact. Promote it through the workflow in `AGENTS.md`, with a source.
- Decisions are immutable: record new ones with the `record_decision` skill,
  never edit an existing `DEC-XXX`.
- Work-unit content stays in `03-work/<unit>/`; cross-cutting content in the
  shared sections.
- Never store credentials, keys or unnecessary personal data — reference where a
  secret lives, never its value.
- Interact in the same language as the user; keep document content in the
  language the document already uses.
- Never commit. The owner makes every commit; report the changed files instead.

## Models and providers

Provider/model config is env-driven in `opencode.json` (`{env:...}`): a LiteLLM
`gateway`, `nvidia` NIM, and self-hosted `ollama` / `lmstudio` — the same
contract as the engineering harness (`ml-python-base`), so one `.env` serves
both repos. Copy `.env.example` to `.env` (or let `make opencode` fall back to
`../ml-python-base/.env`), check endpoints with `make opencode-doctor`, and
launch with `make opencode`. On a small self-hosted model, `LOCAL_AGENT.md`
applies.
