@echo off
REM Setup script for Medical Report Analyzer (Windows)

echo 🏥 Medical Report Analyzer - Setup Script
echo ==========================================

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)
echo ✅ Python found
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    exit /b 1
)
echo ✅ Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✅ Dependencies installed

REM Create uploads directory
echo.
echo Creating uploads directory...
if not exist uploads mkdir uploads
echo ✅ Uploads directory created

REM Check Docker (optional)
echo.
docker --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker not found (optional for containerized deployment)
) else (
    echo ✅ Docker found
    docker --version
)

echo.
echo ✅ Setup complete!
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python backend\app.py
echo   3. Access at: http://localhost:5000
echo.

pause

