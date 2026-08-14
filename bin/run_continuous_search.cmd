@echo off
python "%~dp0\..\run_continuous_search.py" %*
exit /b %errorlevel%
