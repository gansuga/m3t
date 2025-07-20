@echo off
REM Android APK Build Script for Game Timer App (Windows)
REM Note: This requires WSL (Windows Subsystem for Linux) to be installed

echo Game Timer App - Android Build Script (Windows)
echo ================================================

REM Check if WSL is available
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: WSL is not installed or not available
    echo.
    echo To build Android APKs on Windows, you need WSL:
    echo 1. Install WSL from Microsoft Store or run: wsl --install
    echo 2. Install Ubuntu or another Linux distribution
    echo 3. In WSL, install Python and buildozer:
    echo    sudo apt update
    echo    sudo apt install python3 python3-pip
    echo    pip3 install buildozer
    echo 4. Run this script again
    pause
    exit /b 1
)

echo Switching to WSL to build Android APK...
echo.

REM Change to the current directory in WSL and run the build script
wsl cd "$(wslpath '%CD%')" ^&^& chmod +x build_android.sh ^&^& ./build_android.sh

pause
