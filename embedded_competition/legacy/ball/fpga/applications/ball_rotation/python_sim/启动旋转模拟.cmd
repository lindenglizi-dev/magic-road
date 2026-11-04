@echo off
cd /d "%~dp0"
python rotation.py
if errorlevel 1 pause
