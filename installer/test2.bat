SETLOCAL ENABLEDELAYEDEXPANSION
python -V > ./fool.txt
set /p PythonVer= < ./fool.txt
del ./fool.txt
SET PythonVer=!PythonVer:Python=!
SET PythonVer=!PythonVer: =!
echo %PythonVer%
ENDLOCAL