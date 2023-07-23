VIRTUAL_ENV: .venv

${VIRTUAL_ENV}/bin/python:
	python3 -m venv ${VIRTUAL_ENV}
	touch ${VIRTUAL_ENV}/bin/python

.PHONY: venv
venv: ${VIRTUAL_ENV}/bin/python

api.egg-info: pyproject.toml | venv
	${VIRTUAL_ENV}/bin/pip install -e .
	touch api.egg-info

.PHONY: develop
develop: api.egg-info