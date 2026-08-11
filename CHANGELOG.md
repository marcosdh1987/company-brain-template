# Changelog

Semver by tags (`vX.Y.Z`). `MINOR` = new sections/templates; `PATCH` = content
fixes; `MAJOR` = folder restructures that break consumer adapters.

## [1.0.0]

### Changed (BREAKING)
- Replaced the `brain/` tree with the numbered pipeline structure
  (`00-context` … `99-inbox`), consolidated from two production client brains.
- `AGENTS.md` is now the single source of operating rules; `CLAUDE.md` is a
  pointer. Status vocabulary formalized: CONFIRMED / PENDING VALIDATION /
  INFERRED / SUPERSEDED / BLOCKED.
- Tooling is config-driven (`brain.config.json`): modular validation with
  semantic checks (duplicate IDs, unsourced decisions, status debt), init
  with engagement profiles, `make workspace` for hub-and-spoke repo cloning.

### Added
- `02-organization/` (ways of working, conventions incl. ticketing, AI
  policy, ownership, runbooks), `04-architecture/repos.yaml`, source-register
  template with conflict tracking, meeting minutes template, validation
  matrix, periodic validation check, decision log (`DEC-XXX`), skills
  `process_meeting` and bootstrap v2 with migration mode, `docs/workspace.md`.

## [0.1.0]
- Initial template (`brain/` structure).
