[CmdletBinding()]
param([switch]$SkipPull)

$sourceRoot = $PSScriptRoot
$skillSourcesRoot = Split-Path -Parent $sourceRoot
$agentsRoot = Split-Path -Parent $skillSourcesRoot
$targetRoot = Join-Path $agentsRoot 'skills'
$manifestPath = Join-Path $sourceRoot '.codex-skill-tracking.project.json'
$updater = Join-Path $sourceRoot 'tracking\Update-CodexSkills.ps1'

& $updater -Scope project -SourceRoot $sourceRoot -TargetRoot $targetRoot -ManifestPath $manifestPath -SkipPull:$SkipPull
exit $LASTEXITCODE
