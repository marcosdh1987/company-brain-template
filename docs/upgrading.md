# Upgrading an instance to a newer template release

Every brain is a **fork of the template with shared git history**, never a
photocopy. That single property is what makes an upgrade a merge instead of a
manual port, so it is the one thing not to get wrong when handing the template
to a new team.

## Starting an instance, correctly

```bash
git clone git@<host>:<org>/company-brain-template.git <team>-brain
cd <team>-brain
git remote rename origin upstream          # upstream = the template
git remote add origin git@<host>:<org>/<team>-brain.git
make init ORG="<Team>" PROFILE=<profile>
git add -A && git commit -m "instantiate for <Team>"
git push -u origin main
```

> **Do not use a "Use this template" button, a downloaded archive, or a copy of
> a folder.** Each of those produces a repository with **no shared commit**, and
> from that moment every template improvement has to be ported by hand, forever,
> in both directions. That is not a theoretical cost: this template and its
> first live instance diverged exactly that way, and reconciling them took a
> full working session of manual porting.

## Taking a new release

```bash
git fetch upstream
git merge upstream/main
# resolve conflicts, if any (see below)
make init ORG="<Team>" PROFILE=<profile>   # re-run: new files carry placeholders
make index
make validate
git commit
```

Re-running `make init` is required, not optional: files the release *adds*
arrive with `__ORG_NAME__` unsubstituted, and it also prunes `Home.md` for the
modules your profile has off. It is idempotent and it does not touch your
content.

## What upgrades cleanly, and what does not

The upgrade contract is simple: **the template owns the machinery, the rules and
the templates; your instance owns the content.**

| Owned by the template — take theirs | Owned by you — keep yours |
|---|---|
| `scripts/`, `Makefile` | everything under `03-work/` |
| `AGENTS.md`, `README.md`, `START_HERE.md` | `00-context/`, `05-requirements/`, `07-delivery/` |
| `_templates/`, `01-meetings/minutes/*-template.md` | `01-meetings/` content, `09-references/`, `99-inbox/` |
| `.github/skills/`, `docs/` | your own runbooks, conventions and hubs |
| `CHANGELOG.md` | `brain.config.json` |

Two of those are worth knowing precisely:

- **`AGENTS.md` merges cleanly even when a release rewrites it**, because an
  instance never edits it — `make init` only substitutes the organization name.
  If you need a rule of your own, this is the one file not to edit: put it in
  `02-organization/`, and leave `AGENTS.md` upgradable.
- **`brain.config.json` is yours**, and the template deliberately does not add
  keys to it. Template-level knobs (`work_unit_page`, `fail_on_secrets`) are
  code defaults you may *add* to opt out of — they do not ship in the file,
  precisely so a new knob never becomes a merge conflict in every instance.

## Contributing back

An improvement that is not specific to your team belongs upstream: open a PR
against the template. That is what makes it a shared source of truth instead of
a broadcast. Structural changes — adding or renaming a module — need a decision
recorded first, per `.github/brain-governance.md`.

Content never goes upstream. If a fact is about your team, your clients or your
people, it stays in your instance.
