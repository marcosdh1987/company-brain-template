# Skills in this repository

Governed skills for creating and maintaining a company brain. Same format as
the harness skills (`ml-python-base`); meant to be distributed with it.

## Where a skill lives

A skill is either only prose, or prose plus the files it runs. Both belong in
`.github/skills/`; the shape decides the layout.

| The skill is… | It goes in |
|---|---|
| A single `.md`, no helper files | `.github/skills/<name>.md` |
| Prose plus scripts, templates or references | `.github/skills/<name>/SKILL.md` with the helpers beside it |

A folder needs `SKILL.md` as its entry point. Without it the folder is not a
skill: `make sync-skills` reports it and skips it, so you find out at sync time
instead of when the skill silently never triggers. Executable bits on bundled
scripts survive the projection, so a `.sh` copied into the native folders stays
runnable.

`.github/skills-external/` is a different thing: it holds skills synced **from
the harness**, listed in `harness.external_skills` in `brain.config.json`. Every
sync overwrites those from `ml-python-base`. Do not author there, and do not add
a name to that list unless the skill really comes from the harness.

One portability note: the harness itself still takes only flat `.md` files in its
own `.github/skills/`. If you ever want to contribute a folder skill upstream to
`ml-python-base`, it has to land in that repo's `skills-external/` instead.

## Adding a skill, step by step

1. **Put the file where its shape belongs**, per the table above. Name the file
   or folder in `snake_case`; that name is what the skill will be called. It comes
   from the filename or folder name, not from the frontmatter.

2. **Write the YAML frontmatter** at the top of the `.md` (or of `SKILL.md`).
   Both shapes need it:

   ```yaml
   ---
   name: my_skill
   description: One line saying when to use it. This is the trigger text an agent reads to decide.
   ---
   ```

   Keep `name` equal to the filename without `.md`. The `description` is what
   lands in the generated block of `OPENCODE.md`, so write it as a trigger, not
   as a title.

3. **Fix every relative link.** `make validate` resolves links in each `.md` of
   the repo, and the skill gets copied into four native folders, so one broken
   link becomes five errors. Links must resolve from the skill file's own
   location. A skill copied from another repo usually points at paths that do
   not exist here.

   For a bundled script, tell the agent to call it by its **governed** path
   (`.github/skills/<name>/<script>`), not by the native copy. The projections
   are copies, not symlinks, and each sync rebuilds them, so an edit made to a
   copy is lost.

4. **Run the sync.**

   ```bash
   make sync-skills
   ```

   It copies the skill into `.claude/skills/`, `.codex/skills/`, `.agents/skills/`
   and `.opencode/skills/`, and rewrites the generated skills block in
   `OPENCODE.md`. Check the printed count went up by one, and read any `WARNING`.

5. **Add a row to the table below.** It is the index for humans; nothing
   generates it.

6. **Run the gate.**

   ```bash
   make validate
   ```

7. **If the skill should be discoverable per task**, add a row to the
   "What to read per task" table in `AGENTS.md`.

Never edit the four projections or their `.generated-manifest.tsv` by hand: every
sync deletes and rebuilds them.

## Available skills

| Skill | When to use it |
|---|---|
| `add_runbook` | Turn a twice-explained procedure into a runbook |
| `bootstrap_company_brain` | Instantiate and populate the brain (fresh org, or migration mode for an org with history) |
| `process_meeting` | Turn a transcript into minutes + promoted knowledge |
| `quarterly_context_review` | Quarterly anti-drift audit |
| `record_decision` | Record a decision as a DEC entry |
| `update_domain_context` | Absorb a business change consistently |
