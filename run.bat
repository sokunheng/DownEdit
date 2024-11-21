@echo off

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Programs][ERROR] Python is not installed or not found in the PATH.
    exit /b 1
)

if not exist venv (
    echo [Programs][INFO] Creating virtual environment...
    python -m venv .venv
)

echo [Programs][INFO] Activating virtual environment...
call venv\Scripts\activate.bat

if not exist venv\Lib\site-packages\installed (
    if exist requirements.txt (
        echo [Programs][INFO] Installing dependencies from requirements.txt...
        echo.
        pip install -r requirements.txt
        echo.
        echo [Programs][INFO] Dependencies installed successfully.
    ) else (
        echo [Programs][INFO] requirements.txt not found, skipping dependency installation.
    )
) else (
    echo [Programs][INFO] Dependencies already installed, skipping installation.
)

echo [Programs][INFO] Starting the application...
python main.py

echo [Programs][INFO] Done! Exiting...
pause
