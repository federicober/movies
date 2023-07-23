VIRTUAL_ENV = .venv

${VIRTUAL_ENV}/bin/python:
	python3 -m venv ${VIRTUAL_ENV}
	${VIRTUAL_ENV}/bin/pip install -U -q pip wheel
	touch ${VIRTUAL_ENV}/bin/python

.PHONY: venv
venv: ${VIRTUAL_ENV}/bin/python

${VIRTUAL_ENV}/.develop: pyproject.toml | venv
	${VIRTUAL_ENV}/bin/pip install -e .
	touch ${VIRTUAL_ENV}/.develop

.PHONY: develop
develop: ${VIRTUAL_ENV}/.develop

run: | develop
	${VIRTUAL_ENV}/bin/uvicorn api.__main__:app --factory --reload
