@echo off
REM MongoDB Local Setup and Start Script

cls
echo.
echo ============================================================
echo    MongoDB Local Setup & Start
echo ============================================================
echo.

REM Check if MongoDB is running
tasklist /FI "IMAGENAME eq mongod.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB is already RUNNING!
    echo.
    echo Details:
    echo   - Process: mongod.exe
    echo   - Default Port: 27017
    echo   - Host: localhost
    echo.
    goto update_env
) else (
    echo [INFO] MongoDB is not running yet
    echo.
)

REM Try to find MongoDB installation
echo Searching for MongoDB installation...
setlocal enabledelayedexpansion

REM Check common installation paths
for /d %%D in ("C:\Program Files\MongoDB\Server\*") do (
    if exist "%%D\bin\mongod.exe" (
        set MONGO_BIN=%%D\bin\mongod.exe
        set MONGO_DIR=%%D
        echo [OK] Found MongoDB at: %%D
        goto start_mongo
    )
)

echo [WARNING] MongoDB executable not found in Program Files
echo.
echo Please ensure MongoDB is installed properly:
echo 1. Download from: https://www.mongodb.com/try/download/community
echo 2. Run MSI installer
echo 3. Check "Install MongoDB as a Service"
echo 4. Restart this script
echo.
pause
exit /b 1

:start_mongo
echo.
echo Creating data directory...
if not exist "C:\data\db" (
    mkdir C:\data\db
    echo [OK] Created C:\data\db
) else (
    echo [OK] Data directory exists
)

echo.
echo ============================================================
echo    Starting MongoDB Service
echo ============================================================
echo.

REM Try to start MongoDB service
echo Attempting to start MongoDB service...
net start MongoDB >nul 2>&1

if %errorlevel% equ 0 (
    echo [OK] MongoDB service started successfully!
    timeout /t 2 /nobreak
    goto verify_connection
) else (
    echo [INFO] Service start failed, trying manual start...
    echo.
    echo Starting mongod manually...
    start "MongoDB" "!MONGO_BIN!" --dbpath C:\data\db
    timeout /t 3 /nobreak
    goto verify_connection
)

:verify_connection
echo.
echo ============================================================
echo    Verifying MongoDB Connection
echo ============================================================
echo.

REM Test connection
tasklist /FI "IMAGENAME eq mongod.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB is RUNNING
    echo.
    echo Connection Details:
    echo   - Host: localhost
    echo   - Port: 27017
    echo   - URI: mongodb://localhost:27017/cafe_db
    echo.
    goto update_env
) else (
    echo [ERROR] MongoDB failed to start
    echo.
    echo Troubleshooting:
    echo 1. Check if port 27017 is available
    echo 2. Ensure MongoDB is installed correctly
    echo 3. Create C:\data\db folder manually
    echo 4. Try restarting your computer
    echo.
    pause
    exit /b 1
)

:update_env
echo.
echo ============================================================
echo    Checking Application Configuration
echo ============================================================
echo.

REM Check .env file
if exist ".env" (
    echo [OK] .env file exists
    echo.
    echo Current MONGODB_URI from .env:
    for /f "tokens=2 delims==" %%A in ('findstr /I "MONGODB_URI" .env') do echo   %%A
) else (
    echo [WARNING] .env file not found
    echo.
    echo Creating .env from .env.example...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [OK] .env created
    )
)

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo.
echo 1. Ensure .env has:
echo    MONGODB_URI=mongodb://localhost:27017/cafe_db
echo.
echo 2. Install Python dependencies (if not done):
echo    pip install -r requirements.txt
echo.
echo 3. Start Flask app:
echo    python app.py
echo.
echo 4. Open browser:
echo    http://localhost:5000
echo.
echo 5. Test CRUD:
echo    - Add Item
echo    - View Items
echo    - Edit Item
echo    - Delete Item
echo.
echo ============================================================
echo.
echo Keeping this window open while MongoDB runs...
echo Close this window to stop MongoDB.
echo.
pause
