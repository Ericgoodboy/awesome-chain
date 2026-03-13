@echo off
REM Awesome Chain Launcher for Windows

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the CLI
REM For GLM-4 compatibility, use --react flag:
REM   awesome.bat -r "your question" --react
python run.py %*

pause
