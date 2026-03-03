@echo off
REM Horse Racing Management System - Setup Script for Windows

echo Horse Racing Management System - Setup
echo ========================================
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo Dependencies installed

REM Create database
echo Initializing database...
if exist "horse_races.db" (
    echo Old database found. Backing up to horse_races.db.bak
    move /Y horse_races.db horse_races.db.bak >nul
)

python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created/updated')"

echo.
echo Setup complete!
echo.
echo To run the application:
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
echo Then open http://127.0.0.1:5000 in your browser
pause
