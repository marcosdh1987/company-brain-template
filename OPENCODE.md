# OpenCode Adapter — Company Brain

All operating rules for this repository live in **`AGENTS.md`** — read it
first and follow it. Do not maintain rules here; this file exists only so
OpenCode finds its entry point, its skills, and the runtime it runs on.

## Skills

Each skill exposes a `SKILL.md` with purpose, required input, output format, and
execution rules. When a task matches a skill, read its `SKILL.md` before acting.

<!-- BEGIN GENERATED SKILLS (managed by scripts/sync_skills.py; do not edit) -->
The governed skills below are projected into `.opencode/skills/`. Internal skills are the source of truth and take precedence over external synced skills on name conflicts.

**Internal skills:**

- `add_runbook` — Use when a procedure was explained ad-hoc for the second time — converts it into a runbook with verification and rollback. Org-level procedures go to 02-organization/runbooks/, work-unit-specific ones to the work unit folder.
- `bootstrap_company_brain` — Use when instantiating the company-brain template for an organization — fresh start or migration of an org with existing history. Guides profile selection, source mining, interviews, and initial promotion, replacing _PENDING_ placeholders only with verified, cited content.
- `process_meeting` — Use after a meeting — takes a transcript or raw notes from 01-meetings/transcripts/ or 99-inbox/ and produces reviewed minutes plus fully promoted knowledge (decisions, requirements, questions, risks, actions), leaving the source marked processed.
- `quarterly_context_review` — Use every ~90 days (or after major changes) to fight drift — audits canonical content against reality, marks SUPERSEDED/PENDING VALIDATION where the world moved, measures debt, and reports brain health to the owners.
- `query_system_of_record` — Use when a task needs current content from an external system of record (wiki, tracker, CRM, HR system) reachable through a local read-only bridge — fetches the answer, marks it PENDING VALIDATION with a dated citation and its read scope, and never promotes it on its own. Register the bridge in 04-architecture/integrations.md before first use.
- `record_decision` — Use when a decision was made (or proposed) that affects the engagement — records it as an immutable DEC entry in the decision log with mandatory source, handling supersession and status correctly.
- `update_domain_context` — Use when the business changed — entity, rule, integration, vocabulary or scope — and the brain must absorb it without drifting - locates every affected section, updates them consistently with status and source.

**External synced skills:**

- `brainstorm_quick` — Use for fast ideation on a scoped feature when no written spec or formal approval is needed — diverge on options, weigh trade-offs, converge on a recommendation, then hand off to `plan_and_execute_feature`. For new features or design-impacting work that needs a written, user-approved spec, use the external `brainstorming` skill (full design gate) instead.
- `brainstorming` — You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- `research_current_info` — Use when the user asks for up-to-date or current information, to confirm something is still accurate, or when a task depends on facts that may have changed since training (library versions, APIs, pricing, releases, news, current best practices). Runs a governed web search with a curated domain allow/deny policy and cited, recency-checked results.
- `retrospective` — Use at the end of a unit of work to capture durable, non-obvious knowledge into project memory (memory/) and flag decisions worth an ADR. Turns one-off discoveries into compounding, persistent context.
- `writing-clearly-and-concisely` — Apply Strunk's timeless writing rules to ANY prose humans will read—documentation, commit messages, error messages, explanations, reports, or UI text. Makes your writing clearer, stronger, and more professional.
- `writing-plans` — Use when you have a spec or requirements for a multi-step task, before touching code

Refresh this layout with `make sync-skills`.
<!-- END GENERATED SKILLS -->

## Runtime rules (brain-specific, not a second rule set)

- This repository is markdown, not code. The only gate is `make validate`; it
  must pass before any work is called done. There is no linter or test suite.
- Run `make index` after adding or retyping a work unit in `03-work/`;
  `make validate` fails on a stale index.
- **Every operating rule lives in `AGENTS.md`** — the status vocabulary, the
  evidence rule, decision immutability, the language rule and the privacy
  boundary included. Read it; do not restate it here. A rule that exists in two
  files is a rule that will disagree with itself.
- Never commit. The owner makes every commit; report the changed files instead.

## Models and providers

Provider/model config is env-driven in `opencode.json` (`{env:...}`): a LiteLLM
`gateway`, `nvidia` NIM, and self-hosted `ollama` / `lmstudio` — the same
contract as the engineering harness (`ml-python-base`), so one `.env` serves
both repos. Copy `.env.example` to `.env` (or let `make opencode` fall back to
`../ml-python-base/.env`), check endpoints with `make opencode-doctor`, and
launch with `make opencode`. On a small self-hosted model, `LOCAL_AGENT.md`
applies.
