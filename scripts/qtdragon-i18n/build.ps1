[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Catalog,

    [Parameter(Mandatory = $true)]
    [string]$Output,

    [double]$MinimumCoverage = 98,

    [string]$Python = "python",

    [string]$LRelease = "lrelease"
)

$ErrorActionPreference = "Stop"
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$catalogPath = (Resolve-Path -LiteralPath $Catalog).Path
$outputPath = [System.IO.Path]::GetFullPath($Output)
$outputDirectory = Split-Path -Parent $outputPath

if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

& $Python (Join-Path $scriptDirectory "validate_ts.py") $catalogPath --min-coverage $MinimumCoverage
if ($LASTEXITCODE -ne 0) {
    throw "TS validation failed; QM was not generated."
}

& $LRelease $catalogPath -qm $outputPath
if ($LASTEXITCODE -ne 0) {
    throw "lrelease failed."
}

& $Python (Join-Path $scriptDirectory "validate_qm.py") $outputPath
if ($LASTEXITCODE -ne 0) {
    throw "QM validation failed."
}

Get-FileHash -Algorithm SHA256 -LiteralPath $outputPath
