.PHONY: test lint build publish-test clean
test:
	python -m unittest -v

lint:
	flake8 --max-line-length 120 --ignore E231

build:
	poetry build --format wheel

publish-test:
	poetry publish -r test-pypi

clean:
	rm -rf dist
