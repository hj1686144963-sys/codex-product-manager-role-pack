[CmdletBinding()]
param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SkillsRoot = Join-Path $RepoRoot 'skills'
$CatalogPath = Join-Path $SkillsRoot 'CATALOG.json'
$RegistryPath = Join-Path $SkillsRoot 'REGISTRY.json'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-JsonFile([string]$Path) {
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-SkillFrontmatter([string]$SkillPath) {
    $text = Get-Content -LiteralPath $SkillPath -Raw -Encoding UTF8
    $match = [regex]::Match($text, '(?s)\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n')
    if (-not $match.Success) {
        throw "Missing YAML frontmatter: $SkillPath"
    }
    $values = @{}
    foreach ($line in ($match.Groups[1].Value -split '\r?\n')) {
        if ($line -match '^([A-Za-z0-9_-]+):\s*(.*)$') {
            $values[$matches[1]] = $matches[2].Trim().Trim('"').Trim("'")
        }
    }
    return $values
}

function Get-SkillTreeHash([string]$Path) {
    $base = $Path.TrimEnd('\')
    $rows = foreach ($file in (Get-ChildItem -LiteralPath $base -File -Recurse | Sort-Object FullName)) {
        $relative = $file.FullName.Substring($base.Length).TrimStart('\').Replace('\', '/')
        $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$relative`t$hash"
    }
    $bytes = [System.Text.Encoding]::UTF8.GetBytes(($rows -join "`n"))
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function New-RegistryPayload {
    $catalog = Read-JsonFile $CatalogPath
    if ($catalog.schema_version -ne 1) {
        throw 'skills/CATALOG.json schema_version must be 1'
    }

    $folderNames = @(Get-ChildItem -LiteralPath $SkillsRoot -Directory | Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
    } | ForEach-Object Name | Sort-Object)
    $catalogNames = @($catalog.skills | ForEach-Object name | Sort-Object)
    if (($folderNames -join "`n") -ne ($catalogNames -join "`n")) {
        throw "Catalog and Skill folders differ. Folders=[$($folderNames -join ', ')] Catalog=[$($catalogNames -join ', ')]"
    }

    $items = foreach ($item in $catalog.skills) {
        $skillFolder = Join-Path $SkillsRoot $item.name
        $skillPath = Join-Path $skillFolder 'SKILL.md'
        $frontmatter = Get-SkillFrontmatter $skillPath
        if ($frontmatter.name -ne $item.name) {
            throw "$($item.name): SKILL.md name is '$($frontmatter.name)'"
        }
        if ([string]::IsNullOrWhiteSpace($frontmatter.description)) {
            throw "$($item.name): SKILL.md description is empty"
        }

        $entry = [ordered]@{
            name = $item.name
            version = $item.version
            status = $item.status
            category = $item.category
            risk = $item.risk
            capability_summary = $item.capability_summary
            route_description = $frontmatter.description
            capabilities = @($item.capabilities)
            source = $item.source
            skill_sha256 = Get-SkillTreeHash $skillFolder
            capability_manual = "docs/skill-capabilities/$($item.name).md"
        }
        if ($item.PSObject.Properties.Name -contains 'adaptation_notes') {
            $entry.adaptation_notes = $item.adaptation_notes
        }
        $entry.merged_from = @($item.merged_from)
        $entry.merge_notes = $item.merge_notes
        $entry.successor = $item.successor
        [pscustomobject]$entry
    }

    return [ordered]@{
        schema_version = 3
        generated = $true
        generated_from = 'skills/CATALOG.json + skills/*/SKILL.md'
        generated_by = 'scripts/Generate-SkillRegistry.ps1'
        governance = [ordered]@{
            capability_docs_required = $true
            capability_docs_generator = 'scripts/Generate-SkillCapabilityDocs.ps1'
            merge_lineage_required = $true
            routing_tests_required = $true
            routing_tests = 'evaluations/skill-routing-cases.json'
            default_docs_path = 'docs/skill-capabilities'
        }
        category_taxonomy = $catalog.category_taxonomy
        skills = @($items)
    }
}

$json = ((New-RegistryPayload) | ConvertTo-Json -Depth 12) + "`n"
if ($Check) {
    $current = if (Test-Path -LiteralPath $RegistryPath) {
        Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8
    } else {
        ''
    }
    if ($current -cne $json) {
        Write-Error 'skills/REGISTRY.json is missing or stale. Run scripts/Generate-SkillRegistry.ps1.'
        exit 1
    }
} else {
    Write-Utf8NoBom $RegistryPath $json
}

[pscustomobject]@{
    status = 'pass'
    check = [bool]$Check
    skills = @((Read-JsonFile $CatalogPath).skills).Count
    output = $RegistryPath
} | ConvertTo-Json -Compress

