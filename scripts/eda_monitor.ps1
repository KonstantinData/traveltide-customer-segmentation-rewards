# Description: Monitor EDA artifact generation and show milestone status.
param(
  [Parameter(Mandatory = $true)][string]$OutDir,
  [int]$RefreshSeconds = 2,
  [int]$AutoCloseSeconds = 5,
  [switch]$KeepOpen
)

$ErrorActionPreference = "SilentlyContinue"

# Notes: Resolve the most recent EDA run folder in the output directory.
function Get-LatestRunDir {
  if (-not (Test-Path $OutDir)) { return $null }
  Get-ChildItem -Path $OutDir -Directory | Sort-Object Name -Descending | Select-Object -First 1
}

# Notes: Display completion details and optionally close the monitor window.
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
  $cleanedDir = Join-Path $dataDir "cleaned"
  $transformedDir = Join-Path $dataDir "transformed"
  $sessions = Test-Path (Join-Path $dataDir "sessions_clean.parquet")
  $users    = Test-Path (Join-Path $dataDir "users_agg.parquet")
  $cleanedSessions = Test-Path (Join-Path $cleanedDir "sessions_cleaned.parquet")
  $cleanedUsers    = Test-Path (Join-Path $cleanedDir "users_cleaned.parquet")
  $cleanedFlights  = Test-Path (Join-Path $cleanedDir "flights_cleaned.parquet")
  $cleanedHotels   = Test-Path (Join-Path $cleanedDir "hotels_cleaned.parquet")
  $transformedSessions = Test-Path (Join-Path $transformedDir "sessions_transformed.parquet")
  $transformedUsers    = Test-Path (Join-Path $transformedDir "users_transformed.parquet")
  $transformedFlights  = Test-Path (Join-Path $transformedDir "flights_transformed.parquet")
  $transformedHotels   = Test-Path (Join-Path $transformedDir "hotels_transformed.parquet")
  $metaYaml = Test-Path (Join-Path $latest.FullName "metadata.yaml")
  $metaJson = Test-Path (Join-Path $latest.FullName "metadata.json")
  $report   = Test-Path (Join-Path $latest.FullName "eda_report.html")

  Write-Host ""
  Write-Host "Milestones:"
  Write-Host ("- sessions_clean.parquet: " + ($(if ($sessions) { "OK" } else { "..." })))
  Write-Host ("- users_agg.parquet:      " + ($(if ($users)    { "OK" } else { "..." })))
  Write-Host ("- cleaned/sessions_cleaned.parquet: " + ($(if ($cleanedSessions) { "OK" } else { "..." })))
  Write-Host ("- cleaned/users_cleaned.parquet:    " + ($(if ($cleanedUsers)    { "OK" } else { "..." })))
  Write-Host ("- cleaned/flights_cleaned.parquet:  " + ($(if ($cleanedFlights)  { "OK" } else { "..." })))
  Write-Host ("- cleaned/hotels_cleaned.parquet:   " + ($(if ($cleanedHotels)   { "OK" } else { "..." })))
  Write-Host ("- transformed/sessions_transformed.parquet: " + ($(if ($transformedSessions) { "OK" } else { "..." })))
  Write-Host ("- transformed/users_transformed.parquet:    " + ($(if ($transformedUsers)    { "OK" } else { "..." })))
  Write-Host ("- transformed/flights_transformed.parquet:  " + ($(if ($transformedFlights)  { "OK" } else { "..." })))
  Write-Host ("- transformed/hotels_transformed.parquet:   " + ($(if ($transformedHotels)   { "OK" } else { "..." })))
  Write-Host ("- metadata.yaml:          " + ($(if ($metaYaml) { "OK" } else { "..." })))
  Write-Host ("- metadata.json:          " + ($(if ($metaJson) { "OK" } else { "..." })))
  Write-Host ("- eda_report.html:        " + ($(if ($report)   { "OK" } else { "..." })))

  # Auto-finish: if all milestones are present, show completion message and exit.
  if ($sessions -and $users -and $cleanedSessions -and $cleanedUsers -and $cleanedFlights -and $cleanedHotels `
      -and $transformedSessions -and $transformedUsers -and $transformedFlights -and $transformedHotels `
      -and $metaYaml -and $metaJson -and $report) {
    Show-CompletionAndExit -RunName $latest.Name -RunPath $latest.FullName -Seconds $AutoCloseSeconds
    # If KeepOpen was set, we continue monitoring.
  }

  Start-Sleep -Seconds $RefreshSeconds
}
