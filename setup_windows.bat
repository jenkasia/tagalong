@echo off
rem Double-click to set up the keyboard + mouse switch on this Windows PC (channel 2).
rem   setup_windows.bat -Uninstall   stops it and removes it from startup.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_windows.ps1" %*
pause
