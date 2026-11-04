@echo off
cd /d "%~dp0"
python rotation_rtl_model.py
if errorlevel 1 pause
