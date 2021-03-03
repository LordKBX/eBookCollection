@echo off &setlocal
cd /d %~dp0
set /p date = < date /t

set "search={END_YEAR}"
set "replace=%date:~6,4%"
set "textfile=./LICENSE.tpl"
set "newfile=../LICENSE.txt"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"