.DEFAULT_GOAL := help

.PHONY: help init validate stats

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

init:  ## Instantiate for an organization: make init ORG="Acme S.A."
	@test -n "$(ORG)" || (echo "Usage: make init ORG=\"Acme S.A.\"" && exit 1)
	python3 scripts/init_brain.py --org "$(ORG)"

validate:  ## Check structure, links and report _PENDING_ debt
	python3 scripts/validate_structure.py

stats:  ## Quick content stats per section
	@echo "Files and words per section:"
	@for d in brain/domain brain/decisions brain/conventions brain/architecture brain/runbooks brain/team memory; do \
		printf "  %-24s %3d files  %6d words\n" $$d $$(find $$d -name '*.md' | wc -l) $$(cat $$d/*.md 2>/dev/null | wc -w); \
	done
