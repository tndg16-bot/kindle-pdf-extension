@echo off
chcp 65001
cd /d "%~dp0"
echo Starting Antigravity Ideation Agent...
echo Ensuring Ollama is accessible...
python ideation_wizard_v2.py
pause
