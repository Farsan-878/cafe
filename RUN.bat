@echo off
REM Cafe Management App - Automatic Setup and Launcher (Windows)
REM This script will install dependencies and run the Flask app

echo.
echo ============================================================
echo    Cafe Management Web Application - Auto Setup
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python installed

REM Install/Update pip
echo.
echo Updating pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies if not already done
echo Installing dependencies...
pip install -r requirements.txt --quiet

echo [OK] Dependencies installed

REM Check if .env exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env >nul
    echo [OK] .env file created
) else (
    echo [OK] .env file exists
)

REM Create data directory for MongoDB
if not exist data mkdir data
echo [OK] Data directory ready

REM Start MongoDB (if installed)
echo.
echo Checking for MongoDB...
where mongod >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB found
    echo Starting MongoDB...
    start /B mongod --dbpath ./data
    timeout /t 2 /nobreak
    echo [OK] MongoDB started
) else (
    echo [WARNING] MongoDB not found locally
    echo.
    echo MongoDB Options:
    echo.
    echo Option 1: Install MongoDB Community Edition
    echo   - Download from: https://www.mongodb.com/try/download/community
    echo.
    echo Option 2: Use MongoDB Atlas (Cloud - No installation needed)
    echo   - Go to: https://www.mongodb.com/cloud/atlas
    echo   - Create free account and cluster
    echo   - Get connection string
    echo   - Update MONGODB_URI in .env
    echo.
    set /p mongo_choice="Continue with current setup? (yes/no): "
    if /i not "%mongo_choice%"=="yes" (
        if /i not "%mongo_choice%"=="y" (
            exit /b 1
        )
    )
)

REM Start Flask app
echo.
echo ============================================================
echo    Starting Flask Application
echo ============================================================
echo.
echo App will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

python app.py

pause
