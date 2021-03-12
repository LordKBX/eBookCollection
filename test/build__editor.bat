@echo off
setlocal
cd /D %~dp0

pyinstaller --noconfirm --onedir --console --log-level INFO --version-file D:/CODES/Python/EbookCollection/test/BUILD_EDITOR.txt --icon D:/CODES/Python/EbookCollection/ressources/icons/app_icon.ico --hidden-import PyQt5.QtWebKit --hidden-import PyQt5.Qsci --hidden-import editing_pane --hidden-import common --hidden-import common.lang --paths D:/CODES/Python/EbookCollection --exclude-module PySide2                                                                                                                             --add-data D:/CODES/Python/EbookCollection/editor/checkpoint.ui;. --add-data D:/CODES/Python/EbookCollection/editor/content_table_editor.ui;. --add-data D:/CODES/Python/EbookCollection/editor/editor.ui;. --add-data D:/CODES/Python/EbookCollection/editor/files.ui;. --add-data D:/CODES/Python/EbookCollection/editor/files_name.ui;. --add-data D:/CODES/Python/EbookCollection/editor/img.ui;. --add-data D:/CODES/Python/EbookCollection/editor/link.ui;. --add-data D:/CODES/Python/EbookCollection/editor/text_edit.ui;. --add-data D:/CODES/Python/EbookCollection/editor/color_picker.ui;.                                                                                                                        --hidden-import win32gui --hidden-import win32con D:/CODES/Python/EbookCollection/editor/editor.py --distpath D:\CODES\Python\EbookCollection\test --workpath D:\CODES\Python\EbookCollection\test\tmp\build --specpath D:\CODES\Python\EbookCollection\test\tmp
rmdir /S /Q D:\CODES\Python\EbookCollection\test\tmp

cd .\editor
.\editor.exe debug
endlocal