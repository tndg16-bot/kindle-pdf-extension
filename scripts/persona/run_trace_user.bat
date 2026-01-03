@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Persona Trace Module...
python trace_user.py
pause
