@echo off
setlocal
cd /D %~dp0

pyinstaller --noconfirm --onedir --console --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_LIBRARY.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import common --add-data D:/CODES/Python/EbookCollection/ressources;ressources/ --add-data D:/CODES/Python/EbookCollection/tools;tools/ --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2 --add-data D:/CODES/Python/EbookCollection/empty_book.ui;. --add-data D:/CODES/Python/EbookCollection/home.ui;. --add-data D:/CODES/Python/EbookCollection/settings.ui;. --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/library.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

cd .\library
.\library.exe debug
endlocal