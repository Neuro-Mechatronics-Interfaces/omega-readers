@echo off

call py -3.10 --version
if %errorlevel% neq 0 (
    echo --------------------------------------
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo --------------------------------------
    echo Python 3.10 required. Impossible to install the repository. Click any key to close.
    echo --------------------------------------
    pause >nul
    exit /b %errorlevel%
)

call py -3.10 -m venv .venv_310
call .\.venv_310\Scripts\activate
call pip install -r .\requirements310_Windows.txt

echo --------------------------------------
echo Installation successfully completed. Click any key to close.
pause >nul
