@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "LAUNCHER=%SCRIPT_DIR%SkillSyncLauncher.ps1"

if not exist "%LAUNCHER%" (
  echo Missing launcher: %LAUNCHER%
  pause
  exit /b 1
)

if "%DAWNSDEW_SKILL_SYNC_LOG_ROOT%"=="" (
  set "LOG_ROOT=%LOCALAPPDATA%\DawnsdewMorningStar\SkillSyncLauncher\logs"
) else (
  set "LOG_ROOT=%DAWNSDEW_SKILL_SYNC_LOG_ROOT%"
)

if not exist "%LOG_ROOT%" mkdir "%LOG_ROOT%" >nul 2>nul
set "LOG_FILE=%LOG_ROOT%\launcher-last.log"

echo Starting Codex Skill Sync Launcher...
echo Log: %LOG_FILE%

powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File "%LAUNCHER%" > "%LOG_FILE%" 2>&1
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo Launcher failed. ExitCode: %EXIT_CODE%
  echo Log file: %LOG_FILE%
  echo --------------------
  type "%LOG_FILE%"
  echo --------------------
  pause
  exit /b %EXIT_CODE%
)

exit /b 0
