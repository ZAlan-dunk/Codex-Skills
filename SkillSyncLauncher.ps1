param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

if ([System.Threading.Thread]::CurrentThread.ApartmentState -ne [System.Threading.ApartmentState]::STA) {
    $self = $PSCommandPath
    Start-Process powershell.exe -ArgumentList @('-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',$self) -WindowStyle Normal
    exit
}

$scriptRoot = $PSScriptRoot
$script:LastRunOutput = ''
$defaultWorkRoot = 'F:\AAAASMWORK\AgentProject\SkillSync'
$defaultProjectRoot = 'E:\UnityProject\PJ032'

function Quote-Arg {
    param([Parameter(Mandatory = $true)][string]$Value)
    if ($Value -match '[\s"`$]') {
        return '"' + ($Value -replace '"', '`"') + '"'
    }
    return $Value
}

function Append-Log {
    param(
        [Parameter(Mandatory = $true)][System.Windows.Forms.RichTextBox]$Box,
        [Parameter(Mandatory = $true)][string]$Text,
        [System.Drawing.Color]$Color = ([System.Drawing.Color]::Gainsboro)
    )
    if ([string]::IsNullOrWhiteSpace($Text)) { return }
    $Box.SelectionStart = $Box.TextLength
    $Box.SelectionLength = 0
    $Box.SelectionColor = $Color
    $Box.AppendText($Text.TrimEnd() + [Environment]::NewLine)
    $Box.SelectionColor = $Box.ForeColor
    $Box.ScrollToCaret()
}

function Invoke-ScriptCapture {
    param(
        [Parameter(Mandatory = $true)][string]$ScriptPath,
        [string[]]$Arguments = @(),
        [string]$WorkingDirectory = $scriptRoot
    )

    $cmd = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ScriptPath) + $Arguments
    $output = & powershell.exe @cmd 2>&1
    $exitCode = $LASTEXITCODE
    [pscustomobject]@{
        ExitCode = $exitCode
        Output = (@($output | ForEach-Object { "$_" }) -join [Environment]::NewLine)
    }
}

function Set-Busy {
    param([bool]$Busy)
    $buttons = @($btnUpdateUser, $btnUpdateProject, $btnUpdateAgent, $btnSyncProject, $btnSyncPJ032, $btnCheckOnly, $btnOpenProject, $btnOpenWork)
    foreach ($b in $buttons) { $b.Enabled = -not $Busy }
    $form.UseWaitCursor = $Busy
    [System.Windows.Forms.Application]::DoEvents()
}

function Run-And-Log {
    param(
        [Parameter(Mandatory = $true)][string]$Title,
        [Parameter(Mandatory = $true)][string]$ScriptPath,
        [string[]]$Arguments = @(),
        [string]$WorkingDirectory = $scriptRoot
    )

    Append-Log $logBox "=== $Title ===" ([System.Drawing.Color]::DodgerBlue)
    Append-Log $logBox "脚本：$ScriptPath" ([System.Drawing.Color]::Gray)
    if ($Arguments.Count -gt 0) {
        Append-Log $logBox ('参数：' + ($Arguments -join ' ')) ([System.Drawing.Color]::Gray)
    }
    Set-Busy $true
    try {
        $result = Invoke-ScriptCapture -ScriptPath $ScriptPath -Arguments $Arguments -WorkingDirectory $WorkingDirectory
        $script:LastRunOutput = $result.Output
        if (-not [string]::IsNullOrWhiteSpace($result.Output)) {
            Append-Log $logBox $result.Output
        }
        if ($result.ExitCode -ne 0) {
            Append-Log $logBox "退出码：$($result.ExitCode)" ([System.Drawing.Color]::Red)
            [System.Windows.Forms.MessageBox]::Show($form, "$Title 执行失败，请查看日志。", '错误', 'OK', 'Error') | Out-Null
            return $false
        }
        Append-Log $logBox "完成" ([System.Drawing.Color]::LimeGreen)
        return $true
    }
    finally {
        Set-Busy $false
    }
}

function Sync-ProjectLike {
    param([string]$Mode)

    $projectRoot = $txtProjectRoot.Text.Trim()
    $workRoot = $txtWorkRoot.Text.Trim()
    $branch = $txtBranch.Text.Trim()
    if ([string]::IsNullOrWhiteSpace($projectRoot)) {
        [System.Windows.Forms.MessageBox]::Show($form, '请先输入项目根目录。', '缺少输入', 'OK', 'Warning') | Out-Null
        return
    }
    if ([string]::IsNullOrWhiteSpace($workRoot)) {
        [System.Windows.Forms.MessageBox]::Show($form, '请先输入工作产物目录。', '缺少输入', 'OK', 'Warning') | Out-Null
        return
    }

    $baseArgs = @('-ProjectRoot', $projectRoot, '-WorkRoot', $workRoot)
    if (-not [string]::IsNullOrWhiteSpace($branch)) { $baseArgs += @('-Branch', $branch) }
    if ($chkSkipPull.Checked) { $baseArgs += '-SkipPull' }

    $scriptPath = Join-Path $scriptRoot 'Sync-ProjectCodexSkills.ps1'
    $preflight = Run-And-Log -Title "$Mode / 只检查差异" -ScriptPath $scriptPath -Arguments ($baseArgs + '-CheckOnly')
    if (-not $preflight) { return }

    $combinedOutput = $script:LastRunOutput
    if ($combinedOutput -match 'no diff|already identical') {
        [System.Windows.Forms.MessageBox]::Show($form, '未发现差异，无需同步。', '提示', 'OK', 'Information') | Out-Null
        return
    }

    $shouldOverwrite = $chkAutoYes.Checked
    if (-not $shouldOverwrite) {
        $dialog = [System.Windows.Forms.MessageBox]::Show($form, "发现差异。是否使用当前外部仓库版本覆盖项目内已安装的技能？", '确认覆盖', 'YesNo', 'Question')
        $shouldOverwrite = ($dialog -eq [System.Windows.Forms.DialogResult]::Yes)
    }

    if (-not $shouldOverwrite) {
        Append-Log $logBox '用户选择否，已跳过同步。' ([System.Drawing.Color]::Orange)
        return
    }

    $syncArgs = @('-ProjectRoot', $projectRoot, '-WorkRoot', $workRoot, '-Yes')
    if (-not [string]::IsNullOrWhiteSpace($branch)) { $syncArgs += @('-Branch', $branch) }
    if ($chkSkipPull.Checked) { $syncArgs += '-SkipPull' }
    Run-And-Log -Title "$Mode / 执行同步" -ScriptPath $scriptPath -Arguments $syncArgs | Out-Null
}

function Open-Path {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    if (-not (Test-Path -LiteralPath $Path)) {
        [System.Windows.Forms.MessageBox]::Show($form, "路径不存在：$Path", '路径不存在', 'OK', 'Warning') | Out-Null
        return
    }
    Start-Process explorer.exe -ArgumentList @($Path)
}

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Codex 技能同步工具'
$form.Size = New-Object System.Drawing.Size(1120, 760)
$form.StartPosition = 'CenterScreen'
$form.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 9)
$form.TopMost = $false

$lblProject = New-Object System.Windows.Forms.Label
$lblProject.Text = '项目根目录'
$lblProject.Location = New-Object System.Drawing.Point(16, 18)
$lblProject.AutoSize = $true
$form.Controls.Add($lblProject)

$txtProjectRoot = New-Object System.Windows.Forms.TextBox
$txtProjectRoot.Location = New-Object System.Drawing.Point(110, 14)
$txtProjectRoot.Size = New-Object System.Drawing.Size(780, 26)
$txtProjectRoot.Text = $defaultProjectRoot
$form.Controls.Add($txtProjectRoot)

$btnProjectBrowse = New-Object System.Windows.Forms.Button
$btnProjectBrowse.Text = '浏览'
$btnProjectBrowse.Location = New-Object System.Drawing.Point(905, 12)
$btnProjectBrowse.Size = New-Object System.Drawing.Size(80, 28)
$form.Controls.Add($btnProjectBrowse)

$btnOpenProject = New-Object System.Windows.Forms.Button
$btnOpenProject.Text = '打开'
$btnOpenProject.Location = New-Object System.Drawing.Point(990, 12)
$btnOpenProject.Size = New-Object System.Drawing.Size(80, 28)
$form.Controls.Add($btnOpenProject)

$lblWork = New-Object System.Windows.Forms.Label
$lblWork.Text = '工作产物目录'
$lblWork.Location = New-Object System.Drawing.Point(16, 52)
$lblWork.AutoSize = $true
$form.Controls.Add($lblWork)

$txtWorkRoot = New-Object System.Windows.Forms.TextBox
$txtWorkRoot.Location = New-Object System.Drawing.Point(110, 48)
$txtWorkRoot.Size = New-Object System.Drawing.Size(780, 26)
$txtWorkRoot.Text = $defaultWorkRoot
$form.Controls.Add($txtWorkRoot)

$btnWorkBrowse = New-Object System.Windows.Forms.Button
$btnWorkBrowse.Text = '浏览'
$btnWorkBrowse.Location = New-Object System.Drawing.Point(905, 46)
$btnWorkBrowse.Size = New-Object System.Drawing.Size(80, 28)
$form.Controls.Add($btnWorkBrowse)

$btnOpenWork = New-Object System.Windows.Forms.Button
$btnOpenWork.Text = '打开'
$btnOpenWork.Location = New-Object System.Drawing.Point(990, 46)
$btnOpenWork.Size = New-Object System.Drawing.Size(80, 28)
$form.Controls.Add($btnOpenWork)

$lblBranch = New-Object System.Windows.Forms.Label
$lblBranch.Text = '仓库分支'
$lblBranch.Location = New-Object System.Drawing.Point(16, 86)
$lblBranch.AutoSize = $true
$form.Controls.Add($lblBranch)

$txtBranch = New-Object System.Windows.Forms.TextBox
$txtBranch.Location = New-Object System.Drawing.Point(110, 82)
$txtBranch.Size = New-Object System.Drawing.Size(180, 26)
$txtBranch.Text = 'main'
$form.Controls.Add($txtBranch)

$chkSkipPull = New-Object System.Windows.Forms.CheckBox
$chkSkipPull.Text = '跳过拉取（离线）'
$chkSkipPull.Location = New-Object System.Drawing.Point(310, 82)
$chkSkipPull.AutoSize = $true
$form.Controls.Add($chkSkipPull)

$chkAutoYes = New-Object System.Windows.Forms.CheckBox
$chkAutoYes.Text = '发现差异时自动覆盖'
$chkAutoYes.Location = New-Object System.Drawing.Point(480, 82)
$chkAutoYes.AutoSize = $true
$form.Controls.Add($chkAutoYes)

$lblSource = New-Object System.Windows.Forms.Label
$lblSource.Text = "外部技能仓库：$scriptRoot"
$lblSource.Location = New-Object System.Drawing.Point(16, 116)
$lblSource.AutoSize = $true
$lblSource.ForeColor = [System.Drawing.Color]::DimGray
$form.Controls.Add($lblSource)

$btnUpdateUser = New-Object System.Windows.Forms.Button
$btnUpdateUser.Text = '更新用户级技能'
$btnUpdateUser.Location = New-Object System.Drawing.Point(16, 148)
$btnUpdateUser.Size = New-Object System.Drawing.Size(150, 32)
$form.Controls.Add($btnUpdateUser)

$btnUpdateProject = New-Object System.Windows.Forms.Button
$btnUpdateProject.Text = '更新项目级技能'
$btnUpdateProject.Location = New-Object System.Drawing.Point(176, 148)
$btnUpdateProject.Size = New-Object System.Drawing.Size(160, 32)
$form.Controls.Add($btnUpdateProject)

$btnUpdateAgent = New-Object System.Windows.Forms.Button
$btnUpdateAgent.Text = '更新 AgentNote 技能'
$btnUpdateAgent.Location = New-Object System.Drawing.Point(346, 148)
$btnUpdateAgent.Size = New-Object System.Drawing.Size(180, 32)
$form.Controls.Add($btnUpdateAgent)

$btnSyncProject = New-Object System.Windows.Forms.Button
$btnSyncProject.Text = '同步项目技能'
$btnSyncProject.Location = New-Object System.Drawing.Point(536, 148)
$btnSyncProject.Size = New-Object System.Drawing.Size(150, 32)
$form.Controls.Add($btnSyncProject)

$btnSyncPJ032 = New-Object System.Windows.Forms.Button
$btnSyncPJ032.Text = '同步 PJ032 技能'
$btnSyncPJ032.Location = New-Object System.Drawing.Point(696, 148)
$btnSyncPJ032.Size = New-Object System.Drawing.Size(150, 32)
$form.Controls.Add($btnSyncPJ032)

$btnCheckOnly = New-Object System.Windows.Forms.Button
$btnCheckOnly.Text = '只检查差异'
$btnCheckOnly.Location = New-Object System.Drawing.Point(856, 148)
$btnCheckOnly.Size = New-Object System.Drawing.Size(110, 32)
$form.Controls.Add($btnCheckOnly)

$btnClear = New-Object System.Windows.Forms.Button
$btnClear.Text = '清空日志'
$btnClear.Location = New-Object System.Drawing.Point(976, 148)
$btnClear.Size = New-Object System.Drawing.Size(94, 32)
$form.Controls.Add($btnClear)

$logBox = New-Object System.Windows.Forms.RichTextBox
$logBox.Location = New-Object System.Drawing.Point(16, 194)
$logBox.Size = New-Object System.Drawing.Size(1054, 500)
$logBox.ReadOnly = $true
$logBox.Font = New-Object System.Drawing.Font('Consolas', 9)
$logBox.BackColor = ([System.Drawing.Color]::Black)
$logBox.ForeColor = ([System.Drawing.Color]::Gainsboro)
$form.Controls.Add($logBox)

$btnProjectBrowse.Add_Click({
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description = '选择项目根目录'
    $dlg.SelectedPath = $txtProjectRoot.Text
    if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $txtProjectRoot.Text = $dlg.SelectedPath
    }
})
$btnWorkBrowse.Add_Click({
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description = '选择工作产物目录'
    $dlg.SelectedPath = $txtWorkRoot.Text
    if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $txtWorkRoot.Text = $dlg.SelectedPath
    }
})
$btnOpenProject.Add_Click({ Open-Path -Path $txtProjectRoot.Text.Trim() })
$btnOpenWork.Add_Click({ Open-Path -Path $txtWorkRoot.Text.Trim() })
$btnClear.Add_Click({ $logBox.Clear() })

$btnUpdateUser.Add_Click({
    $scriptPath = Join-Path $scriptRoot 'Update-UserCodexSkills.ps1'
    Run-And-Log -Title '更新用户级技能' -ScriptPath $scriptPath -Arguments @() | Out-Null
})
$btnUpdateProject.Add_Click({
    $scriptPath = Join-Path $scriptRoot 'Update-ProjectCodexSkills.ps1'
    Run-And-Log -Title '更新项目级技能' -ScriptPath $scriptPath -Arguments @() | Out-Null
})
$btnUpdateAgent.Add_Click({
    $scriptPath = Join-Path $scriptRoot 'Update-AgentNoteSkills.ps1'
    $args = @()
    if ($chkSkipPull.Checked) { $args += '-SkipFetch' }
    Run-And-Log -Title '更新 AgentNote 技能' -ScriptPath $scriptPath -Arguments $args | Out-Null
})
$btnSyncProject.Add_Click({ Sync-ProjectLike -Mode '同步项目技能' })
$btnSyncPJ032.Add_Click({
    if ([string]::IsNullOrWhiteSpace($txtProjectRoot.Text.Trim())) {
        $txtProjectRoot.Text = $defaultProjectRoot
    }
    Sync-ProjectLike -Mode '同步 PJ032 技能'
})
$btnCheckOnly.Add_Click({
    $txt = $txtProjectRoot.Text.Trim()
    if ([string]::IsNullOrWhiteSpace($txt)) {
        [System.Windows.Forms.MessageBox]::Show($form, '请先输入项目根目录。', '缺少输入', 'OK', 'Warning') | Out-Null
        return
    }
    $scriptPath = Join-Path $scriptRoot 'Sync-ProjectCodexSkills.ps1'
    $args = @('-ProjectRoot', $txt, '-WorkRoot', $txtWorkRoot.Text.Trim(), '-CheckOnly')
    if (-not [string]::IsNullOrWhiteSpace($txtBranch.Text.Trim())) { $args += @('-Branch', $txtBranch.Text.Trim()) }
    if ($chkSkipPull.Checked) { $args += '-SkipPull' }
    Run-And-Log -Title '只检查差异' -ScriptPath $scriptPath -Arguments $args | Out-Null
})

Append-Log $logBox '准备就绪。请填写项目根目录 / 工作产物目录，然后点击按钮执行。' ([System.Drawing.Color]::LimeGreen)
[void]$form.ShowDialog()
