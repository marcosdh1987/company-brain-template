# Automation Map

| Field | Value |
|---|---|
| Last reviewed | _PENDING_ |
| Owner | _PENDING_ |
| Status | _PENDING_ |

> This map limits an automated update to **one knowledge zone at a time**, and
> it never authorizes a write to a corporate system. Every automation reads
> [`AGENTS.md`](../AGENTS.md) and [`ai-policy.md`](ai-policy.md) before
> processing anything that came from outside this repository.

The point of a zone is the **Forbidden** row. An agent that can write anywhere
will eventually write the right fact into the wrong file, where nobody
maintaining that file expects to find it.

Add a zone when a new class of automated update appears; keep the row set
identical across zones, so the contract reads the same everywhere.

## Common update contract

Every automated update must:

1. Read the mandatory files for its zone.
2. Register or cite its evidence in `09-references/`.
3. Check privacy and information status before writing.
4. Update the canonical file **before** any hub or index summary.
5. Record a conflict instead of overwriting it.
6. Run `make validate` after canonical or structural changes.
7. Leave external corporate systems unchanged without documented human approval.

## Zone — Company context

| Field | Value |
|---|---|
| Purpose | Maintain durable business, organization, vocabulary and working-model context |
| Allowed targets | `00-context/`, `02-organization/ways-of-working.md` |
| Read first | `AGENTS.md`, `ai-policy.md`, `docs/privacy-boundaries.md`, the source register, every affected canonical file |
| Corporate sources | Approved corporate documentation and named corporate owners |
| Operational owner | _PENDING_ |
| Validation owner | _PENDING_ — depends on the claim |
| Trigger examples | A reviewed company document, an approved organization change, a validated glossary term |
| Required checks | Status marker, source citation, `make validate` |
| **Forbidden** | Restricted personal data; changing scope or a commitment without an approved source |

## Zone — Work units

| Field | Value |
|---|---|
| Purpose | Keep each work unit's canonical documents current |
| Allowed targets | `03-work/<unit>/` |
| Read first | `AGENTS.md` (graduated rigor), `03-work/README.md`, the unit's own documents |
| Corporate sources | The tracker, the code host, client correspondence |
| Operational owner | The unit's `owner` |
| Validation owner | _PENDING_ — the client or internal sponsor |
| Trigger examples | A processed meeting, a status change, a new risk |
| Required checks | Rigor owed by the unit's `type`, `make index`, `make validate` |
| **Forbidden** | Editing another unit; promoting a `notes/` finding without a source; lowering a tier |

## Zone — Delivery and portfolio

| Field | Value |
|---|---|
| Purpose | Keep status, risks and action items answerable without reading history |
| Allowed targets | `07-delivery/` |
| Read first | `AGENTS.md`, the affected unit's documents |
| Corporate sources | The tracker |
| Operational owner | _PENDING_ |
| Validation owner | _PENDING_ |
| Trigger examples | A processed meeting, a review, a slipped milestone |
| Required checks | Every row links the unit it concerns; `make validate` |
| **Forbidden** | Inventing a status that no unit document supports; silently closing an open item |

## Zone — Organization and conventions

| Field | Value |
|---|---|
| Purpose | Record how the organization works and who owns what |
| Allowed targets | `02-organization/` |
| Read first | `AGENTS.md`, `ai-policy.md`, `docs/privacy-boundaries.md` |
| Corporate sources | Approved policy, named corporate owners |
| Operational owner | _PENDING_ |
| Validation owner | _PENDING_ |
| Trigger examples | A ratified convention, a new runbook, an ownership change |
| Required checks | Source citation, `make validate` |
| **Forbidden** | Growing a second rule set — operating rules live only in `AGENTS.md`; any restricted personal data |

## Zone — Evidence intake

| Field | Value |
|---|---|
| Purpose | Turn raw material into cited, status-marked knowledge |
| Allowed targets | `99-inbox/`, `01-meetings/`, `09-references/` |
| Read first | `AGENTS.md` (processing workflow), `99-inbox/README.md`, `docs/privacy-boundaries.md` |
| Corporate sources | Transcripts, email, exports — as evidence, never as fact |
| Operational owner | _PENDING_ |
| Validation owner | _PENDING_ |
| Trigger examples | A new transcript, a forwarded document, a vendor response |
| Required checks | Source register entry, `processed--` rename, `make validate` |
| **Forbidden** | Editing a transcript; promoting evidence to `CONFIRMED` without validation; storing a restricted category |

---

Hub and index pages are updated **after** the canonical file they summarise,
never instead of it. A hub is a router; it is never the place a fact first
appears.

[← Organization](README.md) · [Home](../Home.md)
