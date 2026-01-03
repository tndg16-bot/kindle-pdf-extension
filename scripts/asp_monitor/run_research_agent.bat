@echo off
chcp 65001
cd /d "%~dp0"

echo ==========================================
echo Antigravity Research Agent - News Fetcher
echo ==========================================

:: Define your keywords here (space separated)
set KEYWORDS="AI" "Technology"

:: Define output file path (Absolute or Relative)
:: Example: ..\..\Community_Project\ASP_News_Log.md
set OUTPUT_FILE=..\..\Community_Project\ASP_News_Log.md

echo Keywords: %KEYWORDS%
echo Output: %OUTPUT_FILE%
echo.

python monitor.py --keywords %KEYWORDS% --output "%OUTPUT_FILE%"

echo.
echo Process complete.
pause
