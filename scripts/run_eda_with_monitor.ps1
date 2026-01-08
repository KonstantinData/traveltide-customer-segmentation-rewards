param(
  [string]$Config = "config/eda.yaml",
  [string]$OutDir  = "artifacts/eda",
  [int]$RefreshSeconds = 2
)

# Ensure output directory exists
New-Item -ItemType Directory -Force $OutDir | Out-Null

# Start EDA run in THIS window
$env:DISABLE_PANDERA_IMPORT_WARNING = "True"

# Start monitor in a NEW window that watches latest run folder
$monitorScript = @"
`$ErrorActionPreference = 'SilentlyContinue'
`$outDir = '$OutDir'
`$refresh = $RefreshSeconds

function Get-LatestRunDir {
  if (-not (Test-Path `$outDir)) { return `$null }
  Get-ChildItem `$outDir -Directory |
    Sort-Object Name -Descending |
    Select-Object -First 1
}

while (`$true) {
  Clear-Host
  Write-Host ("TravelTide EDA Monitor  |  " + (Get-Date))
  Write-Host ("OutDir: " + (Resolve-Path `$outDir -ErrorAction SilentlyContinue))
  Write-Host ""

  `$latest = Get-LatestRunDir
  if (`$null -eq `$latest) {
    Write-Host "No run directory yet..."
  } else {
    Write-Host ("Latest run: " + `$latest.Name)
    Write-Host ("Path: " + `$latest.FullName)
    Write-Host ""

    # Show most recently updated files (top 30)
    Get-ChildItem -Recurse `$latest.FullName |
      Sort-Object LastWriteTime -Descending |
      Select-Object -First 30 FullName, Length, LastWriteTime |
      Format-Table -AutoSize

    # Quick milestone hints
    `$dataDir = Join-Path `$latest.FullName "data"
    `$sessions = Get-ChildItem -Path `$dataDir -Filter "sessions_clean.parquet" -ErrorAction SilentlyContinue
    `$users    = Get-ChildItem -Path `$dataDir -Filter "users_agg.parquet" -ErrorAction SilentlyContinue
    `$metaYaml = Get-ChildItem -Path `$latest.FullName -Filter "metadata.yaml" -ErrorAction SilentlyContinue
    `$report   = Get-ChildItem -Path `$latest.FullName -Filter "eda_report.html" -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host ("Milestones:")
    Write-Host ("- sessions_clean.parquet: " + ($(if (`$sessions) { "✅" } else { "…" })))
    Write-Host ("- users_agg.parquet:      " + ($(if (`$users)    { "✅" } else { "…" })))
    Write-Host ("- metadata.yaml:          " + ($(if (`$metaYaml) { "✅" } else { "…" })))
    Write-Host ("- eda_report.html:        " + ($(if (`$report)   { "✅" } else { "…" })))
  }

  Start-Sleep -Seconds `$refresh
}
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $monitorScript | Out-Null

# Now run the pipeline (this window will show logs/errors)
python -u -m traveltide eda --config $Config --outdir $OutDir
