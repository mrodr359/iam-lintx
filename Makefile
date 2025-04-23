.PHONY: format lint test all

format:
	black iam_lintx tests
	ruff format iam_lintx tests

lint:
	ruff check .

test:
	pytest -v

all: format lint test
