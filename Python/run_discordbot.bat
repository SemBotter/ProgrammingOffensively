@echo off
:: Check for elevated permissions
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with elevated permissions
) else (
    echo Requesting elevated permissions
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0run_discordbot.bat' -Verb RunAs"
    exit /b
)

:: Change to the directory of the script
cd /d %~dp0

:: Debugging output
echo Current directory: %cd%
echo Activating virtual environment...

:: Activate the environment
call .\venv\Scripts\activate

:: Debugging output
echo Running discordbot.py...

:: Run the discordbot.py script
python discordbot.py
