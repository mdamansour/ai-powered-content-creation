@echo off
echo ========================================
echo AI Educational Content Creator
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    echo This may take a few minutes...
    pip install -r requirements.txt
    echo.
) else (
    echo Dependencies already installed.
    echo.
)

REM Run the application
echo Starting application...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run app.py

pause

@REM Made with Bob
