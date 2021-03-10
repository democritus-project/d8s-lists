#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort democritus_lists/ tests/

black democritus_lists/ tests/

mypy democritus_lists/ tests/

pylint --fail-under 9 democritus_lists/*.py

flake8 democritus_lists/ tests/

bandit -r democritus_lists/

# we run black again at the end to undo any odd changes made by any of the linters above
black democritus_lists/ tests/
