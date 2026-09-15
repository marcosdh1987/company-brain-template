# Decision log

> Decisions are **immutable**: to change one, add a new DEC that supersedes
> it. `ACCEPTED` only when evidence records agreement; contractual decisions
> stay `PENDING` until execution is confirmed. Single-repo technical
> decisions belong in that repo's `docs/adr/`, not here.

## DEC-001 — Adopt the company brain

| Field | Value |
|---|---|
| **Date** | _set at bootstrap_ |
| **Status** | ACCEPTED |
| **Context** | The engagement needs a persistent, agent-readable source of truth for context, decisions, and evidence. |
| **Decision** | Use this repository, under the rules in `AGENTS.md`, as the canonical knowledge base for the engagement. |
| **Impact** | All promoted knowledge carries status and source; raw material is evidence only. |
| **Source** | Engagement kickoff |
| **Pending** | — |

## DEC-002 — Rigor follows a work unit's type; tier sets its document set

| Field | Value |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | ACCEPTED |
| **Context** | Tier was carrying two independent questions at once: how many documents a unit holds, and how much traceability each claim owes. In practice they diverge, and both failure modes were observed in a live instance. A one-page client opportunity owes citations on day one, but rigor-by-tier gave it only one way to earn the right to cite — promote to T1/T2 and create mostly-empty files, taxing ceremony to buy traceability. A large internal initiative at T2 owes nothing beyond `owner` and `updated`, yet sat permanently in status-marker debt for claims nobody would audit; a debt counter full of noise is a counter that gets ignored, which costs the whole status vocabulary its force. |
| **Decision** | `tier` sets how many documents a work unit carries. `type` sets the rigor each claim inside it owes, per the matrix in `AGENTS.md` → "Graduated rigor", and only inside `03-work/`. Two floors no type lowers: any claim that feeds `06-decisions/`, `05-requirements/` or a commercial document, or that leaves the organization, carries full rigor regardless of `type` or `tier`; and a unit owner may raise the bar in the unit page's header table, never lower it. |
| **Impact** | A T2 `initiative` no longer owes status markers on every claim — accepted deliberately. The template's original intent survives through the floors: v2.2 defined T2 as client engagements, commercial proposals, and work feeding `06-decisions/`, which are now exactly the floor cases. `notes/` gains light rigor in exchange for never being citable as canonical: a finding must be promoted into a canonical document, with its source, before anything depends on it. No frontmatter or tooling change was required — `type` and `tier` were already mandatory fields. |
| **Source** | Backported from a live instance of this template after ~34 commits of operation; see `docs/superpowers/specs/2026-09-15-instance-backport-design.md` |
| **Pending** | Whether `make validate` should score status-marker debt per `type`, as the source instance does. Not decided here: the check currently reports it for `client` and `opportunity` only. |

---

---

## Entry template (copy below the last entry)

## DEC-00N — <title>

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Status** | PENDING / ACCEPTED / SUPERSEDED by DEC-XXX |
| **Context** | _why this came up_ |
| **Decision** | _what was decided, one affirmative sentence_ |
| **Impact** | _what changes because of it, including at least one cost_ |
| **Source** | _meeting/minute/contract/register link — mandatory_ |
| **Pending** | _what still needs confirmation, if anything_ |
