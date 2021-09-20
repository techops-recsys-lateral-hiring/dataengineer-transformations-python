#!/bin/bash

set -e

poetry install

echo "Running type checks"
poetry run mypy --ignore-missing-imports --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs \
            data_transformations tests

echo "Running lint checks"
poetry run pylint data_transformations tests
