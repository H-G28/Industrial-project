$projectPath = Join-Path $PSScriptRoot "DIAMONDAURAWEB()\DIAMONDAURAWEB()\DIAMONDAURAWEB"

if (-not (Test-Path $projectPath)) {
    Write-Error "Project folder not found: $projectPath"
    exit 1
}

Set-Location $projectPath

if (-not (Test-Path ".\requirements.txt")) {
    Write-Error "requirements.txt not found in $projectPath"
    exit 1
}

Write-Host "Installing dependencies..."
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Running migrations..."
python manage.py migrate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Starting Django server at http://127.0.0.1:8000/"
python manage.py runserver
