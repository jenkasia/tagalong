@echo off
rem Double-click to install the keyboard + mouse switch on this Windows PC. It asks for the channel.
rem   setup_windows.bat -Uninstall   stops it and removes it from startup.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_windows.ps1" %*
pause
