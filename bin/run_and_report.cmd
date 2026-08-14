@echo off
python "%~dp0\..\run_and_report.py" %*
exit /b %errorlevel%
