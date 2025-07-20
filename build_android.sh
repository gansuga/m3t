#!/bin/bash
# Android APK Build Script for Game Timer App
# Note: This requires Linux or WSL (Windows Subsystem for Linux)

echo "Game Timer App - Android Build Script"
echo "======================================"

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "Error: buildozer is not installed or not in PATH"
    echo "Please install buildozer: pip install buildozer"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Make sure you're in the project directory."
    exit 1
fi

if [ ! -f "buildozer.spec" ]; then
    echo "Error: buildozer.spec not found."
    exit 1
fi

echo "Initializing buildozer (first time setup)..."
buildozer init

echo "Building Android APK..."
echo "This may take a while on first build as it downloads dependencies..."

# Build debug APK
buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Build successful!"
    echo "APK location: bin/gametimer-0.1-armeabi-v7a-debug.apk"
    echo ""
    echo "To install on your Android device:"
    echo "1. Enable Developer Options and USB Debugging on your device"
    echo "2. Connect your device via USB"
    echo "3. Run: adb install bin/gametimer-0.1-armeabi-v7a-debug.apk"
    echo ""
    echo "Or copy the APK file to your device and install manually."
else
    echo ""
    echo "Build failed. Check the error messages above."
    echo "Common issues:"
    echo "- Make sure you're running this on Linux or WSL"
    echo "- Check that all dependencies are installed"
    echo "- Verify your Android SDK/NDK setup"
fi
