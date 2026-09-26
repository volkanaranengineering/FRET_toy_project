param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    & node 'projects/build.cjs'
    if ($LASTEXITCODE -ne 0) { throw 'FRET compilation failed' }
    & $Python 'projects/collect-evidence.py'
    if ($LASTEXITCODE -ne 0) { throw 'Evidence collection failed' }
    & node 'projects/check-examples.cjs'
    if ($LASTEXITCODE -ne 0) { throw 'Example checks failed' }
    & node 'projects/report.cjs'
    if ($LASTEXITCODE -ne 0) { throw 'Report generation failed' }
    & $Python 'tools/verify_archive.py'
    if ($LASTEXITCODE -ne 0) { throw 'Archive verification failed' }
} finally { Pop-Location }
