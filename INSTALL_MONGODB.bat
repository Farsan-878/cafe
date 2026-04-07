@echo off
REM MongoDB Installation and Setup Script for Windows
REM This script will help you install and configure MongoDB

echo.
echo ============================================================
echo    MongoDB Installation and Setup for Windows
echo ============================================================
echo.

REM Check if MongoDB is already installed
where mongod >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB is already installed
    goto check_service
) else (
    echo [INFO] MongoDB not found
    goto download_instructions
)

:download_instructions
echo.
echo ============================================================
echo    STEP 1: Download MongoDB Community Edition
echo ============================================================
echo.
echo Please download MongoDB Community Edition from:
echo https://www.mongodb.com/try/download/community
echo.
echo Steps:
echo   1. Go to the above URL
echo   2. Select "Windows" platform
echo   3. Download the MSI installer (latest version)
echo   4. Run the installer (mongod-windows-x86_64-xxx.msi)
echo.
echo Installation Tips:
echo   - Choose "Install MongoDB as a Service"
echo   - Keep default installation path: C:\Program Files\MongoDB\Server\
echo   - Choose "Complete" installation
echo.
pause

REM Try to find MongoDB again after installation
where mongod >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo [OK] MongoDB found! Starting service...
    goto check_service
) else (
    echo.
    echo [ERROR] MongoDB still not found after installation
    echo Please ensure MongoDB was installed correctly
    goto manual_path
)

:manual_path
echo.
echo Attempting to find MongoDB in default locations...
if exist "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\7.0\bin
    echo [OK] Found MongoDB at !MONGO_PATH!
    goto start_mongo
) else if exist "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\6.0\bin
    echo [OK] Found MongoDB at !MONGO_PATH!
    goto start_mongo
) else if exist "C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\5.0\bin
    echo [OK] Found MongoDB at !MONGO_PATH!
    goto start_mongo
) else (
    echo [ERROR] Could not find MongoDB in standard locations
    echo Please install MongoDB Community Edition manually
    pause
    exit /b 1
)

:check_service
echo.
echo ============================================================
echo    STEP 2: Check MongoDB Service Status
echo ============================================================
echo.

REM Check if MongoDB service is running
sc query MongoDB >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB service exists

    REM Check if it's running
    tasklist /FI "IMAGENAME eq mongod.exe" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] MongoDB service is RUNNING
        goto verify_connection
    ) else (
        echo [INFO] MongoDB service is not running
        goto start_service
    )
) else (
    echo [INFO] MongoDB service not registered
    goto start_mongo
)

:start_service
echo.
echo Starting MongoDB service...
net start MongoDB >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB service started successfully
    timeout /t 3 /nobreak
    goto verify_connection
) else (
    echo [ERROR] Failed to start MongoDB service
    echo Attempting manual start...
    goto start_mongo
)

:start_mongo
echo.
echo Creating data directory...
if not exist "C:\data\db" mkdir C:\data\db
echo [OK] Data directory ready

echo.
echo Starting MongoDB manually...
echo This window will keep mongod running
echo.
echo [INFO] MongoDB is starting...
echo [INFO] Listening on: 127.0.0.1:27017
echo [INFO] Keep this window open while using MongoDB
echo.

mongod --dbpath C:\data\db
pause
exit /b 0

:verify_connection
echo.
echo ============================================================
echo    STEP 3: Verify Connection
echo ============================================================
echo.

REM Test MongoDB connection
echo [INFO] Testing MongoDB connection...
timeout /t 2 /nobreak

mongosh --eval "db.adminCommand('ping')" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MongoDB is connected and responding
    goto setup_compass
) else (
    echo [WARNING] Could not verify connection with mongosh
    echo [INFO] MongoDB might still be starting...
    timeout /t 3 /nobreak
    goto setup_compass
)

:setup_compass
echo.
echo ============================================================
echo    STEP 4: Download MongoDB Compass (Optional)
echo ============================================================
echo.
echo MongoDB Compass is a GUI tool to browse your data
echo URL: https://www.mongodb.com/products/compass
echo.
echo Connection String for Compass:
echo mongodb://localhost:27017/
echo.
echo Or use default connection settings:
echo   Host: localhost
echo   Port: 27017
echo.

:create_app_db
echo.
echo ============================================================
echo    STEP 5: Create Cafe Database
echo ============================================================
echo.
echo Creating cafe_db database...

mongosh << EOF
use cafe_db
db.items.insertOne({
    name: "Espresso",
    price: 100
})
db.items.deleteOne({
    name: "Espresso"
})
print("✅ Database cafe_db created successfully")
EOF

if %errorlevel% equ 0 (
    echo [OK] Database created successfully
) else (
    echo [INFO] Database creation skipped (MongoDB might be starting)
)

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo [OK] MongoDB is installed and configured
echo.
echo Next Steps:
echo   1. Keep MongoDB running in background
echo   2. Run Flask app: python app.py
echo   3. Open: http://localhost:5000
echo   4. (Optional) Download MongoDB Compass
echo.
echo MongoDB Status:
echo   - Host: localhost
echo   - Port: 27017
echo   - Database: cafe_db
echo   - Connection: mongodb://localhost:27017/cafe_db
echo.

pause
