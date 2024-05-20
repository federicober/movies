VIRTUAL_ENV = .venv

${VIRTUAL_ENV}/bin/python: .python-version
	rm -rf ${VIRTUAL_ENV}
	python -m venv ${VIRTUAL_ENV}
	${VIRTUAL_ENV}/bin/pip install -U -q pip wheel
	touch ${VIRTUAL_ENV}/bin/python

.PHONY: venv
venv: ${VIRTUAL_ENV}/bin/python

${VIRTUAL_ENV}/.develop: pyproject.toml ${VIRTUAL_ENV}/bin/python
	${VIRTUAL_ENV}/bin/pip install -e .[dev]
	touch ${VIRTUAL_ENV}/.develop

.PHONY: develop
develop: ${VIRTUAL_ENV}/.develop

.env: makefile
	@cat .env | grep CORS_REGEX || (echo CORS_REGEX=.* >> .env)
	@cat .env | grep DB_DSN || (echo DB_DSN=sqlite+aiosqlite:///movies.db >> .env)
	@cat .env | grep SECRET_KEY || (echo SECRET_KEY=$$(openssl rand -hex 32) >> .env)
	touch .env

.PHONY: run
run: .env | develop
	${VIRTUAL_ENV}/bin/uvicorn movies.api.app:app_factory --factory --reload

.PHONY: lint
lint: | develop
	${VIRTUAL_ENV}/bin/ruff check --fix .
	${VIRTUAL_ENV}/bin/mypy

.PHONY: test
test: | develop
	${VIRTUAL_ENV}/bin/pytest

.PHONY: all
all: lint test
