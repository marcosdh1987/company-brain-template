---
cssclasses:
  - brain-home
---

# __ORG_NAME__ — Company Brain

The door for a reader. Click a heading to open that part of the brain.

| | | |
|---|---|---|
| **[Context](00-context/company-overview.md)**<br>Who we are, what is in scope, what the words mean | **[Work](03-work/README.md)**<br>Every unit with an owner, a timeline and a deliverable | **[Decisions](06-decisions/decision-log.md)**<br>What was decided, by whom, on what evidence |
| **[Delivery](07-delivery/current-status.md)**<br>Where things stand, what is next, who owns it | **[Meetings](01-meetings/README.md)**<br>Recurring logs and the minutes of one-off sessions | **[Evidence](09-references/README.md)**<br>The primary sources every confirmed fact cites |
| **[Inbox](99-inbox/README.md)**<br>Raw material waiting to be processed | **[Memory](memory/learnings.md)**<br>Lessons and patterns that outlived one project | **[How to use this](START_HERE.md)**<br>For an operator or an agent: rules and workflows |

**Also, depending on your profile:**

[Organization — how we work, conventions, ownership](02-organization/README.md)

[Architecture — systems, repos, integrations](04-architecture/systems-map.md)

[Requirements — validated rules and requirements](05-requirements/functional.md)

[Vendors — the register and evaluations](08-vendors/vendor-register.md)

[Capabilities — what we know how to build](12-capabilities/README.md)

[People — named people and teams](14-people/README.md)

> `make init` removes the entries above for modules your profile turned off. If
> you delete a module later, remove its link too: a dangling Markdown link is a
> hard `make validate` error, unlike a Canvas node, which is only debt.

**Visual maps (Obsidian):** [Home](maps/home.canvas) ·
[Brain overview](maps/brain-overview.canvas) ·
[How the brain works](maps/brain-operating-model.canvas) ·
[Portfolio](maps/portfolio.canvas)

## How to use this brain

- **Navigate by clicking.** Start here or at a hub, follow links down. You
  never need to know the folder layout.
- **Follow the relationships.** Every decision, risk and action links the work
  unit it concerns, so a unit's backlinks answer "what is going on with X".
- **Read the properties.** The table at the top of a document says when it was
  last updated, who owns it, and how far to trust it.
- **Trust the markers.** `CONFIRMED` was validated against a source.
  `PENDING VALIDATION` is plausible and unconfirmed — never act on it as fact.
  `INFERRED` is someone's reasoning. `SUPERSEDED` has been replaced.
  `BLOCKED` must not be acted on. A visible `_PENDING_` gap is deliberate: it
  beats a plausible invention.
- **Editing is safe.** These are plain text files; nothing here is generated
  from a system you might break — except the files that say so at the top.
- **Nothing here is the official corporate record.** The HR system, the tracker,
  the code host and the contract repository remain authoritative. This brain
  stores links, summaries and verification dates, never a copy.

---

Operators and agents: [`START_HERE.md`](START_HERE.md) routes you, and
[`AGENTS.md`](AGENTS.md) holds every operating rule.
