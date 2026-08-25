@echo off
python "%~dp0\..\submit_indexnow.py" %*
exit /b %errorlevel%
