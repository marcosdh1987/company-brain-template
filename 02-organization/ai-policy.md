# AI Policy — __ORG_NAME__

| Field | Value |
|---|---|
| Last updated | _PENDING_ |
| Owner | _PENDING_ |
| Status | _PENDING_ |

> The "clear AI stance" (DORA capability #1). Every agent and person using AI
> assistants in this organization operates under these rules. **This file may
> not remain `_PENDING_` after bootstrap.**

## Approved tools

| Tool | Approved use | Via |
|---|---|---|
| _PENDING — e.g. Claude Code_ | assisted development | org gateway |

Rule: **all AI traffic goes through the gateway** (one URL, one token per
person, budgets, content-free usage log). Provider API keys are never pasted
into local tools.

## Data

- **May be sent to cloud models:** _PENDING._
- **May never leave:** secrets, credentials, personal data,
  _PENDING: regulated business data_. For that: self-hosted models via the
  gateway, or prior sanitization.

## Accountability

- AI-generated output is reviewed like (or more than) human output; an agent
  never approves its own PR. Whoever merges owns the change.

## Agents with permissions

- Without a human in the loop: _PENDING — e.g. open PRs, run tests._
- Always with a human: merging to main, deploys, production data, new
  external dependencies/integrations.

## Review

Quarterly (with `quarterly_context_review`) or after an incident; changes are
recorded as decisions.
