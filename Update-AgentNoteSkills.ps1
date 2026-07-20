[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$SkipFetch,
    [switch]$InstallOnly,
    [string]$InstallRoot,
    [string]$UpstreamBranch = 'main',
    [string]$TrackingBranch = 'local/agentnote',
    [string]$PythonCommand = 'python',
    [string]$ValidatorPath = (Join-Path $env:USERPROFILE '.codex\skills\.system\skill-creator\scripts\quick_validate.py')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repository = 'https://github.com/ZAlan-dunk/Codex-Skills.git'
$SourceRoot = [System.IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\')
$TrackingRoot = Split-Path -Parent $SourceRoot
if ([string]::IsNullOrWhiteSpace($InstallRoot)) {
    $InstallRoot = Split-Path -Parent $TrackingRoot
}
$InstallRoot = [System.IO.Path]::GetFullPath($InstallRoot).TrimEnd('\')
$ManifestPath = Join-Path $InstallRoot '.codex-skill-tracking.agentnote.json'
$PyYamlLib = Join-Path $TrackingRoot 'dependencies\pyyaml\lib'

$SkillMap = [ordered]@{
    'acsdm-project-catalog' = 'ACSDM'
    'planning-to-requirements' = 'PCTR'
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

    $safeRoot = $SourceRoot.Replace('\', '/')
    $localExclude = (Join-Path $SourceRoot '.git\info\exclude').Replace('\', '/')
    $allArguments = @(
        '-c', "safe.directory=$safeRoot",
        '-c', "core.excludesFile=$localExclude",
        '-C', $SourceRoot
    ) + $Arguments

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

function Get-TreeHash {
    param([Parameter(Mandatory = $true)][string]$Root)

    $fullRoot = Get-FullPath -Path $Root
    $lines = Get-ChildItem -LiteralPath $fullRoot -Recurse -File |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($fullRoot.Length + 1).Replace('\', '/')
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            "$relative=$hash"
        }
    $text = $lines -join "`n"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Assert-SameTree {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target
    )

    $sourceHash = Get-TreeHash -Root $Source
    $targetHash = Get-TreeHash -Root $Target
    if ($sourceHash -ne $targetHash) {
        throw "Tree hash mismatch: '$Source' != '$Target'."
    }
}

function Invoke-SkillValidation {
    param([Parameter(Mandatory = $true)][string]$SkillPath)

    if (-not (Test-Path -LiteralPath $ValidatorPath -PathType Leaf)) {
        throw "Codex skill validator was not found: $ValidatorPath"
    }
    if (-not (Test-Path -LiteralPath (Join-Path $PyYamlLib 'yaml\__init__.py') -PathType Leaf)) {
        throw "Bundled PyYAML dependency was not found: $PyYamlLib"
    }

    $oldPythonPath = $env:PYTHONPATH
    $oldPythonUtf8 = $env:PYTHONUTF8
    try {
        if ([string]::IsNullOrWhiteSpace($oldPythonPath)) {
            $env:PYTHONPATH = $PyYamlLib
        }
        else {
            $env:PYTHONPATH = $PyYamlLib + [System.IO.Path]::PathSeparator + $oldPythonPath
        }
        $env:PYTHONUTF8 = '1'
        $output = & $PythonCommand $ValidatorPath $SkillPath 2>&1
        $exitCode = $LASTEXITCODE
        if ($exitCode -ne 0) {
            throw "Validation failed for '$SkillPath':`n$($output -join [Environment]::NewLine)"
        }
    }
    finally {
        $env:PYTHONPATH = $oldPythonPath
        $env:PYTHONUTF8 = $oldPythonUtf8
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $SourceRoot '.git'))) {
    throw "Tracking source is not a Git clone: $SourceRoot"
}

$workingChanges = @(Invoke-Git status --porcelain)
if ($workingChanges.Count -gt 0 -and ($workingChanges -join '').Trim().Length -gt 0) {
    throw "The tracking clone contains modified or untracked files. Commit, move, or discard them before updating:`n$($workingChanges -join [Environment]::NewLine)"
}

$currentBranch = (Invoke-Git rev-parse --abbrev-ref HEAD | Select-Object -Last 1).Trim()
if ($currentBranch -ne $TrackingBranch) {
    throw "Expected tracking branch '$TrackingBranch', found '$currentBranch'."
}

if (-not $SkipFetch -and -not $InstallOnly) {
    Invoke-Git fetch origin $UpstreamBranch | Out-Null
}

$upstreamRef = "origin/$UpstreamBranch"
$headBefore = (Invoke-Git rev-parse HEAD | Select-Object -Last 1).Trim()
$upstreamCommit = (Invoke-Git rev-parse $upstreamRef | Select-Object -Last 1).Trim()
$countText = (Invoke-Git rev-list --left-right --count "HEAD...$upstreamRef" | Select-Object -Last 1).Trim()
$counts = @($countText -split '\s+')
$ahead = [int]$counts[0]
$behind = [int]$counts[1]

$installedCommit = ''
$existingManifest = $null
if (Test-Path -LiteralPath $ManifestPath -PathType Leaf) {
    try {
        $existingManifest = Get-Content -Raw -Encoding UTF8 -LiteralPath $ManifestPath | ConvertFrom-Json
        $installedCommit = [string]$existingManifest.tracking_commit
    }
    catch {
        $installedCommit = ''
    }
}

if ($CheckOnly) {
    $installDrift = @()
    if ($null -ne $existingManifest) {
        foreach ($skill in @($existingManifest.skills)) {
            $targetPath = [string]$skill.target_path
            $recordedHash = [string]$skill.tree_sha256
            if (-not (Test-Path -LiteralPath $targetPath -PathType Container)) {
                $installDrift += "$($skill.name): target missing ($targetPath)"
                continue
            }
            $actualHash = Get-TreeHash -Root $targetPath
            if ($actualHash -ne $recordedHash) {
                $installDrift += "$($skill.name): tree hash differs"
            }
        }
    }

    Write-Host 'ACSDM/PCTR update status'
    Write-Host "Tracking branch: $currentBranch"
    Write-Host "Tracking commit: $headBefore"
    Write-Host "Upstream commit: $upstreamCommit"
    Write-Host "Ahead of upstream: $ahead"
    Write-Host "Behind upstream: $behind"
    Write-Host "Installed tracking commit: $installedCommit"
    if ($installDrift.Count -gt 0) {
        Write-Host 'Install state: installed skill files differ from the tracking manifest.'
        $installDrift | ForEach-Object { Write-Host "  $_" }
    }
    elseif ($installedCommit -ne $headBefore) {
        Write-Host 'Install state: tracking branch has changes not yet installed.'
    }
    elseif ($behind -gt 0) {
        Write-Host 'Install state: upstream updates are available.'
    }
    else {
        Write-Host 'Install state: up to date.'
    }
    if ($behind -gt 0) {
        Write-Host 'Upstream changed files:'
        Invoke-Git diff --name-status "HEAD..$upstreamRef" | ForEach-Object { Write-Host "  $_" }
    }
    exit 0
}

if (-not $InstallOnly -and $behind -gt 0) {
    try {
        Invoke-Git rebase $upstreamRef | Out-Null
    }
    catch {
        try {
            Invoke-Git rebase --abort | Out-Null
        }
        catch {
        }
        throw "Local tracking changes conflict with upstream. Rebase was aborted and installed skills were not changed.`n$($_.Exception.Message)"
    }
}

$trackingCommit = (Invoke-Git rev-parse HEAD | Select-Object -Last 1).Trim()
$upstreamCommit = (Invoke-Git rev-parse $upstreamRef | Select-Object -Last 1).Trim()
$stageRoot = Join-Path $InstallRoot ('.codex-skill-update-' + [Guid]::NewGuid().ToString('N'))
$backupRoot = Join-Path $InstallRoot ('.codex-skill-backup-' + [Guid]::NewGuid().ToString('N'))
$replacementLog = New-Object System.Collections.ArrayList

Assert-ChildPath -Path $stageRoot -Parent $InstallRoot
Assert-ChildPath -Path $backupRoot -Parent $InstallRoot

try {
    New-Item -ItemType Directory -Path $stageRoot,$backupRoot -Force | Out-Null

    foreach ($skillName in $SkillMap.Keys) {
        $wrapperName = $SkillMap[$skillName]
        $sourceSkill = Join-Path $SourceRoot $skillName
        $stagedWrapper = Join-Path $stageRoot $wrapperName
        $stagedSkill = Join-Path $stagedWrapper $skillName

        if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill 'SKILL.md') -PathType Leaf)) {
            throw "Tracking skill is missing SKILL.md: $sourceSkill"
        }

        New-Item -ItemType Directory -Path $stagedWrapper -Force | Out-Null
        Copy-Item -LiteralPath $sourceSkill -Destination $stagedWrapper -Recurse -Force

        Get-ChildItem -LiteralPath $stagedSkill -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq '__pycache__' } |
            Sort-Object FullName -Descending |
            ForEach-Object { Remove-SafeTree -Path $_.FullName -AllowedParent $stageRoot }

        Get-ChildItem -LiteralPath $stagedSkill -File -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -in @('.pyc', '.pyo', '.tmp') -or $_.Name -in @('.DS_Store', 'Thumbs.db') } |
            Remove-Item -Force

        Invoke-SkillValidation -SkillPath $stagedSkill
        Assert-SameTree -Source $sourceSkill -Target $stagedSkill
    }

    foreach ($skillName in $SkillMap.Keys) {
        $wrapperName = $SkillMap[$skillName]
        $targetWrapper = Join-Path $InstallRoot $wrapperName
        $stagedWrapper = Join-Path $stageRoot $wrapperName
        $backupWrapper = Join-Path $backupRoot $wrapperName
        $hadExisting = Test-Path -LiteralPath $targetWrapper

        Assert-ChildPath -Path $targetWrapper -Parent $InstallRoot
        if ($hadExisting) {
            Move-Item -LiteralPath $targetWrapper -Destination $backupWrapper
        }

        [void]$replacementLog.Add([pscustomobject]@{
            Target = $targetWrapper
            Backup = $backupWrapper
            HadExisting = $hadExisting
        })

        Move-Item -LiteralPath $stagedWrapper -Destination $targetWrapper
        Assert-SameTree -Source (Join-Path $SourceRoot $skillName) -Target (Join-Path $targetWrapper $skillName)
    }

    $installedSkills = @()
    foreach ($skillName in $SkillMap.Keys) {
        $wrapperName = $SkillMap[$skillName]
        $targetSkill = Join-Path (Join-Path $InstallRoot $wrapperName) $skillName
        $installedSkills += [ordered]@{
            name = $skillName
            repository_path = $skillName
            target_path = $targetSkill
            tree_sha256 = (Get-TreeHash -Root $targetSkill)
        }
    }

    $manifest = [ordered]@{
        schema_version = 1
        repository = $Repository
        upstream_branch = $UpstreamBranch
        tracking_branch = $TrackingBranch
        source_root = $SourceRoot
        install_root = $InstallRoot
        upstream_commit = $upstreamCommit
        tracking_commit = $trackingCommit
        previous_installed_commit = $installedCommit
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        update_script = (Join-Path $InstallRoot 'Update-ACSDM-PCTR.ps1')
        check_script = (Join-Path $InstallRoot 'Check-ACSDM-PCTR-Updates.ps1')
        skills = $installedSkills
    }
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
}
catch {
    for ($index = $replacementLog.Count - 1; $index -ge 0; $index--) {
        $item = $replacementLog[$index]
        if (Test-Path -LiteralPath $item.Target) {
            Remove-SafeTree -Path $item.Target -AllowedParent $InstallRoot
        }
        if ($item.HadExisting -and (Test-Path -LiteralPath $item.Backup)) {
            Move-Item -LiteralPath $item.Backup -Destination $item.Target
        }
    }
    throw
}
finally {
    Remove-SafeTree -Path $stageRoot -AllowedParent $InstallRoot
    Remove-SafeTree -Path $backupRoot -AllowedParent $InstallRoot
}

Write-Host 'ACSDM/PCTR skills updated successfully.'
Write-Host "Upstream commit: $upstreamCommit"
Write-Host "Tracking commit: $trackingCommit"
Write-Host "Install root: $InstallRoot"
Write-Host "Tracking manifest: $ManifestPath"
