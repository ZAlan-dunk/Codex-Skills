[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [string]$WorkRoot = 'F:\AAAASMWORK\AgentProject\SkillSync',

    [string]$Branch = 'main',

    [switch]$Yes,

    [switch]$CheckOnly,

    [switch]$SkipPull
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$innerScript = Join-Path $PSScriptRoot 'Sync-ProjectCodexSkills.ps1'
if (-not (Test-Path -LiteralPath $innerScript -PathType Leaf)) {
    throw "Missing base sync script: $innerScript"
}

& $innerScript `
    -ProjectRoot $ProjectRoot `
    -WorkRoot $WorkRoot `
    -Branch $Branch `
    -Yes:$Yes `
    -CheckOnly:$CheckOnly `
    -SkipPull:$SkipPull

exit $LASTEXITCODE
