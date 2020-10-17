@echo off
setlocal
cd /d %~dp0
set input=%~1
start pythonw main.py "%~1"
REM exit