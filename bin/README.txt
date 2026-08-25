Wrappers created to allow Antigravity or other runners to invoke repository tools from this path.

How to use:
- Call the PowerShell wrapper: powershell -File "...\bin\execute_automated_github_search.ps1" -- arg1 arg2
- Or call the CMD shim: "...\bin\execute_automated_github_search.cmd" arg1 arg2

Included wrappers (name -> script):
- execute_automated_github_search -> execute_automated_github_search.py
- multi_engine_search_suite -> multi_engine_search_suite.py
- run_continuous_search -> run_continuous_search.py
- submit_indexnow -> submit_indexnow.py
- google_bypass_searcher -> google_bypass_searcher.py
- ddg_bypass_searcher -> ddg_bypass_searcher.py
- run_and_report -> run_and_report.py

If Antigravity expects executables without extensions, configure it to scan this bin directory or add it to PATH.
