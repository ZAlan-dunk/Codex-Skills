param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [string]$ForgeArtifactsRoot = '',

    [string]$CatalogRoot = ''
)

$ErrorActionPreference = 'Stop'

function ConvertTo-RelativePath {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )
    $base = [System.IO.Path]::GetFullPath($BasePath)
    if (-not $base.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $base += [System.IO.Path]::DirectorySeparatorChar
    }
    $target = [System.IO.Path]::GetFullPath($TargetPath)
    $baseUri = [System.Uri]::new($base)
    $targetUri = [System.Uri]::new($target)
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Escape-MarkdownCell {
    param([AllowNull()][string]$Value)
    if ($null -eq $Value) { return '' }
    return ($Value -replace '\|', '\|' -replace "`r?`n", ' ' -replace '\s+', ' ').Trim()
}

function Get-ArtifactType {
    param([string]$RelativePath)
    $lower = $RelativePath.ToLowerInvariant()
    if ($lower -match 'brief|context') { return 'context-brief' }
    if ($lower -match 'spec|sdd') { return 'sdd' }
    if ($lower -match 'plan') { return 'plan' }
    if ($lower -match 'report') { return 'report' }
    if ($lower -match 'evidence') { return 'evidence' }
    if ($lower -match 'bug|fix') { return 'bug-report' }
    if ($lower -match 'verify|verification|test|qa') { return 'verification' }
    if ($lower -match 'log|journal') { return 'log' }
    return 'other'
}

function Get-FirstMatchOrEmpty {
    param([string]$Text, [string]$Pattern)
    $m = [regex]::Match($Text, $Pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($m.Success) { return $m.Groups[1].Value.Trim() }
    return ''
}

$projectRootItem = Get-Item -LiteralPath $ProjectRoot
$resolvedProjectRoot = $projectRootItem.FullName
if ([string]::IsNullOrWhiteSpace($ForgeArtifactsRoot)) {
    $ForgeArtifactsRoot = Join-Path $resolvedProjectRoot 'docs\forge-artifacts'
}
if ([string]::IsNullOrWhiteSpace($CatalogRoot)) {
    $CatalogRoot = Join-Path $resolvedProjectRoot '.ACSDM'
}

if (-not (Test-Path -LiteralPath $ForgeArtifactsRoot -PathType Container)) {
    throw "OUF artifact root not found: $ForgeArtifactsRoot"
}

$moduleRoot = Join-Path $CatalogRoot '08OUFDevelopmentLogs'
New-Item -ItemType Directory -Force -Path $moduleRoot | Out-Null
$indexPath = Join-Path $moduleRoot '0800Index.md'

$files = Get-ChildItem -LiteralPath $ForgeArtifactsRoot -Recurse -File -Force |
    Where-Object { $_.Extension.ToLowerInvariant() -in @('.md', '.markdown', '.txt', '.json') } |
    Sort-Object FullName

$rows = @()
foreach ($file in $files) {
    $relative = ConvertTo-RelativePath -BasePath $resolvedProjectRoot -TargetPath $file.FullName
    $artifactRelative = ConvertTo-RelativePath -BasePath $ForgeArtifactsRoot -TargetPath $file.FullName
    $text = ''
    try {
        $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    } catch {
        $text = ''
    }
    $fullId = Get-FirstMatchOrEmpty -Text ($relative + "`n" + $text) -Pattern '(\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*-F\d{3})'
    $baseId = Get-FirstMatchOrEmpty -Text ($relative + "`n" + $text) -Pattern '(?<![A-Z0-9-])([A-Z][A-Z0-9-]*-F\d{3})(?![A-Z0-9-])'
    $version = Get-FirstMatchOrEmpty -Text ($relative + "`n" + $text) -Pattern '(M\d{3}v\d+(?:\.\d+)*)'
    $title = Get-FirstMatchOrEmpty -Text $text -Pattern '^#\s+(.+)$'
    if ([string]::IsNullOrWhiteSpace($title)) {
        $title = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    }
    $summary = ''
    foreach ($line in ($text -split "`r?`n")) {
        $candidate = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if ($candidate.StartsWith('#')) { continue }
        if ($candidate.StartsWith('|')) { continue }
        $summary = $candidate
        break
    }
    if ($summary.Length -gt 90) { $summary = $summary.Substring(0, 90) + '…' }
    $type = Get-ArtifactType -RelativePath $artifactRelative
    $scenario = switch ($type) {
        'context-brief' { '快速了解功能背景和开发上下文' }
        'sdd' { '读取详细技术方案或程序确认内容' }
        'plan' { '查看实施步骤、风险、回滚和验证计划' }
        'report' { '回看实现结果、变更摘要和完成情况' }
        'evidence' { '核对证据、测试记录或命令输出' }
        'bug-report' { '定位 Bug 分析、修复链路和复测依据' }
        'verification' { '查看验证、测试和 QA 结论' }
        'log' { '追踪开发过程和决策流水' }
        default { '按功能主题补充阅读' }
    }
    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $rows += [pscustomobject]@{
        FullId = $fullId
        BaseId = $baseId
        Version = $version
        Title = $title
        Type = $type
        Path = $relative
        Summary = $summary
        Updated = $file.LastWriteTime.ToString('s')
        Hash = $hash
        Scenario = $scenario
    }
}

$lines = @()
$lines += '# 0800 OUF Development Logs Link Index'
$lines += ''
$lines += '> ACSDM connector index. OUF owns the original files under `docs/forge-artifacts/`; this file stores paths, hashes, and compact summaries only.'
$lines += ''
$lines += "Generated at: $(Get-Date -Format s)"
$lines += 'Project root: `' + $resolvedProjectRoot + '`'
$lines += 'OUF artifact root: `' + $ForgeArtifactsRoot + '`'
$lines += ''
$lines += '## 检索方法'
$lines += ''
$lines += '1. 先按 PCTR Feature ID 或 Base Feature ID 过滤。'
$lines += '2. 再按 OUF 产物类型选择：context-brief / sdd / plan / report / evidence / log / bug-report / verification / other。'
$lines += '3. 只打开与当前任务直接相关的原始 OUF 文件，不把 OUF 正文复制进 ACSDM。'
$lines += ''
$lines += '## OUF 产物索引'
$lines += ''
$lines += '| PCTR Feature ID | Base Feature ID | 策案版本 | 功能名称 | OUF 产物类型 | OUF 路径 | 摘要 | 更新时间 | Hash | 推荐读取场景 |'
$lines += '|---|---|---|---|---|---|---|---|---|---|'
foreach ($row in $rows) {
    $cells = @(
        (Escape-MarkdownCell $row.FullId),
        (Escape-MarkdownCell $row.BaseId),
        (Escape-MarkdownCell $row.Version),
        (Escape-MarkdownCell $row.Title),
        (Escape-MarkdownCell $row.Type),
        ('`' + (Escape-MarkdownCell $row.Path) + '`'),
        (Escape-MarkdownCell $row.Summary),
        (Escape-MarkdownCell $row.Updated),
        ('`' + $row.Hash + '`'),
        (Escape-MarkdownCell $row.Scenario)
    )
    $lines += '| ' + ($cells -join ' | ') + ' |'
}

Set-Content -LiteralPath $indexPath -Value $lines -Encoding UTF8
Write-Output "Linked $($rows.Count) OUF artifacts into: $indexPath"
