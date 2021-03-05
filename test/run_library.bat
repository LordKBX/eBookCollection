@echo off
setlocal
cd /d %~dp0
cd .\library
.\library.exe debug
pause