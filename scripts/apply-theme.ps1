<#
.SYNOPSIS
  Copy the repo's bamboo-vulgaris.vstheme over the copy installed by the VSIX,
  so you can test theme tweaks without rebuilding/repackaging/republishing.

.DESCRIPTION
  Run this on the Windows test machine after `git pull`. It finds every installed
  copy of bamboo-vulgaris.vstheme under your per-user Visual Studio extensions
  folders and overwrites them with the repo's current version.

  Prerequisite: the Bamboo (Vulgaris) VSIX has been installed at least once
  (that's what creates the destination files).

  After running: restart Visual Studio, then Tools > Options > Environment >
  General and switch the Color theme away and back to "Bamboo (Vulgaris)"
  (VS caches theme colors, so a restart + reselect is what forces a reload).

.EXAMPLE
  pwsh -File scripts/apply-theme.ps1
#>

$ErrorActionPreference = "Stop"

$src = Join-Path $PSScriptRoot "..\bamboo-vulgaris.vstheme" | Resolve-Path
$root = Join-Path $env:LOCALAPPDATA "Microsoft\VisualStudio"

if (-not (Test-Path $root)) {
    Write-Error "No Visual Studio data folder at $root"
    return
}

$targets = Get-ChildItem -Path $root -Recurse -Filter "bamboo-vulgaris.vstheme" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -ne $src.Path }

if (-not $targets) {
    Write-Warning "No installed bamboo-vulgaris.vstheme found under $root."
    Write-Warning "Install the VSIX once first, then re-run this script."
    return
}

foreach ($t in $targets) {
    Copy-Item -Path $src -Destination $t.FullName -Force
    Write-Host "Updated: $($t.FullName)"
}

Write-Host ""
Write-Host "Done. Now restart Visual Studio and reselect 'Bamboo (Vulgaris)'" -ForegroundColor Green
Write-Host "(Tools > Options > Environment > General > Color theme) to reload the colors." -ForegroundColor Green
