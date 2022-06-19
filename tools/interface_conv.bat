@echo off &setlocal
cd /d %~dp0

for /f "tokens=1*delims=." %%a in ('dir /o-n/b/s "..\\*.ui"') do (
	echo ">>> %%a.%%b"
	python -m PyQt5.uic.pyuic -x %%a.ui -o %%a_ui.py
    fart.exe %%a_ui.py "Ui_Dialog(object)" "Ui_Dialog(QtWidgets.QDialog)"
    fart.exe %%a_ui.py "Ui_MainWindow(object)" "Ui_MainWindow(QtWidgets.QMainWindow)"
    fart.exe %%a_ui.py "Ui_Form(object)" "Ui_Form(QtWidgets.QWidget)"

    fart.exe %%a_ui.py "(self, Dialog)" "(self, Dialog: QtWidgets.QDialog)"
    fart.exe %%a_ui.py "(self, dialog)" "(self, dialog: QtWidgets.QDialog)"
    fart.exe %%a_ui.py "(self, MainWindow)" "(self, MainWindow: QtWidgets.QMainWindow)"
    fart.exe %%a_ui.py "(self, Form)" "(self, Form: QtWidgets.QWidget)"
)
REM python "%location%\Lib\site-packages\PyQt5\pyrcc_main.py" ../ressources/r.qrc -o r_rc.py
REM pause