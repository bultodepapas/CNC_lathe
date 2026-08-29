[CmdletBinding()]
param(
    [string]$ConfigDirectory = (Join-Path $PSScriptRoot '..\linuxcnc\configs\torno_v3')
)

$ErrorActionPreference = 'Stop'
$configDirectoryPath = (Resolve-Path -LiteralPath $ConfigDirectory).Path
$iniPath = Join-Path $configDirectoryPath 'torno_v3.ini'
if (-not (Test-Path -LiteralPath $iniPath -PathType Leaf)) {
    throw "No existe el INI esperado: $iniPath"
}

$warnings = [System.Collections.Generic.List[string]]::new()
$iniLines = Get-Content -LiteralPath $iniPath
$referencePatterns = @(
    '^\s*HALFILE\s*=\s*(\S+)',
    '^\s*POSTGUI_HALFILE\s*=\s*(\S+)',
    '^\s*SHUTDOWN\s*=\s*(\S+)',
    '^\s*TOOL_TABLE\s*=\s*(\S+)',
    '^\s*PARAMETER_FILE\s*=\s*(\S+)'
)

$references = foreach ($line in $iniLines) {
    foreach ($pattern in $referencePatterns) {
        if ($line -match $pattern) {
            $Matches[1]
            break
        }
    }
}

foreach ($reference in $references | Sort-Object -Unique) {
    if ($reference -match '^(LIB:|/|[A-Za-z]:)') {
        continue
    }
    $candidate = Join-Path $configDirectoryPath $reference
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        $warnings.Add("Referencia no incluida localmente (podría estar en la biblioteca HAL): $reference")
    }
}

$toolTablePath = Join-Path $configDirectoryPath 'tool.tbl'
if (Test-Path -LiteralPath $toolTablePath) {
    $toolNumbers = Get-Content -LiteralPath $toolTablePath |
        Where-Object { $_ -match '^T(-?\d+)\b' } |
        ForEach-Object { [int]$Matches[1] }
    $duplicates = $toolNumbers | Group-Object | Where-Object Count -gt 1
    foreach ($duplicate in $duplicates) {
        $warnings.Add("Número de herramienta duplicado: T$($duplicate.Name) ($($duplicate.Count) entradas)")
    }
}

$halPath = Join-Path $configDirectoryPath 'torno_v3.hal'
if (Test-Path -LiteralPath $halPath) {
    $halSources = @($halPath)
    $customHalPath = Join-Path $configDirectoryPath 'custom.hal'
    if (Test-Path -LiteralPath $customHalPath) {
        $halSources += $customHalPath
    }
    $halText = ($halSources | ForEach-Object { Get-Content -LiteralPath $_ -Raw }) -join "`n"
    if ($halText -match 'sets\s+spindle-at-speed\s+true') {
        $warnings.Add('spindle-at-speed está forzado a true.')
    }
    if ($halText -notmatch 'ext-estop-ok[\s\S]*and2\.0[\s\S]*iocontrol\.0\.emc-enable-in') {
        $warnings.Add('No se detectó la combinación esperada entre E-stop físico y habilitación de LinuxCNC.')
    }
    if ($halText -notmatch 'stepgen\.00\.') {
        $warnings.Add('El cuarto stepgen (00), probable torreta, no aparece configurado.')
    }

    $m100Path = Join-Path $configDirectoryPath '..\..\nc_files\M100'
    if (Test-Path -LiteralPath $m100Path) {
        $m100Text = Get-Content -LiteralPath $m100Path -Raw
        foreach ($signal in @('turret-search-speed', 'turret-home-mode', 'turret-index-pos')) {
            if ($m100Text -match [regex]::Escape($signal) -and $halText -notmatch [regex]::Escape($signal)) {
                $warnings.Add("M100 usa una señal ausente del HAL activo: $signal")
            }
        }
    }
}

Write-Host "Configuración revisada: $configDirectoryPath"
Write-Host "Referencias INI encontradas: $($references.Count)"
if ($warnings.Count -eq 0) {
    Write-Host 'No se encontraron advertencias estáticas.'
    exit 0
}

Write-Warning "Se encontraron $($warnings.Count) advertencias:"
foreach ($warning in $warnings) {
    Write-Host " - $warning"
}
exit 0
