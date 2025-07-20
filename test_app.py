#!/usr/bin/env python3
"""
Test script to run the game timer app on desktop.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import GameTimerApp

if __name__ == "__main__":
    print("Starting Game Timer App...")
    print("- Use this to test the app on desktop before building for Android")
    print("- Upper player display should be rotated 180 degrees")
    print("- Press Ctrl+C or close window to exit")

    try:
        GameTimerApp().run()
    except KeyboardInterrupt:
        print("\nApp stopped by user")
    except Exception as e:
        print(f"Error running app: {e}")
        import traceback

        traceback.print_exc()
