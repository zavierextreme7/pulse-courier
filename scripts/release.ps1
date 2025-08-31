#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
  [string]$Remote = "https://github.com/R0D10Nq/pulse-courier.git",
  [switch]$SkipDocker,
  [switch]$SkipGit
)

function Invoke-Step($Title, [scriptblock]$Action) {
  Write-Host "`n== $Title ==" -ForegroundColor Cyan
  & $Action
}

Invoke-Step "Upgrade pip & install deps" {
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  python -m pip install -r requirements-dev.txt
}

Invoke-Step "Ruff (fix)" { python -m ruff check . --fix }
Invoke-Step "Black (format + check)" {
  python -m black .
  python -m black --check .
}
Invoke-Step "Mypy" { python -m mypy . }
Invoke-Step "Pytest" { python -m pytest -q }

if (-not $SkipDocker) {
  Invoke-Step "Docker compose config" { docker compose config | Out-Null }
  Invoke-Step "Docker compose up (detached)" { docker compose up -d --build }
  Invoke-Step "Health probe" {
    $ok = $false
    for ($i = 0; $i -lt 45; $i++) {
      try {
        $r = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -TimeoutSec 2
        if ($r.status -eq "ok") {
          Write-Host "Health OK: $($r | ConvertTo-Json -Compress)" -ForegroundColor Green
          $ok = $true
          break
        }
      } catch {}
      Start-Sleep -Seconds 2
    }
    if (-not $ok) { throw "Health check failed" }
  }
}

if (-not $SkipGit) {
  Invoke-Step "Git commit & push" {
    if (-not (Test-Path .git)) { git init }
    git add -A
    try {
      git commit -m "Чистим проект, наводим порядок и готовим к релизу" -m "Добавил QA-скрипты для Windows/Bash, dev-зависимости и выровнял CI. Прописал healthchecks в docker-compose, облегчил Dockerfile, дополнил README. Линтеры строгие, типы в порядке, базовые тесты зелёные. Готово к релизу." | Out-Null
    } catch {
      Write-Host "Commit skipped (nothing to commit?)"
    }
    git branch -M main
    $hasRemote = $true
    try { git remote get-url origin | Out-Null } catch { $hasRemote = $false }
    if ($hasRemote) {
      if ($PSBoundParameters.ContainsKey('Remote') -and $Remote) {
        git remote set-url origin $Remote
      } else {
        Write-Host "Remote 'origin' уже настроен; оставляем как есть."
      }
    } else {
      if ($PSBoundParameters.ContainsKey('Remote') -and $Remote) {
        git remote add origin $Remote
      } else {
        throw "Remote 'origin' не настроен. Запустите скрипт с параметром -Remote <URL>."
      }
    }
    git push -u origin main
  }
} else {
  Write-Host "Пропускаем шаг Git commit & push по флагу -SkipGit." -ForegroundColor Yellow
}

Write-Host "`nВсе этапы успешно завершены." -ForegroundColor Green
