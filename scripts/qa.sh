#!/usr/bin/env bash
set -euo pipefail

echo "== Ruff (fix) =="
python -m ruff check . --fix

echo "== Black (check) =="
python -m black --check .

echo "== Mypy =="
python -m mypy .

echo "== Pytest =="
python -m pytest -q

echo "Все проверки пройдены."
