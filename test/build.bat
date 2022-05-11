@echo off
setlocal
cd /D %~dp0
C:\Windows\System32\cmd.exe /C .\VERSION_UPDATE.bat
rmdir /S /Q D:\CODES\Python\EbookCollection\test\build
rmdir /S /Q D:\CODES\Python\EbookCollection\test\reader
rmdir /S /Q D:\CODES\Python\EbookCollection\test\editor
rmdir /S /Q D:\CODES\Python\EbookCollection\test\library
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

mkdir D:\CODES\Python\EbookCollection\test\build

pyinstaller --noconfirm --onedir --windowed --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_LIBRARY.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import common --add-data D:/CODES/Python/EbookCollection/ressources;ressources/ --add-data D:/CODES/Python/EbookCollection/tools;tools/ --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2 --add-data D:/CODES/Python/EbookCollection/empty_book.ui;. --add-data D:/CODES/Python/EbookCollection/home.ui;. --add-data D:/CODES/Python/EbookCollection/settings.ui;. --add-data D:/CODES/Python/EbookCollection/settings_plugin_params.ui;. --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/library.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

pyinstaller --noconfirm --onedir --windowed --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_READER.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import PyQt5.QtWebKit --hidden-import PyQt5.Qsci --hidden-import CustomQWebView --hidden-import common --add-data D:/CODES/Python/EbookCollection/ressources;ressources/ --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2 --add-data D:/CODES/Python/EbookCollection/reader/reader.ui;. --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/reader/reader.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

pyinstaller --noconfirm --onedir --windowed --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_EDITOR.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import PyQt5.QtWebKit --hidden-import PyQt5.Qsci --hidden-import editing_pane --hidden-import common --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2 --add-data D:/CODES/Python/EbookCollection/editor/checkpoint.ui;. --add-data D:/CODES/Python/EbookCollection/editor/content_table_editor.ui;. --add-data D:/CODES/Python/EbookCollection/editor/editor.ui;. --add-data D:/CODES/Python/EbookCollection/editor/files.ui;. --add-data D:/CODES/Python/EbookCollection/editor/files_name.ui;. --add-data D:/CODES/Python/EbookCollection/editor/img.ui;. --add-data D:/CODES/Python/EbookCollection/editor/link.ui;. --add-data D:/CODES/Python/EbookCollection/editor/text_edit.ui;.  --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/editor/editor.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

C:\Windows\System32\xcopy.exe D:\CODES\Python\EbookCollection\test\reader\ D:\CODES\Python\EbookCollection\test\build\ /E /H /C /I /Q /Y

copy D:\CODES\Python\EbookCollection\test\editor\editor.exe D:\CODES\Python\EbookCollection\test\build\
copy D:\CODES\Python\EbookCollection\test\editor\*.ui D:\CODES\Python\EbookCollection\test\build\

copy D:\CODES\Python\EbookCollection\test\library\library.exe D:\CODES\Python\EbookCollection\test\build\
copy D:\CODES\Python\EbookCollection\test\library\*.ui D:\CODES\Python\EbookCollection\test\build\

rmdir /S /Q D:\CODES\Python\EbookCollection\test\editor
rmdir /S /Q D:\CODES\Python\EbookCollection\test\library
rmdir /S /Q D:\CODES\Python\EbookCollection\test\reader
pause
exit