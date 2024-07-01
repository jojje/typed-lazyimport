.PHONY: test lint build publish publish-test init-env clean

ifeq ($(OS),Windows_NT)
  python := .venv/Scripts/python.exe
else
  python := .venv/bin/python
endif

pip = $(python) -m pip
poetry := $(python) -m poetry
flake8 := $(poetry) run flake8
mypy := $(poetry) run mypy

test:
	$(python) -m unittest -v

lint:
	$(flake8) --max-line-length 120 --ignore E231 --exclude .venv
	$(mypy) -m lazyimport --ignore-missing-imports

build:
	$(poetry) build --format wheel

publish:
	@$(poetry) config pypi-token.pypi $(PYPI_TOKEN)
	$(poetry) publish

publish-test:
	@echo poetry publish -r test-pypi --username=__token__  --password=[api-token]

init-env:
	@test -d .venv || python -m venv .venv
	$(pip) install poetry
	$(poetry) install

clean:
	rm -rf dist
