param(
    [string]$Message = "Update Monster Quant",
    [int]$Retries = 3
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

function Has-Changes {
    $status = git status --porcelain
    return -not [string]::IsNullOrWhiteSpace($status)
}

Write-Host "==> Checking git status" -ForegroundColor Cyan
git status --short --branch

if (Has-Changes) {
    Write-Host ""
    Write-Host "==> Committing local changes" -ForegroundColor Cyan
    git add .
    git commit -m $Message
} else {
    Write-Host ""
    Write-Host "==> No local changes to commit" -ForegroundColor Green
}

for ($Attempt = 1; $Attempt -le $Retries; $Attempt++) {
    Write-Host ""
    Write-Host "==> Pushing origin main (attempt $Attempt/$Retries)" -ForegroundColor Cyan
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push complete." -ForegroundColor Green
        exit 0
    }
    Start-Sleep -Seconds (3 * $Attempt)
}

throw "Push failed after $Retries attempts."
