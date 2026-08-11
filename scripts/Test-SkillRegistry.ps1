[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$CatalogPath = Join-Path $RepoRoot 'skills\CATALOG.json'
$RegistryPath = Join-Path $RepoRoot 'skills\REGISTRY.json'
$errors = @()

& (Join-Path $PSScriptRoot 'Generate-SkillRegistry.ps1') -Check | Out-Null
$catalog = Get-Content -LiteralPath $CatalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
$registry = Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json

if ($registry.schema_version -ne 3) { $errors += 'REGISTRY schema_version must be 3' }
if (-not $registry.generated) { $errors += 'REGISTRY must be marked generated' }
$allowedStatuses = @('draft','candidate','active','deprecated','retired')
$allowedRisks = @('read-only','local-write','external-write','high-impact')
$allowedCategories = @($catalog.category_taxonomy.PSObject.Properties.Name)
$names = @($registry.skills | ForEach-Object name)
if (@($names | Select-Object -Unique).Count -ne $names.Count) { $errors += 'duplicate Skill names' }

foreach ($item in $registry.skills) {
    if ($allowedStatuses -notcontains $item.status) { $errors += "$($item.name): invalid status $($item.status)" }
    if ($allowedRisks -notcontains $item.risk) { $errors += "$($item.name): invalid risk $($item.risk)" }
    if ($allowedCategories -notcontains $item.category) { $errors += "$($item.name): unknown category $($item.category)" }
    if ([string]::IsNullOrWhiteSpace($item.capability_summary)) { $errors += "$($item.name): empty capability_summary" }
    if ([string]::IsNullOrWhiteSpace($item.route_description)) { $errors += "$($item.name): empty route_description" }
    if (@($item.capabilities).Count -eq 0) { $errors += "$($item.name): capabilities must not be empty" }
    if ($item.skill_sha256 -notmatch '^[a-f0-9]{64}$') { $errors += "$($item.name): invalid skill_sha256" }
    if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "skills\$($item.name)\SKILL.md"))) { $errors += "$($item.name): missing SKILL.md" }
    if (@($item.merged_from).Count -gt 0 -and [string]::IsNullOrWhiteSpace($item.merge_notes)) { $errors += "$($item.name): merged Skill requires merge_notes" }
    foreach ($origin in @($item.merged_from)) {
        if ($names -notcontains $origin.name) { $errors += "$($item.name): unknown merged_from Skill $($origin.name)" }
        if ([string]::IsNullOrWhiteSpace($origin.version)) { $errors += "$($item.name): merged_from version is required" }
    }
    if (@('deprecated','retired') -contains $item.status -and [string]::IsNullOrWhiteSpace($item.successor)) { $errors += "$($item.name): deprecated or retired Skill requires successor" }
}

& (Join-Path $PSScriptRoot 'Generate-SkillCapabilityDocs.ps1') -Check | Out-Null

[ordered]@{
    status = if ($errors.Count -eq 0) { 'pass' } else { 'fail' }
    skills = $registry.skills.Count
    categories = $allowedCategories.Count
    errors = $errors
} | ConvertTo-Json -Depth 5
if ($errors.Count -gt 0) { exit 1 }

