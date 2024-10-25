PY:=python3
PROJECT_ROOT:=$(shell pwd)
REQUIREMENTS:=$(PROJECT_ROOT)/requirements.txt

.ONESHELL:
.PHONY: venv
venv:
	@$(PY) -m venv .venv
	@. .venv/bin/activate
	@pip install -r $(REQUIREMENTS)

.PHONY: test
test:

.PHONY: fmt
fmt:
	@ruff format .
	@ruff check --fix .

.PHONY: check
check:
	@ruff check .
