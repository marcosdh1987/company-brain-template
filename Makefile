.DEFAULT_GOAL := help

.PHONY: help init validate index workspace stats sync-skills opencode opencode-doctor

# OpenCode runtime: load ./.env, else the harness .env (same variable contract).
HARNESS_SOURCE ?= ../ml-python-base
OPENCODE_ENV ?= $(firstword $(wildcard .env $(HARNESS_SOURCE)/.env))

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

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

opencode:  ## Launch the OpenCode TUI with .env loaded (falls back to ../ml-python-base/.env)
	@command -v opencode >/dev/null 2>&1 || { echo "❌ opencode not found. Install: brew install anomalyco/tap/opencode"; exit 1; }
	@[ -n "$(OPENCODE_ENV)" ] || echo "⚠️  no .env found here or in $(HARNESS_SOURCE) — copy .env.example to .env (or use 'opencode auth login' / the /models picker)."
	@set -a; [ -n "$(OPENCODE_ENV)" ] && . "$(OPENCODE_ENV)"; set +a; opencode

opencode-doctor:  ## Check opencode install, which .env is loaded, and endpoint reachability
	@set -a; [ -n "$(OPENCODE_ENV)" ] && . "$(OPENCODE_ENV)"; set +a; \
	if command -v opencode >/dev/null 2>&1; then echo "✅ opencode: $$(opencode --version 2>/dev/null || echo installed)"; \
	else echo "❌ opencode not installed (brew install anomalyco/tap/opencode)"; fi; \
	if [ -n "$(OPENCODE_ENV)" ]; then echo "✅ env file: $(OPENCODE_ENV)"; \
	else echo "–  env file: none (.env or $(HARNESS_SOURCE)/.env) — copy .env.example to .env"; fi; \
	echo "–  build model: $${OPENCODE_MODEL:-<unset>}   plan model: $${OPENCODE_MODEL_PLAN:-<unset>}   small: $${OPENCODE_SMALL_MODEL:-<unset>}"; \
	for pair in "Ollama=$$OLLAMA_BASE_URL" "LM_Studio=$$LMSTUDIO_BASE_URL"; do \
	  name=$${pair%%=*}; url=$${pair#*=}; \
	  if [ -z "$$url" ]; then echo "–  $$name: not configured in .env"; continue; fi; \
	  if curl -fsS --max-time 4 "$$url/models" >/dev/null 2>&1; then echo "✅ $$name reachable: $$url"; \
	  else echo "❌ $$name unreachable: $$url (is the host up and the server listening?)"; fi; \
	done; \
	if [ -n "$$GATEWAY_BASE_URL" ]; then \
	  if curl -fsS --max-time 4 "$$GATEWAY_BASE_URL/models" -H "Authorization: Bearer $$GATEWAY_TOKEN" >/dev/null 2>&1; then echo "✅ AI Gateway reachable: $$GATEWAY_BASE_URL"; \
	  else echo "❌ AI Gateway unreachable: $$GATEWAY_BASE_URL (is the gateway running on :4000 and GATEWAY_TOKEN correct?)"; fi; \
	else echo "–  AI Gateway: GATEWAY_BASE_URL not set (using direct ollama/lmstudio providers)"; fi
