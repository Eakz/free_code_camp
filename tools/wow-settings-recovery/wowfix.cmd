@echo off
rem ---------------------------------------------------------------------------
rem  wowfix - launcher for Restore-WowSettings.ps1
rem  Callable from any directory once Install.cmd has been run.
rem  All arguments are passed straight through to the script.
rem ---------------------------------------------------------------------------
setlocal

rem Prefer a copy sitting next to this launcher, then the installed location.
set "PS1=%~dp0Restore-WowSettings.ps1"
if not exist "%PS1%" set "PS1=%LOCALAPPDATA%\WowFix\Restore-WowSettings.ps1"

if not exist "%PS1%" (
    echo(
    echo   Cannot find Restore-WowSettings.ps1
    echo(
    echo   Looked in: %~dp0
    echo          and: %LOCALAPPDATA%\WowFix\
    echo(
    echo   Run Install.cmd from the folder you unzipped, or pass the script
    echo   path directly with:
    echo       powershell -NoProfile -ExecutionPolicy Bypass -File "C:\path\to\Restore-WowSettings.ps1"
    echo(
    exit /b 1
)

rem No arguments at all -> the safe report-only default.
if "%~1"=="" (
    echo(
    echo   No options given - running a REPORT ONLY scan for a reset in the
    echo   last 60 minutes. Nothing will be changed.
    echo   Use -ResetMinutesAgo N if that is wrong.
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
    exit /b %ERRORLEVEL%
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
exit /b %ERRORLEVEL%
