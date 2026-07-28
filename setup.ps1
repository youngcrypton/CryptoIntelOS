# ==========================================================
# CryptoIntel OS
# Windows Development Setup Script
# ==========================================================

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        CryptoIntel OS Setup"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------
# Check Python
# ----------------------------------------------------------

try {
    python --version | Out-Null
}
catch {
    Write-Host "Python is not installed." -ForegroundColor Red
    Write-Host "Install Python 3.11+ before continuing."
    exit
}

Write-Host "[OK] Python detected." -ForegroundColor Green

# ----------------------------------------------------------
# Create Virtual Environment
# ----------------------------------------------------------

if (!(Test-Path ".venv")) {

    Write-Host ""
    Write-Host "Creating virtual environment..."

    python -m venv .venv
}

# ----------------------------------------------------------
# Activate Virtual Environment
# ----------------------------------------------------------

Write-Host ""
Write-Host "Activating virtual environment..."

& ".\.venv\Scripts\Activate.ps1"

# ----------------------------------------------------------
# Upgrade pip
# ----------------------------------------------------------

Write-Host ""
Write-Host "Upgrading pip..."

python -m pip install --upgrade pip

# ----------------------------------------------------------
# Install Requirements
# ----------------------------------------------------------

Write-Host ""
Write-Host "Installing project dependencies..."

pip install -r requirements.txt

# ----------------------------------------------------------
# Install Playwright Browsers
# ----------------------------------------------------------

Write-Host ""
Write-Host "Installing Playwright browser..."

playwright install chromium

# ----------------------------------------------------------
# Environment File
# ----------------------------------------------------------

if (!(Test-Path ".env")) {

    Write-Host ""
    Write-Host "Creating .env from template..."

    Copy-Item ".env.example" ".env"
}

# ----------------------------------------------------------
# Create Project Directories
# ----------------------------------------------------------

$folders = @(
    "logs",
    "assets",
    "data"
)

foreach ($folder in $folders) {

    if (!(Test-Path $folder)) {

        New-Item -ItemType Directory -Path $folder | Out-Null
    }
}

# ----------------------------------------------------------
# Finished
# ----------------------------------------------------------

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " CryptoIntel OS setup completed!"
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:"
Write-Host ""
Write-Host "1. Edit your .env file"
Write-Host "2. Add your API keys"
Write-Host "3. Run the application"
Write-Host ""