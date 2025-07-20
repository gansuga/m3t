# Two-Player Game Timer

A simple timer application for turn-based games like shogi, chess, or go. Built with Python and Kivy.

## Features

- **Initial Settings Screen**: Configure game time
- **Timer Screen**: Visual timer with large buttons for each player
- **Rotated Upper Display**: Upper side text is rotated 180° for shared device use
- **Flexible Start**: Either player can start the game by pressing their button first
- **Persistent Settings**: Automatically saves and loads previous time settings
- **Pause/Resume**: Pause both timers during breaks
- **Symmetric Design**: Both players can comfortably use the shared device

## Requirements

- Python 3.7+
- Kivy 2.1.0+
- Buildozer (for Android APK generation)

## Installation

### Desktop Testing

1. Install Python dependencies:
```bash
pip install kivy>=2.1.0
```

2. Run the application:
```bash
python main.py
# or
python test_app.py
```

### Android APK Build

#### Windows (using WSL)
1. Install WSL and Ubuntu from Microsoft Store
2. In WSL, install dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install buildozer kivy
```
3. Run the build script:
```bash
# From Windows Command Prompt or PowerShell
build_android.bat
```

#### Linux/macOS
1. Install dependencies:
```bash
pip install buildozer kivy
```
2. Run the build script:
```bash
chmod +x build_android.sh
./build_android.sh
```

## Usage

1. **Settings Screen**: 
   - Set the total time per player (default: 15 minutes)
   - Tap "Start Game"

2. **Timer Screen**:
   - **Upper side**: Text is rotated 180° for easy reading from opposite side
   - **Lower side**: Normal orientation
   - Either player can start by tapping their button first
   - Only one timer runs at a time
   - Use "Pause" to stop both timers temporarily
   - Use "End" to return to settings

## Installing on Android

After building the APK:

1. **Enable Developer Options** on your Android device:
   - Go to Settings > About phone
   - Tap "Build number" 7 times
   - Go back to Settings > Developer options
   - Enable "USB debugging"

2. **Install via ADB** (if connected to computer):
```bash
adb install bin/gametimer-0.1-armeabi-v7a-debug.apk
```

3. **Manual Installation**:
   - Copy the APK file to your device
   - Open file manager and tap the APK
   - Allow installation from unknown sources if prompted

## File Structure

- `main.py` - Main application code with rotated upper display
- `test_app.py` - Desktop testing script
- `buildozer.spec` - Android build configuration
- `build_android.sh` - Linux/macOS build script
- `build_android.bat` - Windows build script (uses WSL)
- `requirements.txt` - Python dependencies
- `game_timer_settings.json` - Local settings storage (created automatically)

## Technical Details

- Uses Kivy's graphics transformations for 180° text rotation
- Clock-based timer with 0.1-second precision
- Vertical orientation optimized for shared device usage
- JsonStore for persistent settings
- No external dependencies beyond Kivy

## License

MIT License - see LICENSE file for details
