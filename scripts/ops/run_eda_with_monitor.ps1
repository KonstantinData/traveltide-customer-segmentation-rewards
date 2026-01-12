# Purpose: Launch the EDA pipeline and a live monitoring window for artifact progress.
# Inputs: Config (EDA config path), OutDir (output root), RefreshSeconds (monitor poll interval).
# Outputs (path + format): Writes EDA artifacts under OutDir (e.g., artifacts/eda/<run_id>/...), formats include parquet, yaml/json, html.
# How to run: powershell -File scripts/ops/run_eda_with_monitor.ps1 [-Config config/eda.yaml] [-OutDir artifacts/eda] [-RefreshSeconds 2]
# Description: Optional operational helper to run EDA with a live monitor (non-EDA utility).
param(
  [string]$Config = "config/eda.yaml",
  [string]$OutDir = "artifacts/eda",
  [int]$RefreshSeconds = 2
)

# Notes: Default paths assume repo-root execution; override for custom locations.
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

# Notes: The EDA CLI writes parquet and report artifacts into the OutDir tree.
# Notes: Execute the EDA pipeline in the current terminal session.
# Run EDA in the current window
python -u -m traveltide eda --config $Config --outdir $OutDir
