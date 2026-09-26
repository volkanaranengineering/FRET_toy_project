param([switch]$Desktop)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$fretDir = Join-Path $repoRoot 'vendor/fret/fret-electron'
Get-Command node,npm -ErrorAction Stop | Out-Null
& npm ci --prefix $fretDir --ignore-scripts --legacy-peer-deps --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'FRET compiler dependency installation failed' }
if ($Desktop) {
    & npm ci --prefix (Join-Path $repoRoot 'vendor/fret/tools/LTLSIM/ltlsim-core') --ignore-scripts --legacy-peer-deps --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'LTLSIM JavaScript library dependency installation failed' }
    & npm ci --prefix (Join-Path $fretDir 'app') --ignore-scripts --legacy-peer-deps --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'FRET desktop dependency installation failed' }
    Push-Location $fretDir
    try {
        & node 'node_modules/electron/install.js'
        if ($LASTEXITCODE -ne 0) { throw 'Electron runtime installation failed' }
        & npm run build
        if ($LASTEXITCODE -ne 0) { throw 'FRET desktop build failed' }
    } finally { Pop-Location }
}
Write-Host 'Setup completed. See docs/REPRODUCIBILITY.md.'
