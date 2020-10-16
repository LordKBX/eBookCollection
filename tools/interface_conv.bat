@echo off
python ./_getpython.py > ./fool.txt
set /p location= < ./fool.txt
del ./fool.txt

for /f "tokens=1*delims=." %%a in ('dir /o-n/b/s "..\\*.ui"') do (
	echo ">>> %%a.%%b"
	python -m PyQt5.uic.pyuic -x %%a.ui -o %%a_ui.py
)
REM python "%location%\Lib\site-packages\PyQt5\pyrcc_main.py" ../ressources/r.qrc -o r_rc.py
REM pause