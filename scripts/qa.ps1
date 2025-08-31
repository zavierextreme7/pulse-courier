#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "== Ruff (fix) =="
python -m ruff check . --fix

Write-Host "== Black (check) =="
python -m black --check .

Write-Host "== Mypy =="
python -m mypy .

Write-Host "== Pytest =="
python -m pytest -q

Write-Host "Все проверки пройдены."
