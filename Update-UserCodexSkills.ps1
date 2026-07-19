[CmdletBinding()]
param([switch]$SkipPull)

$sourceRoot = $PSScriptRoot
$targetRoot = Join-Path $env:USERPROFILE '.codex\skills'
$manifestPath = Join-Path $sourceRoot '.codex-skill-tracking.user.json'
$updater = Join-Path $sourceRoot 'tracking\Update-CodexSkills.ps1'

& $updater -Scope user -SourceRoot $sourceRoot -TargetRoot $targetRoot -ManifestPath $manifestPath -SkipPull:$SkipPull
exit $LASTEXITCODE
