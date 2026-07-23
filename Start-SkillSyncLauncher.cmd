@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "LAUNCHER=%SCRIPT_DIR%SkillSyncLauncher.ps1"

if not exist "%LAUNCHER%" (
  echo Missing launcher: %LAUNCHER%
  pause
  exit /b 1
)

powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File "%LAUNCHER%"
exit /b %ERRORLEVEL%
