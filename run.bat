@echo off
SETLOCAL

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Programs][ERROR] Python is not installed or not found in the PATH.
    exit /b 1
)

:: Create a virtual environment
if not exist .venv (
    echo [Programs][INFO] Creating virtual environment...
    python -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        echo [Programs][ERROR] Failed to create a virtual environment.
        exit /b 1
    )
)

:: Activate the virtual environment
echo [Programs][INFO] Activating virtual environment...
CALL .venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo [Programs][ERROR] Failed to activate the virtual environment.
    exit /b 1
)

:: Install libraries
if not exist .venv\Lib\site-packages\installed (
    if exist requirements.txt (
        ping 8.8.8.8 -n 1 >nul
        if %ERRORLEVEL% neq 0 (
            echo [Programs][ERROR] No network connection. Please check your internet connection and try again.
            exit /b 1
        ) else (
            echo [Programs][INFO] Installing dependencies from requirements.txt...
            echo.
            pip install -r requirements.txt
            IF %ERRORLEVEL% NEQ 0 (
                echo [Programs][ERROR] Failed to install one or more dependencies.
                exit /b 1
            )
            echo.
            echo [Programs][INFO] Dependencies installed successfully.
            type nul > .venv\Lib\site-packages\installed
        )
    ) else (
        echo [Programs][INFO] requirements.txt not found, skipping dependency installation.
    )
) else (
    echo [Programs][INFO] Dependencies already installed, skipping installation.
)

echo [Programs][INFO] Setup completed successfully.
ENDLOCAL

echo [Programs][INFO] Starting the application...
python main.py

echo [Programs][INFO] Done! Exiting...
pause