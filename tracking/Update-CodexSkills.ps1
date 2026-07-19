[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('user', 'project')]
    [string]$Scope,

    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetRoot,

    [Parameter(Mandatory = $true)]
    [string]$ManifestPath,

    [string]$Repository = 'https://github.com/ZAlan-dunk/Codex-Skills.git',
    [string]$Branch = 'main',
    [string]$ValidatorPath = (Join-Path $env:USERPROFILE '.codex\skills\.system\skill-creator\scripts\quick_validate.py'),
    [string]$PythonCommand = 'python',
    [switch]$SkipPull
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$skillMap = [ordered]@{
    'acsdm-project-catalog' = 'acsdm-project-catalog'
    'planning-to-requirements' = 'planning-to-requirements'
}

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
}

function Assert-ChildPath {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Parent
    )

    $fullPath = Get-FullPath -Path $Path
    $fullParent = Get-FullPath -Path $Parent
    $prefix = $fullParent + [System.IO.Path]::DirectorySeparatorChar
    if (-not $fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Safety check failed: '$fullPath' is not below '$fullParent'."
    }
}

function Remove-SafeTree {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$AllowedParent
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    Assert-ChildPath -Path $Path -Parent $AllowedParent
    Remove-Item -LiteralPath $Path -Recurse -Force
}

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)

    $safeRoot = (Get-FullPath -Path $SourceRoot).Replace('\', '/')
    $allArguments = @('-c', "safe.directory=$safeRoot", '-C', $SourceRoot) + $Arguments
    $output = & git @allArguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed:`n$($output -join [Environment]::NewLine)"
    }
    return $output
}

$SourceRoot = Get-FullPath -Path $SourceRoot
$TargetRoot = Get-FullPath -Path $TargetRoot
$ManifestPath = [System.IO.Path]::GetFullPath($ManifestPath)
$targetParent = Split-Path -Parent $TargetRoot
$manifestParent = Split-Path -Parent $ManifestPath

if (-not (Test-Path -LiteralPath (Join-Path $SourceRoot '.git'))) {
    throw "SourceRoot is not a Git clone: $SourceRoot"
}
if (-not (Test-Path -LiteralPath $ValidatorPath -PathType Leaf)) {
    throw "Codex skill validator was not found: $ValidatorPath"
}

New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
New-Item -ItemType Directory -Path $manifestParent -Force | Out-Null

$trackedChanges = @(Invoke-Git status --porcelain --untracked-files=no)
if ($trackedChanges.Count -gt 0 -and ($trackedChanges -join '').Trim().Length -gt 0) {
    throw "The tracking clone contains modified tracked files. Commit or discard them before updating:`n$($trackedChanges -join [Environment]::NewLine)"
}

$previousCommit = (Invoke-Git rev-parse HEAD | Select-Object -Last 1).Trim()

if (-not $SkipPull) {
    Invoke-Git fetch origin $Branch | Out-Null
    Invoke-Git checkout $Branch | Out-Null
    Invoke-Git pull --ff-only origin $Branch | Out-Null
}

$currentCommit = (Invoke-Git rev-parse HEAD | Select-Object -Last 1).Trim()
$stageRoot = Join-Path $targetParent ('.codex-skill-update-' + [Guid]::NewGuid().ToString('N'))
$backupRoot = Join-Path $targetParent ('.codex-skill-backup-' + [Guid]::NewGuid().ToString('N'))
$replacementLog = New-Object System.Collections.ArrayList

try {
    New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

    foreach ($skillName in $skillMap.Keys) {
        $relativeSource = $skillMap[$skillName]
        $sourceSkill = Join-Path $SourceRoot $relativeSource
        $stagedSkill = Join-Path $stageRoot $skillName

        if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill 'SKILL.md') -PathType Leaf)) {
            throw "Repository skill is missing SKILL.md: $sourceSkill"
        }

        Copy-Item -LiteralPath $sourceSkill -Destination $stagedSkill -Recurse -Force

        Get-ChildItem -LiteralPath $stagedSkill -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq '__pycache__' } |
            Sort-Object FullName -Descending |
            ForEach-Object { Remove-SafeTree -Path $_.FullName -AllowedParent $stageRoot }

        Get-ChildItem -LiteralPath $stagedSkill -File -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -in @('.pyc', '.pyo', '.tmp') -or $_.Name -in @('.DS_Store', 'Thumbs.db') } |
            Remove-Item -Force

        $oldPythonUtf8 = $env:PYTHONUTF8
        try {
            $env:PYTHONUTF8 = '1'
            $validationOutput = & $PythonCommand $ValidatorPath $stagedSkill 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Validation failed for '$skillName':`n$($validationOutput -join [Environment]::NewLine)"
            }
        }
        finally {
            $env:PYTHONUTF8 = $oldPythonUtf8
        }
    }

    foreach ($skillName in $skillMap.Keys) {
        $targetSkill = Join-Path $TargetRoot $skillName
        $stagedSkill = Join-Path $stageRoot $skillName
        $backupSkill = Join-Path $backupRoot $skillName
        $hadExisting = Test-Path -LiteralPath $targetSkill

        if ($hadExisting) {
            Move-Item -LiteralPath $targetSkill -Destination $backupSkill
        }

        [void]$replacementLog.Add([pscustomobject]@{
            Target = $targetSkill
            Backup = $backupSkill
            HadExisting = $hadExisting
        })

        Move-Item -LiteralPath $stagedSkill -Destination $targetSkill
    }

    $installedSkills = @()
    foreach ($skillName in $skillMap.Keys) {
        $installedSkills += [ordered]@{
            name = $skillName
            repository_path = $skillMap[$skillName]
            target_path = (Join-Path $TargetRoot $skillName)
        }
    }

    $manifest = [ordered]@{
        schema_version = 1
        repository = $Repository
        branch = $Branch
        scope = $Scope
        source_root = $SourceRoot
        target_root = $TargetRoot
        previous_commit = $previousCommit
        installed_commit = $currentCommit
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        skills = $installedSkills
    }
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
}
catch {
    for ($index = $replacementLog.Count - 1; $index -ge 0; $index--) {
        $item = $replacementLog[$index]
        if (Test-Path -LiteralPath $item.Target) {
            Remove-SafeTree -Path $item.Target -AllowedParent $TargetRoot
        }
        if ($item.HadExisting -and (Test-Path -LiteralPath $item.Backup)) {
            Move-Item -LiteralPath $item.Backup -Destination $item.Target
        }
    }
    throw
}
finally {
    Remove-SafeTree -Path $stageRoot -AllowedParent $targetParent
    Remove-SafeTree -Path $backupRoot -AllowedParent $targetParent
}

Write-Host "[$Scope] Codex skills updated successfully."
Write-Host "Repository commit: $currentCommit"
Write-Host "Target root: $TargetRoot"
Write-Host "Tracking manifest: $ManifestPath"
