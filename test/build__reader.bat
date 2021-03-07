@echo off
setlocal
cd /D %~dp0

pyinstaller --noconfirm --onedir --console --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_READER.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import PyQt5.QtWebKit --hidden-import PyQt5.Qsci --hidden-import CustomQWebView --hidden-import common --add-data D:/CODES/Python/EbookCollection/ressources;ressources/ --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2 --add-data D:/CODES/Python/EbookCollection/reader/reader.ui;. --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/reader/reader.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

cd .\reader
.\reader.exe debug
endlocal