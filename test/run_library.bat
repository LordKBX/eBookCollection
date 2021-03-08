@echo off
setlocal
set aa=%~dp0%build
echo %aa%
cd /D %aa%
%aa%\library.exe debug