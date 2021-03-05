@echo off
setlocal
cd /d %~dp0
set input=%~1
start pythonw reader.py "%~1"
REM exit