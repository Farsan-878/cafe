@echo off
REM Quick MongoDB Setup Helper for Windows

cls
echo.
echo ============================================================
echo    MongoDB Setup Helper - Choose Your Option
echo ============================================================
echo.
echo This tool will help you set up MongoDB
echo.
echo Option 1: Use MongoDB Atlas (Cloud) - RECOMMENDED for first time
echo Option 2: Install MongoDB Locally
echo Option 3: View both setup guides
echo.
echo ============================================================
echo.

:menu
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" (
    echo.
    echo Opening MongoDB Atlas setup guide...
    start notepad MONGODB_ATLAS_SETUP.md
    echo.
    echo Steps:
    echo 1. Go to https://www.mongodb.com/cloud/atlas
    echo 2. Create free account
    echo 3. Create M0 cluster
    echo 4. Add database user
    echo 5. Whitelist IP
    echo 6. Copy connection string
    echo 7. Update .env file with connection string
    echo 8. Run: python app.py
    echo.
    pause
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Opening MongoDB Local Install guide...
    start notepad MONGODB_LOCAL_INSTALL.md
    echo.
    echo Steps:
    echo 1. Download from https://www.mongodb.com/try/download/community
    echo 2. Run the MSI installer
    echo 3. Check "Install MongoDB as a Service"
    echo 4. MongoDB will auto-start
    echo 5. Run: python app.py
    echo.
    pause
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Opening both setup guides...
    start notepad MONGODB_ATLAS_SETUP.md
    start notepad MONGODB_LOCAL_INSTALL.md
    echo.
    pause
    goto end
)

echo Invalid choice. Please enter 1, 2, or 3.
echo.
goto menu

:end
echo.
echo Setup complete! Run: python app.py
echo App will be available at: http://localhost:5000
echo.
pause
