# Description: Optional operational helper to run EDA with a live monitor (non-EDA utility).
param(
  [string]$Config = "config/eda.yaml",
  [string]$OutDir = "artifacts/eda",
  [int]$RefreshSeconds = 2
)

# Notes: Ensure output directory exists and suppress noise.
New-Item -ItemType Directory -Force $OutDir | Out-Null
$env:DISABLE_PANDERA_IMPORT_WARNING = "True"

# Notes: Start the monitor in a new window for live run visibility.
# Start monitor in a new window (runs a real .ps1 file, no embedded strings)
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-ExecutionPolicy", "Bypass",
  "-File", (Join-Path $PSScriptRoot "eda_monitor.ps1"),
  "-OutDir", $OutDir,
  "-RefreshSeconds", $RefreshSeconds
) | Out-Null

# Notes: Execute the EDA pipeline in the current terminal session.
# Run EDA in the current window
python -u -m traveltide eda --config $Config --outdir $OutDir
