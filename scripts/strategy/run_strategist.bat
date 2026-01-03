@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Strategist Agent...
python strategist.py
pause
