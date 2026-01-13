# allow triggering Make both outside/inside of a Docker container
# use ?= assignments to allow overwrite from env vars
IN_DOCKER ?= $(if $(wildcard /.dockerenv),true,false)
ifeq ($(IN_DOCKER), true)
  RUN ?=
  RUN_INTERACTIVE ?=
else
  RUN ?= docker compose --progress=quiet run --no-TTY --rm connect-mcp
  RUN_INTERACTIVE ?= docker compose --progress=quiet run --rm connect-mcp
endif
define ABORT_IN_DOCKER
  @if $(IN_DOCKER); then \
    echo "ABORTING: target '$@' cannot be run inside a Docker container."; \
    exit 1; \
  fi
endef

# colors
COLOR_GREEN=\033[0;32m
COLOR_RED=\033[0;31m
COLOR_BLUE=\033[0;34m
END_COLOR=\033[0m

.PHONY: up
up: .env build
	@echo "$(COLOR_GREEN)Starting the app 🎬$(END_COLOR)"
	$(call ABORT_IN_DOCKER)
	docker compose up -d
	@echo "$(COLOR_GREEN)MCP Server is running 🚀$(END_COLOR)"


# Stop all application containers
.PHONY: down
down:
	$(call ABORT_IN_DOCKER)
	docker compose down --remove-orphans

# restart the app
.PHONY: restart
restart: down up

# Run shell inside a new app container (having consistent environment, but different container)
.PHONY: bash
bash:
	$(RUN_INTERACTIVE) bash

# Run shell in the currently running app container
.PHONY: exec
exec:
	$(call ABORT_IN_DOCKER)
	docker compose exec -it connect-mcp bash

# Force trigger re-build of the app image
.PHONY: build
build:
	$(call ABORT_IN_DOCKER)
	docker compose build

# Clean everything
.PHONY: clean
clean:
	@echo "$(COLOR_RED)- 🧼 Cleaning the project 🧹$(END_COLOR)"
	$(call ABORT_IN_DOCKER)
	docker compose down --remove-orphans --rmi local --volumes

# Run unit tests including doctests
# pytest has nicer output when run with TTY attached
.PHONY: tests
tests:
	@echo "$(COLOR_BLUE)----- tests -----$(END_COLOR)"
	$(RUN_INTERACTIVE) uv run pytest
	@echo

# Run linter
.PHONY: lint
lint:
	@echo "$(COLOR_BLUE)----- linter -----$(END_COLOR)"
	$(RUN_INTERACTIVE) uv run ruff check --fix
	@echo

# Run formatter
.PHONY: format
format:
	@echo "$(COLOR_BLUE)----- format -----$(END_COLOR)"
	$(RUN_INTERACTIVE) uv run ruff format
	@echo

.PHONY: qa
qa: lint format tests

# Don't check .env existence inside Docker - there are real env vars instead
.env:
	@if [ "$(IN_DOCKER)" = "false" -a ! -f .env ]; then \
	    @echo "Please create '.env' with your conf"; \
	    exit 1; \
	fi;
