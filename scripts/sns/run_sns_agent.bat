@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Antigravity SNS Agent...
python sns_poster.py
pause
