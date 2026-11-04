@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo 请先运行安装环境.cmd
 pause
 exit /b 1
)
".venv\Scripts\python.exe" "pc_app\main.py"
if errorlevel 1 pause
