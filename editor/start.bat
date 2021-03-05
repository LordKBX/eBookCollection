@echo off
setlocal
cd /d %~dp0
set input=%~1
start pythonw editor.py "%~1"
REM exit