# Little Lores Audio Generation - Quick Start Guide
# Run these commands in PowerShell

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Little Lores - Audio Generation Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check if in scripts directory
$currentPath = Get-Location
if (-not ($currentPath -like "*\scripts")) {
    Write-Host "Changing to scripts directory..." -ForegroundColor Yellow
    Set-Location "$PSScriptRoot"
}

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check Google Cloud credentials
Write-Host "`nChecking Google Cloud credentials..." -ForegroundColor Green
$gcpCreds = $env:GOOGLE_APPLICATION_CREDENTIALS
if ($gcpCreds -and (Test-Path $gcpCreds)) {
    Write-Host "  ✓ Credentials found: $gcpCreds" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Google Cloud credentials not set!" -ForegroundColor Yellow
    Write-Host "    Set with: `$env:GOOGLE_APPLICATION_CREDENTIALS='path\to\key.json'" -ForegroundColor Yellow
    Write-Host "    See README.md for setup instructions" -ForegroundColor Yellow
}

# Check Supabase status
Write-Host "`nChecking Supabase status..." -ForegroundColor Green
$supabaseStatus = supabase status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Supabase is running" -ForegroundColor Green
} else {
    Write-Host "  ✗ Supabase is not running! Start with: supabase start" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "Setup Complete! Ready to process stories" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Analyze stories:    python analyze_stories.py" -ForegroundColor White
Write-Host "  2. Clean stories:      python clean_stories.py" -ForegroundColor White
Write-Host "  3. Test audio (5):     python generate_audio.py --limit 5" -ForegroundColor White
Write-Host "  4. Generate all:       python generate_audio.py --all --apply" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Gray
Write-Host ""
