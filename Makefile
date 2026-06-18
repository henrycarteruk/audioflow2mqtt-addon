.DEFAULT_GOAL := help

.PHONY: help install test run lock clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "} {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Create the virtualenv and install all dependencies (incl. dev)
	uv sync

test: ## Run the test suite
	uv run pytest

run: ## Run the add-on locally (python -m audioflow2mqtt)
	uv run python -m audioflow2mqtt

lock: ## Update the dependency lockfile
	uv lock

clean: ## Remove the virtualenv and caches
	rm -rf .venv .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
