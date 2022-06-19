REM @echo off
setlocal
cd /d %~dp0
.\7zip\7z.exe a ..\packages\style\Light.ebcstyle ..\ressources\styles\Light.json
.\7zip\7z.exe a ..\packages\lang\fr_FR.ebclang ..\ressources\langs\fr_FR.json

cd "C:\Program Files\PuTTY"
psftp -b "D:\CODES\Python\EbookCollection\tools\UpdatePackages-putty.txt" tiranusho@sd-36502.dedibox.fr -pw 2Fullmetal
pause