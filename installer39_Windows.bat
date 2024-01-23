@echo off

call py -3.9 --version
if %errorlevel% neq 0 (
    echo --------------------------------------
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo --------------------------------------
    echo Python 3.9 required. Impossible to install the repository. Click any key to close.
    echo --------------------------------------
    pause >nul
    exit /b %errorlevel%
)

call py -3.9 -m venv .venv_39
call .\.venv_39\Scripts\activate
call pip install -r .\requirements39_Windows.txt

echo --------------------------------------
echo Installation successfully completed. Click any key to close.
pause >nul
