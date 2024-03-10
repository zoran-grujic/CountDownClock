@echo off

Rem call %windir%\System32\cmd.exe "/K" C:\Users\Zoran\anaconda3\Scripts\activate.bat C:\Users\Zoran\anaconda3
set root=C:\Users\Zoran\anaconda3
call %root%\Scripts\activate.bat %root%

Rem cd D:\Users\Zoran\Dropbox\Konferencije\PW2022\Bedz\Py
cd %~dp0

@echo on
python clock.py

pause
