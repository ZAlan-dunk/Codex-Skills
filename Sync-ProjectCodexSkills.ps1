[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [string]$Branch = 'main',

    [switch]$Yes,

    [switch]$CheckOnly,

    [switch]$SkipPull,

    [Parameter(Mandatory = $true)]
    [string]$WorkRoot
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

    $safeRoot = $script:SourceRoot.Replace('\', '/')
    $allArguments = @('-c', "safe.directory=$safeRoot", '-C', $script:SourceRoot) + $Arguments
    $oldErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $output = & git @allArguments 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $oldErrorActionPreference
    }
    if ($exitCode -ne 0) {
        throw "git $($Arguments -join ' ') failed:`n$($output -join [Environment]::NewLine)"
    }
    return @($output | ForEach-Object { "$_" })
}

function Get-RelativePath {
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
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', '\')
}

function Test-IgnoredFile {
    param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

    if ($File.Extension -in @('.pyc', '.pyo', '.tmp')) { return $true }
    if ($File.Name -in @('.DS_Store', 'Thumbs.db')) { return $true }
    foreach ($part in ($File.FullName -split '[\\/]')) {
        if ($part -eq '__pycache__') { return $true }
    }
    return $false
}

function Get-TreeFileMap {
    param([Parameter(Mandatory = $true)][string]$Root)

    $map = @{}
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        return $map
    }

    Get-ChildItem -LiteralPath $Root -Recurse -File -Force |
        Where-Object { -not (Test-IgnoredFile -File $_) } |
        ForEach-Object {
            $relative = (Get-RelativePath -BasePath $Root -TargetPath $_.FullName).Replace('\', '/')
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $map[$relative] = $hash
        }
    return $map
}

function Compare-TreeMaps {
    param(
        [Parameter(Mandatory = $true)][hashtable]$SourceMap,
        [Parameter(Mandatory = $true)][hashtable]$TargetMap
    )

    $added = New-Object System.Collections.ArrayList
    $modified = New-Object System.Collections.ArrayList
    $removed = New-Object System.Collections.ArrayList

    foreach ($path in ($SourceMap.Keys | Sort-Object)) {
        if (-not $TargetMap.ContainsKey($path)) {
            [void]$added.Add($path)
        }
        elseif ($SourceMap[$path] -ne $TargetMap[$path]) {
            [void]$modified.Add($path)
        }
    }
    foreach ($path in ($TargetMap.Keys | Sort-Object)) {
        if (-not $SourceMap.ContainsKey($path)) {
            [void]$removed.Add($path)
        }
    }

    return [pscustomobject]@{
        Added = @($added)
        Modified = @($modified)
        Removed = @($removed)
        HasDiff = ($added.Count -gt 0 -or $modified.Count -gt 0 -or $removed.Count -gt 0)
    }
}

function Format-DiffList {
    param(
        [Parameter(Mandatory = $true)][string]$SkillName,
        [Parameter(Mandatory = $true)]$Diff,
        [int]$Limit = 80
    )

    $lines = New-Object System.Collections.ArrayList
    [void]$lines.Add("Skill: $SkillName")
    foreach ($group in @(
        @{ Label = 'Added in source'; Items = $Diff.Added },
        @{ Label = 'Modified'; Items = $Diff.Modified },
        @{ Label = 'Extra in project target'; Items = $Diff.Removed }
    )) {
        $items = @($group.Items)
        if ($items.Count -eq 0) { continue }
        [void]$lines.Add("  [$($group.Label)] $($items.Count)")
        foreach ($item in ($items | Select-Object -First $Limit)) {
            [void]$lines.Add("    - $item")
        }
        if ($items.Count -gt $Limit) {
            [void]$lines.Add("    ... and $($items.Count - $Limit) more")
        }
    }
    return @($lines)
}

function Copy-TrackedSkillToStage {
    param(
        [Parameter(Mandatory = $true)][string]$SkillSourceName,
        [Parameter(Mandatory = $true)][string]$StageRoot
    )

    $files = @(Invoke-Git ls-files -- $SkillSourceName)
    if ($files.Count -eq 0) {
        throw "No version-controlled files found for skill: $SkillSourceName"
    }

    foreach ($relativeGitPath in $files) {
        $relativeLocal = $relativeGitPath.Replace('/', '\')
        $sourceFile = Join-Path $script:SourceRoot $relativeLocal
        $targetFile = Join-Path $StageRoot $relativeLocal
        $targetParent = Split-Path -Parent $targetFile
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
        Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
    }

    $stagedSkill = Join-Path $StageRoot $SkillSourceName
    if (-not (Test-Path -LiteralPath (Join-Path $stagedSkill 'SKILL.md') -PathType Leaf)) {
        throw "Staged skill is missing SKILL.md: $stagedSkill"
    }
}

function Assert-SameTreeHash {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target
    )

    $sourceMap = Get-TreeFileMap -Root $Source
    $targetMap = Get-TreeFileMap -Root $Target
    $diff = Compare-TreeMaps -SourceMap $sourceMap -TargetMap $targetMap
    if ($diff.HasDiff) {
        throw "Tree verification failed after sync: '$Source' != '$Target'."
    }
}

$script:SourceRoot = Get-FullPath -Path $PSScriptRoot
$ProjectRoot = Get-FullPath -Path $ProjectRoot
$WorkRoot = Get-FullPath -Path $WorkRoot
$targetRoot = Join-Path $ProjectRoot '.codex\skills'
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$projectName = Split-Path -Leaf $ProjectRoot
$runRoot = Join-Path $WorkRoot "run-$projectName-$timestamp"
$stageRoot = Join-Path $runRoot 'stage'
$backupRoot = Join-Path $WorkRoot "backups\$projectName\$timestamp"
$reportPath = Join-Path $runRoot 'diff-report.txt'
$manifestPath = Join-Path $targetRoot '.codex-skill-sync.json'
$replacementLog = New-Object System.Collections.ArrayList

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Project root not found: $ProjectRoot"
}
if (-not (Test-Path -LiteralPath (Join-Path $script:SourceRoot '.git') -PathType Container)) {
    throw "This script must run from a Git clone: $script:SourceRoot"
}

New-Item -ItemType Directory -Path $WorkRoot -Force | Out-Null
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

try {
    $trackedChanges = @(Invoke-Git status --porcelain --untracked-files=no)
    if ($trackedChanges.Count -gt 0 -and ($trackedChanges -join '').Trim().Length -gt 0) {
        throw "The external version-controlled skill folder has modified tracked files. Commit or discard them before sync:`n$($trackedChanges -join [Environment]::NewLine)"
    }

    if ($SkipPull) {
        Write-Host "SkipPull is set. Using current local repository content: $script:SourceRoot"
    }
    else {
        Write-Host "Pulling latest skill repository content from origin/$Branch ..."
        Invoke-Git fetch origin $Branch | Out-Null
        Invoke-Git checkout $Branch | Out-Null
        Invoke-Git pull --ff-only origin $Branch | Out-Null
        Write-Host "Pull succeeded. Continuing sync."
    }

    $currentCommit = (Invoke-Git rev-parse HEAD | Select-Object -Last 1).Trim()

    foreach ($sourceSkill in $skillMap.Keys) {
        Copy-TrackedSkillToStage -SkillSourceName $sourceSkill -StageRoot $stageRoot
    }

    $allDiffLines = New-Object System.Collections.ArrayList
    $diffBySkill = [ordered]@{}
    foreach ($skillName in $skillMap.Keys) {
        $stagedSkill = Join-Path $stageRoot $skillMap[$skillName]
        $targetSkill = Join-Path $targetRoot $skillName
        $sourceMap = Get-TreeFileMap -Root $stagedSkill
        $targetExists = Test-Path -LiteralPath $targetSkill -PathType Container
        $targetMap = Get-TreeFileMap -Root $targetSkill
        $diff = Compare-TreeMaps -SourceMap $sourceMap -TargetMap $targetMap
        $diff | Add-Member -NotePropertyName TargetExists -NotePropertyValue $targetExists
        $diffBySkill[$skillName] = $diff
        if ($diff.HasDiff -and $targetExists) {
            foreach ($line in (Format-DiffList -SkillName $skillName -Diff $diff)) {
                [void]$allDiffLines.Add($line)
            }
            [void]$allDiffLines.Add('')
        }
        elseif ($targetExists) {
            [void]$allDiffLines.Add("Skill: $skillName - no diff")
        }
        else {
            [void]$allDiffLines.Add("Skill: $skillName - not installed; will install")
            $diff.HasDiff = $true
        }
    }

    Set-Content -LiteralPath $reportPath -Value @($allDiffLines) -Encoding UTF8
    Write-Host "Diff report: $reportPath"
    Write-Host ''
    $allDiffLines | ForEach-Object { Write-Host $_ }

    $hasAnyDiff = $false
    $hasExistingTargetDiff = $false
    foreach ($skillName in $diffBySkill.Keys) {
        if ($diffBySkill[$skillName].HasDiff) { $hasAnyDiff = $true }
        if ($diffBySkill[$skillName].HasDiff -and $diffBySkill[$skillName].TargetExists) { $hasExistingTargetDiff = $true }
    }

    if (-not $hasAnyDiff) {
        Write-Host "Project skills are already identical to external repository commit $currentCommit."
        exit 0
    }

    if ($CheckOnly) {
        Write-Host "CheckOnly is set. No files were changed."
        exit 0
    }

    $shouldSync = $Yes.IsPresent -or (-not $hasExistingTargetDiff)
    if (-not $shouldSync) {
        $answer = Read-Host "Use current external repository version to overwrite project installed skills? Type yes/no"
        $shouldSync = ($answer -eq 'yes')
    }

    if (-not $shouldSync) {
        Write-Host "Sync skipped by user. Project skills were not changed."
        exit 0
    }

    foreach ($skillName in $skillMap.Keys) {
        if (-not $diffBySkill[$skillName].HasDiff) {
            Write-Host "[$skillName] no diff; skipped."
            continue
        }

        $stagedSkill = Join-Path $stageRoot $skillMap[$skillName]
        $targetSkill = Join-Path $targetRoot $skillName
        $backupSkill = Join-Path $backupRoot $skillName

        Assert-ChildPath -Path $targetSkill -Parent $targetRoot
        if (Test-Path -LiteralPath $targetSkill -PathType Container) {
            Move-Item -LiteralPath $targetSkill -Destination $backupSkill
            [void]$replacementLog.Add([pscustomobject]@{
                Target = $targetSkill
                Backup = $backupSkill
                HadExisting = $true
            })
        }
        else {
            [void]$replacementLog.Add([pscustomobject]@{
                Target = $targetSkill
                Backup = $backupSkill
                HadExisting = $false
            })
        }

        Copy-Item -LiteralPath $stagedSkill -Destination $targetSkill -Recurse -Force
        Assert-SameTreeHash -Source $stagedSkill -Target $targetSkill
        Write-Host "[$skillName] synced to $targetSkill"
    }

    $manifest = [ordered]@{
        schema_version = 1
        source_root = $script:SourceRoot
        branch = $Branch
        commit = $currentCommit
        project_root = $ProjectRoot
        target_root = $targetRoot
        backup_root = $backupRoot
        diff_report = $reportPath
        synced_at_utc = [DateTime]::UtcNow.ToString('o')
        skills = @($skillMap.Keys)
    }
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

    Write-Host ''
    Write-Host "Project Codex skills synced successfully."
    Write-Host "Commit: $currentCommit"
    Write-Host "Target root: $targetRoot"
    Write-Host "Backup root: $backupRoot"
    Write-Host "Manifest: $manifestPath"
}
catch {
    for ($index = $replacementLog.Count - 1; $index -ge 0; $index--) {
        $item = $replacementLog[$index]
        if (Test-Path -LiteralPath $item.Target) {
            Remove-SafeTree -Path $item.Target -AllowedParent $targetRoot
        }
        if ($item.HadExisting -and (Test-Path -LiteralPath $item.Backup)) {
            Move-Item -LiteralPath $item.Backup -Destination $item.Target
        }
    }
    throw
}
finally {
    Remove-SafeTree -Path $stageRoot -AllowedParent $runRoot
}
