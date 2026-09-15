# Telemetry (optional, off by default)

The question telemetry answers is narrow and genuinely useful: **which sections
do agents actually read?** Content nobody ever loads is content to merge or
delete, and that is hard to know by intuition.

It is off unless you create it.

## Turning it on

1. Copy `.engobs.toml.example` to `.engobs.toml` and fill in the `_PENDING_`
   values. The file is gitignored on purpose.
2. Stand up your own endpoint. **No endpoint ships with this template**, and
   none should: a template that phones home by default sends one organization's
   usage data to whoever set it up.
3. Record the decision. Enabling telemetry sends data about how this brain is
   used to another system, so it belongs in
   [`06-decisions/decision-log.md`](../06-decisions/decision-log.md) like any
   other decision with an external surface.

## What may be sent

Event counts and timings. Which section was read, how long a run took, how many
files changed.

**Never:** document content, file names that reveal a client or a person, quoted
text, or anything in the restricted categories listed in
[privacy boundaries](privacy-boundaries.md). If your endpoint
cannot guarantee that, do not enable this.

## Turning it off

Delete `.engobs.toml`. There is no other switch, and nothing in `make validate`
depends on it.
