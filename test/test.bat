@echo off
setlocal
cd /d %~dp0
.\compil_reader.bat
cd .\reader
.\reader.exe "D:\Calibre_bookstore\Chugong, Jang Sung-Lak, cugong\I Alone Level-Up (501)\I Alone Level-Up - Chugong, Jang Sung-Lak, cugong.epub"
pause