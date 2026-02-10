# AI Career Interview System - Cleanup Script
# This script removes cache folders, logs, and temporary files.

Write-Host "Starting project cleanup..." -ForegroundColor Cyan

# 1. Remove Python cache
Write-Host "Removing Python __pycache__ folders..."
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Force -Recurse
if (Test-Path "backend/__pycache__") { Remove-Item -Path "backend/__pycache__" -Force -Recurse }

# 2. Remove Frontend junk
Write-Host "Removing Frontend cache and logs..."
$frontendJunk = @(
    "frontend/.next",
    "frontend/node_modules",
    "frontend/package-lock.json",
    "frontend/tsconfig.tsbuildinfo",
    "frontend/build_log.txt",
    "frontend/build_log_2.txt",
    "frontend/lint_check.txt",
    "frontend/lint_final.txt",
    "frontend/lint_full.txt",
    "frontend/lint_full_2.txt",
    "frontend/lint_new.txt",
    "frontend/lint_output.txt",
    "frontend/lint_report.json",
    "frontend/lint_src.txt",
    "frontend/tsc_errors.txt",
    "frontend/tsc_output.txt"
)

foreach ($item in $frontendJunk) {
    if (Test-Path $item) {
        Write-Host "Deleting $item"
        Remove-Item -Path $item -Force -Recurse
    }
}

# 3. Remove Backend junk
Write-Host "Removing Backend logs..."
if (Test-Path "backend/diagnostic_results.txt") {
    Remove-Item -Path "backend/diagnostic_results.txt" -Force
}

Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "1. cd frontend"
Write-Host "2. npm install"
Write-Host "3. npm run dev"
Write-Host "4. (In another terminal) cd backend"
Write-Host "5. pip install -r requirements.txt"
Write-Host "6. python main.py"
