param(
    [ValidateSet("setup", "cli", "api", "frontend", "docker", "status")]
    [string]$Action = "cli",

    [ValidateSet("mock", "akshare")]
    [string]$Provider = "akshare"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

function Invoke-Step($Message, $ScriptBlock) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
    & $ScriptBlock
}

switch ($Action) {
    "setup" {
        Invoke-Step "Installing Python package" {
            python -m pip install -e ".[dev]"
        }
        Invoke-Step "Setup complete" {
            Write-Host "Run mock demo: .\scripts\monster.ps1 cli -Provider mock"
            Write-Host "Run akshare:   .\scripts\monster.ps1 cli -Provider akshare"
            Write-Host "Run API:       .\scripts\monster.ps1 api -Provider akshare"
        }
    }

    "cli" {
        $env:DATA_PROVIDER = $Provider
        Invoke-Step "Running Monster Quant CLI with DATA_PROVIDER=$Provider" {
            python -m monster_quant.cli
        }
    }

    "api" {
        $env:DATA_PROVIDER = $Provider
        Invoke-Step "Starting API at http://127.0.0.1:8000 with DATA_PROVIDER=$Provider" {
            uvicorn monster_quant.api.app:create_app --factory --reload
        }
    }

    "frontend" {
        Invoke-Step "Installing frontend dependencies if needed" {
            if (-not (Test-Path "frontend\node_modules")) {
                npm install --prefix frontend
            }
        }
        Invoke-Step "Starting frontend at http://127.0.0.1:5173" {
            npm run dev --prefix frontend
        }
    }

    "docker" {
        Invoke-Step "Starting PostgreSQL, Redis, and backend" {
            docker compose -f docker/docker-compose.yml up -d
        }
    }

    "status" {
        Invoke-Step "Git status" {
            git status --short --branch
        }
        Invoke-Step "Latest commit" {
            git log --oneline -1
        }
    }
}
