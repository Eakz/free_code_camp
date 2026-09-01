@echo off
rem ---------------------------------------------------------------------------
rem  Installs wowfix so it can be run from any directory in cmd.
rem  Copies the script to %LOCALAPPDATA%\WowFix and drops a launcher into
rem  %LOCALAPPDATA%\Microsoft\WindowsApps, which is already on your PATH.
rem  No PATH editing, no admin rights, no registry changes.
rem ---------------------------------------------------------------------------
setlocal

set "DEST=%LOCALAPPDATA%\WowFix"
set "SHIM=%LOCALAPPDATA%\Microsoft\WindowsApps"

echo(
echo   Installing wowfix...
echo(

if not exist "%~dp0Restore-WowSettings.ps1" (
    echo   [ !! ] Restore-WowSettings.ps1 is not in this folder:
    echo          %~dp0
    echo          Keep both files together and run Install.cmd again.
    goto :end
)

if not exist "%SHIM%\" (
    echo   [warn] %SHIM%
    echo          does not exist, so the global launcher cannot be installed.
    echo          The script itself will still be copied - see the fallback
    echo          command printed at the end.
)

mkdir "%DEST%" 2>nul
copy /y "%~dp0Restore-WowSettings.ps1" "%DEST%\Restore-WowSettings.ps1" >nul
if errorlevel 1 (
    echo   [ !! ] Could not copy the script to %DEST%
    goto :end
)
echo   [ ok ] Script installed to %DEST%

rem Clear the mark-of-the-web so Windows does not block the downloaded file.
powershell -NoProfile -Command "Unblock-File -LiteralPath '%DEST%\Restore-WowSettings.ps1' -ErrorAction SilentlyContinue" 2>nul

if exist "%SHIM%\" (
    copy /y "%~dp0wowfix.cmd" "%SHIM%\wowfix.cmd" >nul
    if errorlevel 1 (
        echo   [warn] Could not install the launcher into %SHIM%
    ) else (
        echo   [ ok ] Launcher installed - 'wowfix' now works from any folder.
    )
)

echo(
echo   ------------------------------------------------------------------
echo   Open a NEW cmd window, then from ANY directory run:
echo(
echo       wowfix -ResetMinutesAgo 90
echo(
echo   That is report-only. It changes nothing and tells you what can
echo   actually be recovered.
echo(
echo   If 'wowfix' is not recognised, use this instead - it also works
echo   from any directory:
echo(
echo       powershell -NoProfile -ExecutionPolicy Bypass -File "%DEST%\Restore-WowSettings.ps1" -ResetMinutesAgo 90
echo   ------------------------------------------------------------------
echo(

:end
echo   Press any key to close.
pause >nul
