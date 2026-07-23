Option Explicit
Dim shell, fso, env, scriptDir, launcher, logRoot, logFile, command, exitCode, text
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
Set env = shell.Environment("PROCESS")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
launcher = fso.BuildPath(scriptDir, "SkillSyncLauncher.ps1")

If Not fso.FileExists(launcher) Then
    MsgBox "Missing launcher: " & launcher, vbCritical, "Codex Skill Sync Launcher"
    WScript.Quit 1
End If

logRoot = env("DAWNSDEW_SKILL_SYNC_LOG_ROOT")
If Len(Trim(logRoot)) = 0 Then
    logRoot = fso.BuildPath(env("LOCALAPPDATA"), "DawnsdewMorningStar\SkillSyncLauncher\logs")
End If
If Not fso.FolderExists(logRoot) Then
    CreateFolders logRoot
End If
logFile = fso.BuildPath(logRoot, "launcher-last.log")

command = "cmd.exe /c powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File " & Chr(34) & launcher & Chr(34) & " > " & Chr(34) & logFile & Chr(34) & " 2>&1"
exitCode = shell.Run(command, 0, True)

If exitCode <> 0 Then
    text = ReadTextSafe(logFile)
    If Len(text) > 1800 Then
        text = Left(text, 1800) & vbCrLf & "..." & vbCrLf & "See full log: " & logFile
    End If
    MsgBox "Launcher failed. ExitCode: " & exitCode & vbCrLf & "Log: " & logFile & vbCrLf & vbCrLf & text, vbCritical, "Codex Skill Sync Launcher"
End If

WScript.Quit exitCode

Sub CreateFolders(ByVal path)
    Dim parent
    If Len(path) = 0 Or fso.FolderExists(path) Then Exit Sub
    parent = fso.GetParentFolderName(path)
    If Len(parent) > 0 And Not fso.FolderExists(parent) Then
        CreateFolders parent
    End If
    If Not fso.FolderExists(path) Then fso.CreateFolder path
End Sub

Function ReadTextSafe(ByVal path)
    On Error Resume Next
    Dim file
    If Not fso.FileExists(path) Then
        ReadTextSafe = ""
        Exit Function
    End If
    Set file = fso.OpenTextFile(path, 1, False)
    ReadTextSafe = file.ReadAll
    file.Close
    If Err.Number <> 0 Then
        ReadTextSafe = "Could not read log file."
        Err.Clear
    End If
    On Error GoTo 0
End Function
