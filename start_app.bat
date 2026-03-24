@echo off
title MediScan AI
color 0A
cd /d "%~dp0"

echo.
echo  ============================================================
echo.
echo        ooo   ooo  ooooooooo  ooooooo   ooooo  oooooooo
echo        888   888  888       888    888  888    888     
echo        888ooo888  888ooooo  888    888  888    888ooooo
echo        888   888  888       888    888  888         888
echo        888   888  888       888    888  888    888  888
echo        888   888  ooooooooo  ooooooo   ooooo   oooooooo
echo.
echo                   MediScan AI  ^|  Disease Prediction
echo                   Powered by Machine Learning
echo.
echo  ============================================================
echo.

:: ── Check Python ──────────────────────────────────────────────
echo  [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [FAIL] Python not found on this machine.
    echo         Download it from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  [ OK ] %PYVER% detected

:: ── Check app.py ──────────────────────────────────────────────
echo  [2/3] Checking project files...
if not exist "app.py" (
    echo.
    echo  [FAIL] app.py not found. Make sure you're running this
    echo         from the correct project folder.
    echo.
    pause
    exit /b 1
)
if not exist "disease_model.pkl" (
    echo.
    echo  [WARN] disease_model.pkl not found.
    echo         Run model.py first to train and save the model.
    echo.
    pause
    exit /b 1
)
echo  [ OK ] All project files found

:: ── Check Flask ───────────────────────────────────────────────
echo  [3/3] Checking Flask installation...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [INFO] Flask not found. Installing dependencies...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  [FAIL] Failed to install dependencies.
        echo         Try running: pip install -r requirements.txt manually.
        echo.
        pause
        exit /b 1
    )
)
echo  [ OK ] Flask is ready

echo.
echo  ============================================================
echo   Server  :  http://127.0.0.1:5000
echo   Mode    :  Development  ^|  Debug ON
echo   Stop    :  Press Ctrl+C in this window
echo  ============================================================
echo.

:: ── Launch Flask ──────────────────────────────────────────────
python app.py

echo.
echo  ============================================================
echo   Server has stopped.
echo  ============================================================
echo.
pause
