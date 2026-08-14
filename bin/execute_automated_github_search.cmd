@echo off
python "%~dp0\..\execute_automated_github_search.py" %*
exit /b %errorlevel%
