
.PHONY: build clean test
test:
	python -m unittest -v

build:
	poetry build --format wheel

publish-test:
	poetry publish -r test-pypi

clean:
	rm -rf dist
