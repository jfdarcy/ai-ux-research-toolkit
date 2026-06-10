$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating project virtual environment..."
    python -m venv .venv
    & $venvPython -m pip install -r requirements.txt
}

Write-Host "Starting Thematic Analyzer with project venv..."
& $venvPython -m streamlit run thematic_analyzer.py
