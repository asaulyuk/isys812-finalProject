@echo off
REM ========== WINDOWS ONLY — double-click in File Explorer ==========
REM (Mac users: use Run_dashboard_Mac.command in Finder instead.)

cd /d "%~dp0"
python launch_dashboard.py
if errorlevel 1 (
  echo.
  echo Try: py launch_dashboard.py
  echo Or open Anaconda Prompt, cd to this folder, then run the line above.
  pause
)
