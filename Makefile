MYPY_OPTIONS = --ignore-missing-imports --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs

.PHONY: integration-test
integration-test:
	poetry run pytest tests/integration

.PHONY: unit-test
unit-test:
	poetry run pytest tests/unit

.PHONY: lint-check
lint-check:
	poetry run pylint data_transformations tests

.PHONY: type-check
type-check:
	poetry run mypy ${MYPY_OPTIONS} data_transformations tests

.PHONY: style-checks
style-checks: lint-check type-check

.PHONY: tests
tests: unit-test integration-test

requirements.txt:
	poetry export -f requirements.txt --output requirements.txt --dev

.PHONY: docker-tests
docker-tests:
	./scripts/spark-docker-tests.sh
