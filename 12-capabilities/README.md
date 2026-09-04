# 12-capabilities

Optional module. A **capability** is something the organization (or the
consultancy working with it) can actually do — a technical pattern, a GenAI
use case, an internal accelerator — tracked by maturity, not intention.

Off by default; on by default for the `consulting-company` profile
(`brain.config.json` → `modules.12-capabilities`). Turn it on for any brain
where "what have we actually shipped, versus researched" is a real question.

## Maturity states

| State | Meaning |
|---|---|
| `researched` | Evaluated conceptually or via a spike; not run against real client work |
| `piloted` | Used on at least one real engagement, outcome not yet generalized |
| `proven` | Used repeatedly with a documented, repeatable outcome |

Never claim `proven` for something only `researched` — this is the
distinction that keeps "what GenAI capabilities have we shipped" answerable
without confusing research with delivered experience.

## Contents

- `capability-register.md` — one row per capability, its maturity, evidence,
  and owner.
