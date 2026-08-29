[CmdletBinding()]
param(
    [string]$CncHost = 'cnc.taila1b901.ts.net',
    [string]$CncUser = 'cnc',
    [string]$RemoteLinuxCncRoot = '/home/cnc/linuxcnc',
    [string]$BackupRoot = (Join-Path $PSScriptRoot '..\backups'),
    [switch]$InteractiveAuth
)

$ErrorActionPreference = 'Stop'

foreach ($command in @('ssh', 'scp')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "No se encontró '$command' en PATH. Instale OpenSSH Client."
    }
}

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$resolvedBackupRoot = [System.IO.Path]::GetFullPath($BackupRoot)
if (-not $resolvedBackupRoot.StartsWith($repositoryRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Por seguridad, BackupRoot debe estar dentro del repositorio: $repositoryRoot"
}

$target = '{0}@{1}' -f $CncUser, $CncHost
$sshOptions = @('-o', 'ConnectTimeout=8', '-o', 'StrictHostKeyChecking=accept-new')
if (-not $InteractiveAuth) {
    $sshOptions += @('-o', 'BatchMode=yes')
}

Write-Host "Comprobando conexión de solo lectura con $target ..."
& ssh @sshOptions $target 'hostname; uname -a; linuxcnc --version 2>/dev/null || true'
if ($LASTEXITCODE -ne 0) {
    throw "No fue posible conectar con $target. Confirme Tailscale, usuario y autenticación."
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDirectory = Join-Path $resolvedBackupRoot "$timestamp-cnc"
New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null

$inventoryCommand = @'
set -u
printf 'hostname='; hostname
printf 'date='; date --iso-8601=seconds
printf 'kernel='; uname -srmo
printf 'linuxcnc='; linuxcnc --version 2>/dev/null || true
printf 'tailscale_ipv4='; tailscale ip -4 2>/dev/null || true
printf '\nLinuxCNC files:\n'
find /home/cnc/linuxcnc -maxdepth 4 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS %s %p\n' 2>/dev/null | sort
'@

$inventoryPath = Join-Path $backupDirectory 'remote-inventory.txt'
$inventory = & ssh @sshOptions $target $inventoryCommand
if ($LASTEXITCODE -ne 0) {
    throw 'No fue posible generar el inventario remoto.'
}
$inventory | Set-Content -LiteralPath $inventoryPath -Encoding utf8

$remoteSpec = '{0}:{1}' -f $target, $RemoteLinuxCncRoot
Write-Host "Copiando $remoteSpec ..."
& scp @sshOptions -p -r $remoteSpec $backupDirectory
if ($LASTEXITCODE -ne 0) {
    throw 'scp no pudo completar la copia. El directorio parcial se conserva para diagnóstico.'
}

$hashPath = Join-Path $backupDirectory 'sha256.txt'
$hashLines = Get-ChildItem -LiteralPath $backupDirectory -File -Recurse |
    Where-Object { $_.FullName -ne $hashPath } |
    Sort-Object FullName |
    ForEach-Object {
        $relativePath = [System.IO.Path]::GetRelativePath($backupDirectory, $_.FullName)
        $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$hash  $relativePath"
    }
$hashLines | Set-Content -LiteralPath $hashPath -Encoding ascii

Write-Host "Respaldo terminado: $backupDirectory"
