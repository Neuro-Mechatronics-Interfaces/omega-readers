@echo off

call py -3.8 --version
if %errorlevel% neq 0 (
    echo --------------------------------------
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo --------------------------------------
    echo Python 3.8 required. Impossible to install the repository. Click any key to close.
    echo --------------------------------------
    pause >nul
    exit /b %errorlevel%
)

call py -3.8 -m venv .venv_psychopy
call .\.venv_psychopy\Scripts\activate
pip install -r .\requirements39_Windows.txt
echo --------------------------------------
pip install PsychoPy==2023.1.2
echo --------------------------------------
pip install scikit-learn==1.3.1
echo --------------------------------------
pip install easygui
echo --------------------------------------
echo installation successfully completed
echo --------------------------------------
echo press any button to close 
pause >nul