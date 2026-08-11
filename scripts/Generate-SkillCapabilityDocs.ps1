[CmdletBinding()]
param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$RegistryPath = Join-Path $RepoRoot 'skills\REGISTRY.json'
$DocsRoot = Join-Path $RepoRoot 'docs\skill-capabilities'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-SourceLines($Source) {
    $rows = @("- 来源类型：$($Source.type)")
    if ($Source.repo) { $rows += "- 来源仓库：https://github.com/$($Source.repo)" }
    if ($Source.commit) { $rows += "- 固定提交：``$($Source.commit)``" }
    if ($Source.path) { $rows += "- 来源路径：``$($Source.path)``" }
    if ($Source.license) { $rows += "- 许可证：$($Source.license)" }
    return $rows
}

function Render-Manual($Item) {
    $capabilities = @($Item.capabilities | ForEach-Object { "- $_" }) -join "`n"
    $source = @(Get-SourceLines $Item.source) -join "`n"
    $merged = if (@($Item.merged_from).Count -eq 0) {
        '- 无；这是独立 Skill，不是同类 Skill 合并产物。'
    } else {
        @($Item.merged_from | ForEach-Object { "- ``$($_.name)`` $($_.version)" }) -join "`n"
    }
    $mergeNotes = if ($Item.merge_notes) { $Item.merge_notes } else { '不适用。' }
    $successor = if ($Item.successor) { $Item.successor } else { '无' }
    return @"
<!-- GENERATED FILE. DO NOT EDIT. Source: skills/REGISTRY.json -->
# Skill 能力说明：$($Item.name)

- 版本：``$($Item.version)``
- 生命周期：``$($Item.status)``
- 主分类：``$($Item.category)``
- 风险级别：``$($Item.risk)``
- 执行定义：``skills/$($Item.name)/SKILL.md``
- 内容哈希：``$($Item.skill_sha256)``

## 一句话机器路由

$($Item.capability_summary)

## Codex 实际触发描述

$($Item.route_description)

## 核心能力

$capabilities

## 来源与版本证据

$source

## 合并血缘

$merged

## 合并说明

$mergeNotes

## 替代关系

- 后继 Skill：$successor

## 维护规则

- 本文由 ``scripts/Generate-SkillCapabilityDocs.ps1`` 生成，不得手工编辑。
- 行为变化先修改 ``SKILL.md``；治理元数据先修改 ``skills/CATALOG.json``，然后重新生成 Registry 和本文。
- 安装、合并、废弃或回滚必须保留来源版本、哈希和验证证据。
"@
}

function Render-Index($Items, $Taxonomy) {
    $rows = @(
        '<!-- GENERATED FILE. DO NOT EDIT. Source: skills/REGISTRY.json -->',
        '# Skill 能力索引',
        '',
        '路由时先扫描“一句话机器路由”；命中后再打开对应 `SKILL.md` 和能力说明。',
        '',
        '## 分类说明',
        ''
    )
    foreach ($property in $Taxonomy.PSObject.Properties) {
        $rows += "- ``$($property.Name)``：$($property.Value)"
    }
    $rows += @('', '## Skill 清单', '', '| 分类 | Skill | 状态 | 风险 | 一句话机器路由 |', '|---|---|---|---|---|')
    foreach ($item in ($Items | Sort-Object category, name)) {
        $summary = $item.capability_summary.Replace('|', '\|')
        $rows += "| ``$($item.category)`` | [$($item.name)]($($item.name).md) | ``$($item.status)`` | ``$($item.risk)`` | $summary |"
    }
    return ($rows -join "`n") + "`n"
}

$registry = Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expected = @{}
foreach ($item in $registry.skills) {
    $expected[(Join-Path $DocsRoot "$($item.name).md")] = Render-Manual $item
}
$expected[(Join-Path $DocsRoot '00_能力索引.generated.md')] = Render-Index $registry.skills $registry.category_taxonomy

$stale = @()
foreach ($path in $expected.Keys) {
    if ($Check) {
        $current = if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw -Encoding UTF8 } else { '' }
        if ($current -cne $expected[$path]) { $stale += $path }
    } else {
        if (-not (Test-Path -LiteralPath $DocsRoot)) { New-Item -ItemType Directory -Path $DocsRoot | Out-Null }
        Write-Utf8NoBom $path $expected[$path]
    }
}

if ($stale.Count -gt 0) {
    $relative = @($stale | ForEach-Object { $_.Substring($RepoRoot.Length + 1).Replace('\', '/') })
    [pscustomobject]@{status='fail'; stale=$relative} | ConvertTo-Json -Depth 3
    exit 1
}

[pscustomobject]@{status='pass'; check=[bool]$Check; files=$expected.Count} | ConvertTo-Json -Compress

