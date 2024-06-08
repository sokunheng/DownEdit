@echo off

if not exist venv (
    echo [Programs][INFO] Creating virtual environment...
    python -m venv venv
)

echo [Programs][INFO] Activating virtual environment...
call venv\Scripts\activate

if not exist venv\Lib\site-packages\installed (
    if exist requirements.txt (
        echo [Programs][INFO] Installing dependencies...
        pip install -r requirements.txt
        echo. > venv\Lib\site-packages\installed
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
