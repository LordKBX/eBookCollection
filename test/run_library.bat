@echo off
setlocal
cd /d %~dp0
cd .\build
.\library.exe debug
exit