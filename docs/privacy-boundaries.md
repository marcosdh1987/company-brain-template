# Privacy Boundaries

| Field | Value |
|---|---|
| Last updated | _PENDING_ |
| Owner | _PENDING_ |
| Status | _PENDING_ |

> This repository is a knowledge base, not an HR, performance,
> applicant-tracking, or personnel system. These boundaries are mandatory, and
> they do not depend on which modules are active.

This file is the **single place** the lists below are written down. Every other
document names the category and links here — see [`AGENTS.md`](../AGENTS.md)
for the rule itself.

It lives in `docs/` on purpose: `docs/` is not a module, so no profile can turn
it off. A boundary that disappears when someone deselects a module is not a
boundary.

## This repository must not store

- Individual performance ratings, written evaluations, or assessment outcomes.
- Compensation, salary, bonus, equity, offers, or counteroffers.
- Medical, disability, parental-leave, immigration, or visa information.
- Disciplinary actions, formal warnings, or investigation records.
- Identifiable confidential feedback or confidential one-on-one notes.
- Candidate identities, contact details, interview notes, scores, rejection
  reasons, or background checks.
- Personal contact information beyond an approved public or operational reference.
- Credentials, passwords, API keys, MFA seeds, or private keys — reference where
  a secret lives, never its value.
- Any material that could become an unauthorized personnel record.

## This repository may store

- Non-sensitive operational commitments and their owners.
- Team structure, and role or capacity signals **in aggregate**.
- Hiring, onboarding, assessment, and performance *process* descriptions.
- Meeting decisions, risks, and action items that contain no restricted people data.
- Links and references to official corporate systems, with a verification date.
- **Named person entities**, if the `14-people` module is active, limited to
  exactly this allowlist:

  > name · role · team · specialty · public or professional location ·
  > tenure · current assignment

  A person page must never carry a formal HR job title, compensation,
  performance content, or any field that is not on this list. Adding a field to
  the allowlist is a decision: record it in
  [`06-decisions/decision-log.md`](../06-decisions/decision-log.md) with its
  source, and amend this list — never widen it in place in a person page.

## Corporate-system redirects

Restricted data has a home, and it is not here. Record where it goes; do not
name a system you have not verified.

| Data | Corporate destination | Owner | Status |
|---|---|---|---|
| Employee profile, leave, and HR records | _PENDING_ | _PENDING_ | PENDING VALIDATION — system name intentionally not assumed |
| Performance reviews and manager assessments | _PENDING_ | _PENDING_ | PENDING VALIDATION — system name intentionally not assumed |
| Compensation and disciplinary records | _PENDING_ | _PENDING_ | PENDING VALIDATION — system name intentionally not assumed |
| Candidate records and interview feedback | _PENDING_ | _PENDING_ | PENDING VALIDATION — system name intentionally not assumed |
| Confidential one-on-one content | Approved private manager or HR mechanism | _PENDING_ | PENDING VALIDATION — never this repository |

`PENDING VALIDATION — system name intentionally not assumed` is the point of
this table, not a gap in it. "We do not know which system owns this yet" is a
recorded state; guessing a vendor name is an invented fact that someone will
later act on.

## Safe reference pattern

Store the minimum needed to *find* an official record, never the record:

```text
Record type: <category>
System:      <corporate system, or "pending validation">
Owner:       <role>
Period:      YYYY-HN
```

Do not copy the record's content, rating, or outcome.

## Agents

An agent working in this repository **refuses** to store or process excluded
data. If a task arrives carrying restricted content, it preserves only an
approved system reference in the shape above and asks the human owner to handle
the source in the corporate system. It does not summarise the restricted part
"just this once", and it does not put it in a commit message either.

Which AI providers may see this brain's content at all is governed by
the AI and data policy (`02-organization/ai-policy.md`, if that module is active). Authorization for one analysis does not
establish organization-wide approval.

---

[← Home](../Home.md)
