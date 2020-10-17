SETLOCAL ENABLEDELAYEDEXPANSION
SET size=0
SET size2=0
SET String=%PATH%
SET String=!String:A=a!
SET String=!String:B=b!
SET String=!String:C=c!
SET String=!String:D=d!
SET String=!String:E=e!
SET String=!String:F=f!
SET String=!String:G=g!
SET String=!String:H=h!
SET String=!String:I=i!
SET String=!String:J=j!
SET String=!String:K=k!
SET String=!String:L=l!
SET String=!String:M=m!
SET String=!String:N=n!
SET String=!String:O=o!
SET String=!String:P=p!
SET String=!String:Q=q!
SET String=!String:R=r!
SET String=!String:S=s!
SET String=!String:T=t!
SET String=!String:U=u!
SET String=!String:V=v!
SET String=!String:W=w!
SET String=!String:X=x!
SET String=!String:Y=y!
SET String=!String:Z=z!
REM echo "%String%"
echo "%String%" | findstr "python" > tmppath.txt
call :filesize tmppath.txt
echo "file size is %size%"
IF %size% == 0 (
python\python-3.8.5-amd64.exe /quiet
cmd /K test.bat
exit
)
del python\python-3.8.5-amd64.exe
python -V > fool.txt
python -c "import sys; print(sys.version)" > fool2.txt
SET /p PythonVer= < fool.txt
del fool.txt
SET PythonVer=!PythonVer:Python=!
SET PythonVer=!PythonVer: =!
SET PythonVer=!PythonVer:.=!
SET PythonVer=%PythonVer:~0,2%

pip install python/pywin32-228-cp38-cp38-win_amd64.whl
pip install python/six-1.15.0-py2.py3-none-any.whl
pip install python/beautifulsoup4-4.9.2-py3-none-any.whl
pip install python/lxml-4.5.2-cp38-cp38-win_amd64.whl
pip install python/Pillow-7.2.0-cp38-cp38-win_amd64.whl
pip install python/PyQt5-5.15.1-5.15.1-cp35.cp36.cp37.cp38.cp39-none-win_amd64.whl
pip install python/PyQtWebKit-5.13.1-cp38-none-win_amd64.whl
pip install python/pysqlite3-0.4.3.tar.gz
pip install python/pyperclip-1.8.1.tar.gz

rmdir "python" /Q

del tmppath.txt
del tmppath2.txt
del fool2.txt
REM pause
REM exit

:: set filesize of 1st argument in %size% variable, and return
:filesize
  SET size=%~z1
  GOTO:EOF
  
:filesize2
  SET size2=%~z1
  GOTO:EOF

ENDLOCAL