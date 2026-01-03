@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Antigravity Designer Agent...
python design_director.py
pause
