param(
    [string]$VaultRoot = (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Codex-Obsidian-Vault-Product-Manager'),
    [switch]$IncludeDashiLocalFolders
)

$ErrorActionPreference = 'Stop'

$vaultFolders = @(
    '00-Home',
    '00-Inbox',
    '10-Sources',
    '20-Concepts',
    '30-Methods',
    '40-Projects',
    '50-Outputs',
    '60-Reviews',
    '90-System',
    '90-System\Templates'
)

$created = [System.Collections.Generic.List[string]]::new()
$existing = [System.Collections.Generic.List[string]]::new()

foreach ($relative in $vaultFolders) {
    $path = Join-Path $VaultRoot $relative
    if (Test-Path -LiteralPath $path) {
        $existing.Add($path)
    } else {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        $created.Add($path)
    }
}

$dashiRoot = $null
if ($IncludeDashiLocalFolders) {
    $dashiRoot = Join-Path $env:LOCALAPPDATA 'CodexWorkbench\Dashi'
    foreach ($relative in @('config', 'data', 'backups', 'logs', 'runtime', 'staging')) {
        $path = Join-Path $dashiRoot $relative
        if (Test-Path -LiteralPath $path) {
            $existing.Add($path)
        } else {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            $created.Add($path)
        }
    }
}

[pscustomobject]@{
    status = 'ok'
    vault_root = [System.IO.Path]::GetFullPath($VaultRoot)
    dashi_root = $dashiRoot
    created = $created
    existing = $existing
} | ConvertTo-Json -Depth 4
