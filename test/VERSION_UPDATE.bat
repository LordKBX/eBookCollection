@echo off
setlocal enabledelayedexpansion
cd /D %~dp0
set /p version=<.\VERSION.txt
set /p build=<.\VERSION_BUILD.txt
set /A step=1
set /A end=%build% + %step%
echo !end!>.\VERSION_BUILD.txt

set "search={BUILD}"
set "replace=%end%"
set "textfile=./BUILD_READER.yaml"
set "newfile=./BUILD_READER.yamlo"
copy /Y VERSION.tpl "%textfile%"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"

set "textfile=./BUILD_READER.yamlo"
set "newfile=./BUILD_READER.yaml"
set "search={VERSION}"
set "replace=%version%"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"

set "textfile=./BUILD_READER.yaml"
set "newfile=./BUILD_READER.yamlo"
set "search={NAME}"
set "replace=reader"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"

set "textfile=./BUILD_READER.yamlo"
set "newfile=./BUILD_EDITOR.yaml"
set "replace=editor"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"

set "newfile=./BUILD_LIBRARY.yaml"
set "replace=library"
(for /f "delims=" %%i in (%textfile%) do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    set "line=!line:%search%=%replace%!"
    echo(!line!
    endlocal
))>"%newfile%"

create-version-file .\BUILD_READER.yamlo --outfile .\BUILD_READER.txt
create-version-file .\BUILD_EDITOR.yaml --outfile .\BUILD_EDITOR.txt
create-version-file .\BUILD_LIBRARY.yaml --outfile .\BUILD_LIBRARY.txt

del *.yaml
del *.yamlo
endlocal