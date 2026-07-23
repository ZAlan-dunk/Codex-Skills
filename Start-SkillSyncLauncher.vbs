Option Explicit
Dim shell, fso, scriptDir, launcher, command
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
launcher = fso.BuildPath(scriptDir, "SkillSyncLauncher.ps1")
If Not fso.FileExists(launcher) Then
    MsgBox "Missing launcher: " & launcher, vbCritical, "Codex Skill Sync Launcher"
    WScript.Quit 1
End If
command = "powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File " & Chr(34) & launcher & Chr(34)
shell.Run command, 0, False
