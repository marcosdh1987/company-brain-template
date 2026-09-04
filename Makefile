.DEFAULT_GOAL := help

.PHONY: help init validate index workspace stats

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

init:  ## Instantiate: make init ORG="Acme Inc." [PROFILE=consulting|delivery-oversight|development|full|team|engineering-management|consulting-company|client-engagement]
	@test -n "$(ORG)" || (echo "Usage: make init ORG=\"Acme Inc.\" [PROFILE=full]" && exit 1)
	python3 scripts/init_brain.py --org "$(ORG)" --profile "$(or $(PROFILE),full)"

validate:  ## Structure (per config), links, duplicate IDs, unsourced decisions, status debt, index staleness
	python3 scripts/build_indexes.py --check
	python3 scripts/validate_structure.py

index:  ## Regenerate generated indexes (03-work, 06-decisions, 05-requirements)
	python3 scripts/build_indexes.py

workspace:  ## Clone all repos from 04-architecture/repos.yaml as siblings of this brain
	python3 scripts/clone_workspace.py

stats:  ## Content stats per active module
	@python3 -c "import json,pathlib; cfg=json.load(open('brain.config.json')); \
mods=[m for m,on in cfg['modules'].items() if on and pathlib.Path(m).is_dir()]; \
print('Files and words per active module:'); \
[print('  %-20s %3d files %7d words' % (m, len(list(pathlib.Path(m).rglob('*.md'))), sum(len(p.read_text(encoding='utf-8').split()) for p in pathlib.Path(m).rglob('*.md')))) for m in mods]"

sync-skills:  ## Sync working skills from the harness + regenerate tool projections
	python3 scripts/sync_skills.py
