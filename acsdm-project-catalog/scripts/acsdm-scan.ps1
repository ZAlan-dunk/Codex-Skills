param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [switch]$Json
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Project root not found: $ProjectRoot"
}

$CatalogRoot = Join-Path (Get-Item -LiteralPath $ProjectRoot).FullName '.ACSDM'
if (-not (Test-Path -LiteralPath $CatalogRoot -PathType Container)) {
    throw "ACSDM catalog root not found: $CatalogRoot"
}

$rootItem = Get-Item -LiteralPath $CatalogRoot
$modules = @()

foreach ($dir in Get-ChildItem -LiteralPath $CatalogRoot -Directory -Force | Sort-Object Name) {
    $mdFiles = @(Get-ChildItem -LiteralPath $dir.FullName -File -Filter '*.md' -Force | Sort-Object Name | ForEach-Object {
        [pscustomobject]@{
            name = $_.Name
            last_write_time = $_.LastWriteTime.ToString('s')
            length = $_.Length
        }
    })

    $modules += [pscustomobject]@{
        name = $dir.Name
        full_name = $dir.FullName
        last_write_time = $dir.LastWriteTime.ToString('s')
        markdown_count = $mdFiles.Count
        markdown_files = $mdFiles
    }
}

$result = [pscustomobject]@{
    project_root = (Get-Item -LiteralPath $ProjectRoot).FullName
    catalog_root = $rootItem.FullName
    scanned_at = (Get-Date).ToString('s')
    module_count = $modules.Count
    modules = $modules
}

if ($Json) {
    $result | ConvertTo-Json -Depth 6
} else {
    Write-Output "ProjectRoot: $($result.project_root)"
    Write-Output "CatalogRoot: $($result.catalog_root)"
    Write-Output "ScannedAt: $($result.scanned_at)"
    foreach ($module in $modules) {
        Write-Output "[DIR] $($module.name)"
        foreach ($file in $module.markdown_files) {
            Write-Output "  $($file.name)"
        }
    }
}