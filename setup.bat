@echo off
echo ===================================
echo Recipe Genie - Installation Script
echo ===================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    echo Please make sure you have venv module installed.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Creating launch script...
(
echo @echo off
echo call .venv\Scripts\activate
echo python main.py
echo pause
) > RecipeGenie.bat

echo.
echo ===================================
echo Installation complete!
echo.
echo To start Recipe Genie, double-click on RecipeGenie.bat
echo.
echo Before using, make sure to update config.json with your API key.
echo ===================================
echo.
pause
