#!/usr/bin/env python3
"""
Two-Player Game Timer App
A simple timer app for turn-based games like shogi.
"""

import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import PopMatrix, PushMatrix, Rotate
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class SettingsScreen(BoxLayout):
    """Initial settings screen for configuring game parameters."""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 20

        # Load saved settings
        self.load_settings()

        self.build_ui()

    def load_settings(self):
        """Load settings from local storage."""
        try:
            if self.app.store.exists("settings"):
                settings = self.app.store.get("settings")
                self.default_time = settings.get("time_minutes", 15)
            else:
                self.default_time = 15
        except Exception:
            self.default_time = 15

    def build_ui(self):
        """Build the settings UI."""
        # Title
        title = Label(
            text="Game Timer Settings", font_size="32sp", size_hint_y=0.2, bold=True
        )
        self.add_widget(title)

        # Time input section
        time_layout = BoxLayout(orientation="horizontal", size_hint_y=0.2)
        time_layout.add_widget(
            Label(text="Time per player (minutes):", font_size="20sp", size_hint_x=0.7)
        )

        self.time_input = TextInput(
            text=str(self.default_time),
            font_size="20sp",
            size_hint_x=0.3,
            multiline=False,
            input_filter="int",
        )
        time_layout.add_widget(self.time_input)
        self.add_widget(time_layout)

        # Spacer - larger space without starting player selection
        self.add_widget(Label(text="", size_hint_y=0.4))

        # Start button
        start_button = Button(
            text="Start Game",
            font_size="24sp",
            size_hint_y=0.2,
            background_color=(0.2, 0.8, 0.2, 1),
        )
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

    def start_game(self, instance):
        """Start the game with current settings."""
        try:
            time_minutes = int(self.time_input.text)
            if time_minutes <= 0:
                raise ValueError("Time must be positive")
        except ValueError:
            # Reset to default if invalid input
            time_minutes = 15
            self.time_input.text = "15"

        # Save settings (only time now)
        self.app.store.put("settings", time_minutes=time_minutes)

        # Switch to timer screen (no starting player needed)
        self.app.switch_to_timer(time_minutes)


class TimerScreen(BoxLayout):
    """Main timer screen for the game."""

    def __init__(self, app_instance, time_minutes, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.orientation = "vertical"

        # Timer state
        self.total_time = time_minutes * 60  # Convert to seconds
        self.upper_time = self.total_time
        self.lower_time = self.total_time
        self.active_player = None  # No active player initially
        self.last_update_time = None

        # Game states: 'waiting_for_start', 'choosing_first_player', 'active_turn', 'paused'
        self.game_state = "waiting_for_start"

        self.build_ui()

        # Start the clock
        self.clock_event = Clock.schedule_interval(self.update_timer, 0.1)

    def build_ui(self):
        """Build the timer UI."""
        # Upper player section (rotated display)
        upper_layout = BoxLayout(orientation="vertical", size_hint_y=0.4)

        self.upper_time_label = Label(
            text=self.format_time(self.upper_time),
            font_size="48sp",
            bold=True,
            size_hint_y=0.6,
        )

        # Rotate the upper time label 180 degrees
        with self.upper_time_label.canvas.before:
            PushMatrix()
            self.upper_rotation = Rotate()
            self.upper_rotation.angle = 180
            self.upper_rotation.origin = (0, 0)  # Will be set properly in on_size

        with self.upper_time_label.canvas.after:
            PopMatrix()

        # Bind to update rotation origin when size changes
        self.upper_time_label.bind(size=self.update_upper_rotation)

        self.upper_button = Button(
            text="READY",
            font_size="20sp",
            size_hint_y=0.4,
            background_color=(0.3, 0.3, 0.8, 1),
        )
        self.upper_button.bind(on_press=self.upper_player_turn)

        # Rotate the upper button 180 degrees
        with self.upper_button.canvas.before:
            PushMatrix()
            self.upper_button_rotation = Rotate()
            self.upper_button_rotation.angle = 180
            self.upper_button_rotation.origin = (
                0,
                0,
            )  # Will be set properly in on_size

        with self.upper_button.canvas.after:
            PopMatrix()

        # Bind to update rotation origin when size changes
        self.upper_button.bind(size=self.update_upper_button_rotation)

        upper_layout.add_widget(self.upper_time_label)
        upper_layout.add_widget(self.upper_button)
        self.add_widget(upper_layout)

        # Control buttons section
        control_layout = BoxLayout(orientation="horizontal", size_hint_y=0.2)

        self.pause_button = Button(
            text="Start",
            font_size="20sp",
            size_hint_x=0.7,
            background_color=(0.2, 0.8, 0.2, 1),
        )
        self.pause_button.bind(on_press=self.toggle_pause)

        end_button = Button(
            text="End",
            font_size="20sp",
            size_hint_x=0.3,
            background_color=(0.8, 0.2, 0.2, 1),
        )
        end_button.bind(on_press=self.end_game)

        control_layout.add_widget(self.pause_button)
        control_layout.add_widget(end_button)
        self.add_widget(control_layout)

        # Lower player section
        lower_layout = BoxLayout(orientation="vertical", size_hint_y=0.4)

        self.lower_button = Button(
            text="READY",
            font_size="20sp",
            size_hint_y=0.4,
            background_color=(0.8, 0.3, 0.3, 1),
        )
        self.lower_button.bind(on_press=self.lower_player_turn)

        self.lower_time_label = Label(
            text=self.format_time(self.lower_time),
            font_size="48sp",
            bold=True,
            size_hint_y=0.6,
        )

        lower_layout.add_widget(self.lower_button)
        lower_layout.add_widget(self.lower_time_label)
        self.add_widget(lower_layout)

        self.update_button_states()

    def update_upper_rotation(self, instance, size):
        """Update the rotation origin for upper time label."""
        self.upper_rotation.origin = (instance.center_x, instance.center_y)

    def update_upper_button_rotation(self, instance, size):
        """Update the rotation origin for upper button."""
        self.upper_button_rotation.origin = (instance.center_x, instance.center_y)

    def format_time(self, seconds):
        """Format time in MM:SS format."""
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def update_timer(self, dt):
        """Update the active timer."""
        if self.game_state != "active_turn":
            self.last_update_time = None
            return

        current_time = time.time()
        if self.last_update_time is None:
            self.last_update_time = current_time
            return

        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # Subtract elapsed time from active player
        if self.active_player == "upper":
            self.upper_time -= elapsed
        elif self.active_player == "lower":
            self.lower_time -= elapsed

        # Update displays
        self.upper_time_label.text = self.format_time(self.upper_time)
        self.lower_time_label.text = self.format_time(self.lower_time)

        # Check for time out
        if self.upper_time <= 0 or self.lower_time <= 0:
            self.game_state = "paused"
            self.active_player = None
            self.update_button_states()

    def upper_player_turn(self, instance):
        """Handle upper player button press."""
        if self.game_state == "choosing_first_player":
            # Start upper player's turn
            self.active_player = "upper"
            self.game_state = "active_turn"
            self.last_update_time = time.time()
            self.update_button_states()
        elif self.game_state == "active_turn" and self.active_player == "upper":
            # End upper player's turn, switch to lower
            self.active_player = "lower"
            self.last_update_time = time.time()
            self.update_button_states()

    def lower_player_turn(self, instance):
        """Handle lower player button press."""
        if self.game_state == "choosing_first_player":
            # Start lower player's turn
            self.active_player = "lower"
            self.game_state = "active_turn"
            self.last_update_time = time.time()
            self.update_button_states()
        elif self.game_state == "active_turn" and self.active_player == "lower":
            # End lower player's turn, switch to upper
            self.active_player = "upper"
            self.last_update_time = time.time()
            self.update_button_states()

    def toggle_pause(self, instance):
        """Handle Start/Pause button press."""
        if self.game_state == "waiting_for_start":
            # Start the game - show first player selection
            self.game_state = "choosing_first_player"
            self.update_button_states()
        elif self.game_state == "active_turn":
            # Pause the game
            self.game_state = "paused"
            self.update_button_states()
        elif self.game_state == "paused":
            # Resume the game
            self.game_state = "active_turn"
            self.last_update_time = time.time()
            self.update_button_states()

    def update_button_states(self):
        """Update button states based on current game state."""
        if self.game_state == "waiting_for_start":
            self.pause_button.text = "Start"
            self.pause_button.background_color = (0.2, 0.8, 0.2, 1)
            self.upper_button.text = "READY"
            self.lower_button.text = "READY"

        elif self.game_state == "choosing_first_player":
            self.pause_button.text = "Pause"
            self.pause_button.background_color = (0.8, 0.8, 0.2, 1)
            self.upper_button.text = "START MY\nTURN"
            self.lower_button.text = "START MY\nTURN"

        elif self.game_state == "active_turn":
            self.pause_button.text = "Pause"
            self.pause_button.background_color = (0.8, 0.8, 0.2, 1)
            if self.active_player == "upper":
                self.upper_button.text = "END MY\nTURN"
                self.lower_button.text = "WAITING..."
            else:
                self.upper_button.text = "WAITING..."
                self.lower_button.text = "END MY\nTURN"

        elif self.game_state == "paused":
            self.pause_button.text = "Resume"
            self.pause_button.background_color = (0.2, 0.8, 0.2, 1)
            if self.active_player == "upper":
                self.upper_button.text = "MY TURN\n(PAUSED)"
                self.lower_button.text = "WAITING..."
            elif self.active_player == "lower":
                self.upper_button.text = "WAITING..."
                self.lower_button.text = "MY TURN\n(PAUSED)"
            else:
                self.upper_button.text = "READY"
                self.lower_button.text = "READY"

    def end_game(self, instance):
        """End the game and return to settings."""
        Clock.unschedule(self.clock_event)
        self.app.switch_to_settings()


class GameTimerApp(App):
    """Main application class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_screen = None
        # Set up storage
        self.store = JsonStore("game_timer_settings.json")

    def build(self):
        """Build the application."""
        # Set window properties
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        # Start with settings screen
        self.current_screen = SettingsScreen(self)
        return self.current_screen

    def switch_to_timer(self, time_minutes):
        """Switch to timer screen."""
        self.root.clear_widgets()
        self.current_screen = TimerScreen(self, time_minutes)
        self.root.add_widget(self.current_screen)

    def switch_to_settings(self):
        """Switch to settings screen."""
        self.root.clear_widgets()
        self.current_screen = SettingsScreen(self)
        self.root.add_widget(self.current_screen)


if __name__ == "__main__":
    GameTimerApp().run()
