VIRTUAL_ENV = .venv

${VIRTUAL_ENV}/bin/python:
	python3 -m venv ${VIRTUAL_ENV}
	${VIRTUAL_ENV}/bin/pip install -U -q pip wheel
	touch ${VIRTUAL_ENV}/bin/python

.PHONY: venv
venv: ${VIRTUAL_ENV}/bin/python

${VIRTUAL_ENV}/.develop: pyproject.toml | venv
	${VIRTUAL_ENV}/bin/pip install -e .[dev]
	touch ${VIRTUAL_ENV}/.develop

.PHONY: develop
develop: ${VIRTUAL_ENV}/.develop

.env: makefile
	@cat .env | grep CORS_REGEX || (echo CORS_REGEX=.* >> .env)
	@cat .env | grep DB_DSN || (echo DB_DSN=sqlite+aiosqlite:///movies.db >> .env)
	@cat .env | grep SECRET_KEY || (echo SECRET_KEY=$$(openssl rand -hex 32) >> .env)
	touch .env

run: .env | develop
	${VIRTUAL_ENV}/bin/uvicorn api.app:app --factory --reload

.PHONY: lint
lint:
	${VIRTUAL_ENV}/bin/ruff check --fix .
