# AI Policy — __ORG_NAME__

> The "clear AI stance" (capability #1 of the DORA model): what is allowed, what
> is not, and with which safeguards. Every agent and every person using AI
> assistants in the organization operates under these rules. Owner: _PENDING_.

## Approved tools

| Tool | Approved use | Via |
|---|---|---|
| _PENDING — e.g. Claude Code_ | assisted development | org gateway |
| _PENDING — e.g. self-hosted models_ | sensitive code / experimentation | org gateway |

Rule: **all AI traffic goes through the gateway** (one URL, one token per person,
budgets and a content-free usage log). Provider API keys are never pasted into
local tools.

## Data

- **May be sent to cloud models:** _PENDING — e.g. non-sensitive code, public
  documentation._
- **May never leave:** secrets, credentials, customer personal data,
  _PENDING: add what is regulated for this business_. To work on that:
  self-hosted models via the gateway, or prior abstraction/sanitization.

## Accountability for output

- AI-generated code is reviewed the same as (or more than) human code: the
  harness gates are mandatory and an agent does not approve its own PR.
- Whoever merges owns the change, whether a person or an agent wrote it.

## Agents with permissions

- What an agent may do without a human in the loop: _PENDING — e.g. open PRs,
  run tests._
- What always requires a human: merging to main, deploys, touching production
  data, adding new external dependencies/integrations.

## Reviewing this policy

- Reviewed quarterly in the context review (see the template's
  `docs/maintenance.md`) or after an incident. Changes are recorded as ADRs.
