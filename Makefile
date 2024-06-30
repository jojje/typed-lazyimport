.PHONY: test lint build publish-test clean
test:
	python -m unittest -v

lint:
	flake8 --max-line-length 120 --ignore E231

build:
	poetry build --format wheel

publish:
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	poetry publish

publish-test:
	@echo poetry publish -r test-pypi --username=__token__  --password=[api-token]

init-env:
	python -m pip install poetry
	poetry install

clean:
	rm -rf dist
