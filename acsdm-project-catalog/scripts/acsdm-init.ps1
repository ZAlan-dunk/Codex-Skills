param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Get-AcsdmModules {
    @(
        [pscustomobject]@{ Name='00Rule'; Index='0000Index.md'; Purpose='项目架构、项目规则、自研框架规则、Lua/C# 交互规则、全项目通用但与常规不同的操作方式。'; Keywords='规则,规范,框架,Lua,C#,导表,UI框架,弹窗,道具弹窗' },
        [pscustomobject]@{ Name='01ProjectOverview'; Index='0100Index.md'; Purpose='项目总览、游戏规则、玩法、大体功能、主干脚本路径、快速检索说明。'; Keywords='项目总览,玩法,游戏规则,主干脚本,快速了解,功能列表' },
        [pscustomobject]@{ Name='02LevelEditor'; Index='0200Index.md'; Purpose='关卡编辑器相关方案、工具说明、编辑器实现、调整日志。'; Keywords='关卡编辑器,编辑器工具,像素图,难度,数独算法' },
        [pscustomobject]@{ Name='03LevelLoading'; Index='0300Index.md'; Purpose='游戏关卡加载链路、地图加载、颜色方块加载、预览图加载、加载优化。'; Keywords='关卡加载,地图加载,颜色方块,预览图,加载链路' },
        [pscustomobject]@{ Name='04PlayerInput'; Index='0400Index.md'; Purpose='用户输入系统、拖拽填充、交互流程、输入相关修复记录。'; Keywords='输入,拖拽,DragFill,交互,填充,手势' },
        [pscustomobject]@{ Name='05PropSystem'; Index='0500Index.md'; Purpose='道具系统、道具解锁、消除错误道具、回退道具、道具弹窗。'; Keywords='道具,回退,消除错误,道具解锁,道具弹窗' },
        [pscustomobject]@{ Name='06Review'; Index='0600Index.md'; Purpose='项目开发功能审查、实现审查、审查清单、风险对照。'; Keywords='审查,review,检查清单,风险,验收' },
        [pscustomobject]@{ Name='07ADMD'; Index='0700Index.md'; Purpose='广告接入、埋点接入、数据统计、广告/埋点相关规则和实现记录。'; Keywords='广告,埋点,AD,打点,Analytics,统计' },
        [pscustomobject]@{ Name='08OUFDevelopmentLogs'; Index='0800Index.md'; Purpose='连接 Orange Unity Forge 保存在 docs/forge-artifacts 下的功能开发日志、Context Brief、SDD、Plan、Report、Evidence，只保存索引不复制正文。'; Keywords='OUF,Orange,Forge,开发日志,SDD,Context Brief,Plan,Report,Evidence,功能历史' }
    )
}

function New-ModuleIndexContent($module) {
@"
# $($module.Index -replace '\.md$','') $($module.Name)

## 命名规范

本目录使用 `<模块编号><文档编号><文档主题>.md` 命名。
`xx00Index.md` 为本目录索引，新增文档从 `xx01` 递增。
检索时先读根索引，再读本模块索引，最后只读取与任务直接相关的 md 文档。

## 检索方法

1. 先通过关键词定位模块。
2. 读取本索引的用途、脚本、方法、行号字段。
3. 只打开与当前需求直接相关的 md 文档。
4. 不进行全目录正文读取。

## 模块用途

$($module.Purpose)

## 文档索引

| md 文件名 | 加入时间 | 最新修改时间 | 用途 | 涉及脚本名称 | 脚本简要功能说明 | 涉及方法名称 | 涉及行数 | 检索关键词 | 记录类型 |
|---|---|---|---|---|---|---|---|---|---|
"@
}

function New-RootIndexContent($catalogRoot, $modules) {
    $lines = @()
    $lines += '# 0000 ACSDM Root Index'
    $lines += ''
    $lines += '## 命名规范'
    $lines += ''
    $lines += '使用 `<模块编号><文档编号><文档主题>.md`。`xx00Index.md` 为模块索引。'
    $lines += ''
    $lines += '## 检索方法'
    $lines += ''
    $lines += '先读根索引，再读模块索引，最后只读取与任务直接相关的 md 文档。'
    $lines += ''
    $lines += '## 模块总览'
    $lines += ''
    $lines += '| 模块 | 用途 | 索引文件 | 关键词 | 文档数量 | 更新时间 |'
    $lines += '|---|---|---|---|---:|---|'
    foreach ($module in $modules) {
        $moduleDir = Join-Path $catalogRoot $module.Name
        $docCount = 0
        $updated = ''
        if (Test-Path -LiteralPath $moduleDir -PathType Container) {
            $docCount = @(Get-ChildItem -LiteralPath $moduleDir -File -Filter '*.md' -Force).Count
            $updated = (Get-Item -LiteralPath $moduleDir).LastWriteTime.ToString('s')
        }
        $lines += "| ``$($module.Name)`` | $($module.Purpose) | ``$($module.Index)`` | $($module.Keywords) | $docCount | $updated |"
    }
    $lines += ''
    $lines += '## 模块映射兼容表'
    $lines += ''
    $lines += '| 当前目录 | 标准目录 | 说明 |'
    $lines += '|---|---|---|'
    $lines += ''
    $lines += '## 最近更新'
    $lines += ''
    $lines += "- $(Get-Date -Format s): initialized or repaired by acsdm-init.ps1"
    return $lines
}

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Project root not found: $ProjectRoot"
}

$projectRootItem = Get-Item -LiteralPath $ProjectRoot
$catalogRoot = Join-Path $projectRootItem.FullName '.ACSDM'
New-Item -ItemType Directory -Force -Path $catalogRoot | Out-Null

$modules = Get-AcsdmModules
foreach ($module in $modules) {
    $moduleDir = Join-Path $catalogRoot $module.Name
    New-Item -ItemType Directory -Force -Path $moduleDir | Out-Null
    $indexPath = Join-Path $moduleDir $module.Index
    if ($Force -or -not (Test-Path -LiteralPath $indexPath -PathType Leaf)) {
        Set-Content -Path $indexPath -Value (New-ModuleIndexContent $module) -Encoding UTF8
    }
}

$rootIndexPath = Join-Path $catalogRoot '0000ACSDMRootIndex.md'
if ($Force -or -not (Test-Path -LiteralPath $rootIndexPath -PathType Leaf)) {
    Set-Content -Path $rootIndexPath -Value (New-RootIndexContent $catalogRoot $modules) -Encoding UTF8
}

$gitExclude = Join-Path $projectRootItem.FullName '.git\info\exclude'
$gitInfoDir = Split-Path $gitExclude -Parent
if (Test-Path -LiteralPath $gitInfoDir -PathType Container) {
    if (-not (Test-Path -LiteralPath $gitExclude -PathType Leaf)) {
        New-Item -ItemType File -Force -Path $gitExclude | Out-Null
    }
    $excludeContent = Get-Content -LiteralPath $gitExclude -ErrorAction SilentlyContinue
    if ($excludeContent -notcontains '.ACSDM/') {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        $prefix = if ((Get-Item -LiteralPath $gitExclude).Length -gt 0) { [Environment]::NewLine } else { '' }
        [System.IO.File]::AppendAllText($gitExclude, "$prefix.ACSDM/$([Environment]::NewLine)", $utf8NoBom)
    }
}

Write-Output "ACSDM catalog root: $catalogRoot"
Write-Output "Root index: $rootIndexPath"
Write-Output "Standard modules: $($modules.Count)"