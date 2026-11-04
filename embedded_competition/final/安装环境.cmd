@echo off

setlocal

cd /d "%~dp0"

py -3.13 -m venv .venv

if errorlevel 1 goto fail

".venv\Scripts\python.exe" -m pip install -r pc_app\requirements.txt

if errorlevel 1 goto fail

exit /b 0

:fail

pause

exit /b 1

