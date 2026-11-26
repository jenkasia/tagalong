@echo off
rem Double-click to install Tagalong (keyboard + mouse switch) on this Windows PC. It asks for the channel.
rem   setup.bat -Uninstall   stops it and removes it from startup.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
pause
