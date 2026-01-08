param(
  [Parameter(Mandatory = $true)][string]$OutDir,
  [int]$RefreshSeconds = 2,
  [int]$AutoCloseSeconds = 5,
  [switch]$KeepOpen
)

$ErrorActionPreference = "SilentlyContinue"

function Get-LatestRunDir {
  if (-not (Test-Path $OutDir)) { return $null }
  Get-ChildItem -Path $OutDir -Directory | Sort-Object Name -Descending | Select-Object -First 1
}

function Show-CompletionAndExit {
  param(
    [string]$RunName,
    [string]$RunPath,
    [int]$Seconds
  )

  Write-Host ""
  Write-Host "✅ EDA run completed." -ForegroundColor Green
  Write-Host ("Run:  " + $RunName)
  Write-Host ("Path: " + $RunPath)

  if ($KeepOpen) {
    Write-Host ""
    Write-Host "KeepOpen was set -> leaving monitor window open."
    return
  }

  if ($Seconds -le 0) {
    exit 0
  }

  Write-Host ""
  Write-Host ("Closing this monitor window in " + $Seconds + " seconds...")
  for ($i = $Seconds; $i -ge 1; $i--) {
    Write-Host ("  " + $i + "...")
    Start-Sleep -Seconds 1
  }
  exit 0
}

while ($true) {
  Clear-Host
  Write-Host ("TravelTide EDA Monitor | " + (Get-Date))
  Write-Host ("OutDir: " + $OutDir)
  Write-Host ""

  $latest = Get-LatestRunDir
  if ($null -eq $latest) {
    Write-Host "No run directory yet..."
    Start-Sleep -Seconds $RefreshSeconds
    continue
  }

  Write-Host ("Latest run: " + $latest.Name)
  Write-Host ("Path: " + $latest.FullName)
  Write-Host ""

  Get-ChildItem -Recurse -Path $latest.FullName |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 30 FullName, Length, LastWriteTime |
    Format-Table -AutoSize

  $dataDir  = Join-Path $latest.FullName "data"
  $sessions = Test-Path (Join-Path $dataDir "sessions_clean.parquet")
  $users    = Test-Path (Join-Path $dataDir "users_agg.parquet")
  $metaYaml = Test-Path (Join-Path $latest.FullName "metadata.yaml")
  $metaJson = Test-Path (Join-Path $latest.FullName "metadata.json")
  $report   = Test-Path (Join-Path $latest.FullName "eda_report.html")

  Write-Host ""
  Write-Host "Milestones:"
  Write-Host ("- sessions_clean.parquet: " + ($(if ($sessions) { "OK" } else { "..." })))
  Write-Host ("- users_agg.parquet:      " + ($(if ($users)    { "OK" } else { "..." })))
  Write-Host ("- metadata.yaml:          " + ($(if ($metaYaml) { "OK" } else { "..." })))
  Write-Host ("- metadata.json:          " + ($(if ($metaJson) { "OK" } else { "..." })))
  Write-Host ("- eda_report.html:        " + ($(if ($report)   { "OK" } else { "..." })))

  # Auto-finish: if all milestones are present, show completion message and exit.
  if ($sessions -and $users -and $metaYaml -and $metaJson -and $report) {
    Show-CompletionAndExit -RunName $latest.Name -RunPath $latest.FullName -Seconds $AutoCloseSeconds
    # If KeepOpen was set, we continue monitoring.
  }

  Start-Sleep -Seconds $RefreshSeconds
}
