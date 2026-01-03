@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Antigravity Content Agent...
python content_creator.py
pause
