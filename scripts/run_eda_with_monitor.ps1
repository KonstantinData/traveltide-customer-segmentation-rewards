param(
  [string]$Config = "config/eda.yaml",
  [string]$OutDir = "artifacts/eda",
  [int]$RefreshSeconds = 2
)

New-Item -ItemType Directory -Force $OutDir | Out-Null
$env:DISABLE_PANDERA_IMPORT_WARNING = "True"

# Start monitor in a new window (runs a real .ps1 file, no embedded strings)
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-ExecutionPolicy", "Bypass",
  "-File", (Join-Path $PSScriptRoot "eda_monitor.ps1"),
  "-OutDir", $OutDir,
  "-RefreshSeconds", $RefreshSeconds
) | Out-Null

# Run EDA in the current window
python -u -m traveltide eda --config $Config --outdir $OutDir
