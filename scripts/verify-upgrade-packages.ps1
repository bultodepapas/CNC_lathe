[CmdletBinding()]
param(
    [string]$PackageRoot = (Join-Path $PSScriptRoot '..\backups\upgrade-packages')
)

$ErrorActionPreference = 'Stop'

$expected = @(
    # 2.9.10: official GitHub release files; identical hashes are published by
    # the official Bookworm 2.9-uspace APT package index.
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-doc-de_2.9.10_all_bookworm.deb'; Size = 26639908; Sha256 = '281a43e355df78c063f4045e4192aa42fe2dcb4c4106dcd627a77945ace2ccaa' }
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-doc-en_2.9.10_all_bookworm.deb'; Size = 27224432; Sha256 = '8e729dec3dfdc0df4f64f10087ab7b2edf7d6e0aeff8b44ffa9cc0573e55b27d' }
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-doc-es_2.9.10_all_bookworm.deb'; Size = 26369832; Sha256 = '01a08eae108578903eea8f8990afa3089117b5620e8e05f7be4a708342aba33c' }
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-doc-fr_2.9.10_all_bookworm.deb'; Size = 26287408; Sha256 = '633969ddee40aabd371c3547c03f5eb36d3ee99008796d2a8926c675453a1982' }
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-uspace_2.9.10_amd64_bookworm.deb'; Size = 25665664; Sha256 = '09c8d93ed6ddb197a57695e473a7fb6d930fd17cffb77d8f0fa24f2a79b561b2' }
    [pscustomobject]@{ Channel = 'github-release'; Version = '2.9.10'; File = 'linuxcnc-uspace-dev_2.9.10_amd64_bookworm.deb'; Size = 276380; Sha256 = 'cd6e609d04f973ab402dd30b09186136beb68807d46f5628bdbf03cbfa56d8ae' }

    # 2.9.7: exact files from the official Bookworm APT repository. These are
    # intentionally different from the same-version GitHub release rebuilds.
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-doc-de_2.9.7_all.deb'; Size = 26418960; Sha256 = 'f371cfd3cd1a65155fd1a0292755cc565aa004b8bc3f124464988a11a12960a0' }
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-doc-en_2.9.7_all.deb'; Size = 26995856; Sha256 = '0600cb3cfb83105810a8e02d3fe3472291ff4cb2f0362481d0030453eb22ebf2' }
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-doc-es_2.9.7_all.deb'; Size = 26143948; Sha256 = 'ed00d12c0a2ea49b15bc483df95eee681bd3119c4ee1ea25fbe0df44230d10d0' }
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-doc-fr_2.9.7_all.deb'; Size = 26064672; Sha256 = '37cd3df7829271412f74e31997f53c7104bdb5dda43322f630e9a19fec43b563' }
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-uspace_2.9.7_amd64.deb'; Size = 25672688; Sha256 = 'db2528514b986ca12c194f6c171a081124930d7df0ea87017ac10cc4ce12d1c2' }
    [pscustomobject]@{ Channel = 'apt-repository'; Version = '2.9.7-repo'; File = 'linuxcnc-uspace-dev_2.9.7_amd64.deb'; Size = 273812; Sha256 = '3083df1ef53a8d91acf89762d67831a121f7ff183e385c637b8e5f4d04fd4dc1' }
)

$resolvedRoot = [System.IO.Path]::GetFullPath($PackageRoot)
$failures = [System.Collections.Generic.List[string]]::new()
$results = foreach ($item in $expected) {
    $directory = if ($item.Version -eq '2.9.7-repo') { 'v2.9.7-repo' } else { "v$($item.Version)" }
    $path = Join-Path (Join-Path $resolvedRoot $directory) $item.File

    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $failures.Add("Falta: $path")
        [pscustomobject]@{ Version = $item.Version; File = $item.File; Status = 'MISSING'; Bytes = $null; Sha256 = $null }
        continue
    }

    $file = Get-Item -LiteralPath $path
    $digest = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    $sizeOk = $file.Length -eq $item.Size
    $hashOk = $digest -eq $item.Sha256
    if (-not $sizeOk) { $failures.Add("Tamaño inesperado: $path ($($file.Length), esperado $($item.Size))") }
    if (-not $hashOk) { $failures.Add("SHA-256 inesperado: $path ($digest)") }

    [pscustomobject]@{
        Version = $item.Version
        File = $item.File
        Status = if ($sizeOk -and $hashOk) { 'OK' } else { 'FAIL' }
        Bytes = $file.Length
        Sha256 = $digest
    }
}

$results | Format-Table Version, Status, Bytes, File -AutoSize
if ($failures.Count -gt 0) {
    foreach ($failure in $failures) { Write-Error $failure -ErrorAction Continue }
    exit 1
}

Write-Host "OK: $($results.Count) paquetes oficiales disponibles y verificados."
Write-Host 'Cobertura: upgrade completo 2.9.10 y rollback exacto APT 2.9.7.'
exit 0
