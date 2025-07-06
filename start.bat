@echo off
CHDIR /D "%~dp0"
title InkFlow One-Click Launcher

echo ==================================================
echo  InkFlow One-Click Launcher
echo ==================================================
echo.

set "BACKEND_DIR=ink-backend"
set "FRONTEND_DIR=ink-electron-vue"

:: Backend Setup
echo [1/4] Setting up backend environment...
if not exist "%BACKEND_DIR%\.env" (
    if exist "%BACKEND_DIR%\env_example" (
        echo   - .env file not found, creating from env_example...
        copy "%BACKEND_DIR%\env_example" "%BACKEND_DIR%\.env" > nul
        echo   - SUCCESS: .env file created.
        echo   - IMPORTANT: Please review "%BACKEND_DIR%\.env" to ensure CHROME_PATH and WEBDRIVER_CHROME_DRIVER are correct.
        echo.
    ) else (
        echo   - WARNING: env_example not found in "%BACKEND_DIR%". Backend might not work correctly.
        echo.
    )
) else (
    echo   - .env file already exists. Skipping creation.
    echo.
)

:: Install Backend Dependencies
echo [2/4] Installing backend dependencies...
echo   - Note: Pip will automatically skip packages that are already satisfied.
pushd %BACKEND_DIR%
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install backend dependencies. Please check the error message above.
    pause
    exit /b 1
)
popd
echo   - Backend dependencies check complete.
echo.

:: Install Frontend Dependencies
echo [3/4] Installing frontend dependencies...
if exist "%FRONTEND_DIR%\node_modules" (
    set /p "skip_npm=Frontend 'node_modules' folder exists. Skip 'npm install'? (y/n): "
    if /i "%skip_npm%"=="y" (
        echo   - Skipping frontend dependency installation as requested.
    ) else (
        pushd %FRONTEND_DIR%
        call npm install
        if %errorlevel% neq 0 (
            echo.
            echo ERROR: Failed to install frontend dependencies. Please check the error message above.
            pause
            exit /b 1
        )
        popd
        echo   - Frontend dependencies installed successfully.
    )
) else (
    echo   - 'node_modules' not found, running 'npm install'...
    pushd %FRONTEND_DIR%
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install frontend dependencies. Please check the error message above.
        pause
        exit /b 1
    )
    popd
    echo   - Frontend dependencies installed successfully.
)
echo.

:: Start services
echo [4/4] Starting services...
echo   - Starting Backend service in a new window...
start "InkFlow Backend" cmd /k "node start-backend.js"

echo   - Starting Frontend service in a new window...
start "InkFlow Frontend" cmd /k "node start-frontend.js"

echo.
echo ==================================================
echo  All services have been launched.
echo  The new windows will show logs for each service.
echo  You can close this window now.
echo ==================================================
echo.

pause 