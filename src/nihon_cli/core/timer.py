import logging
import platform
import subprocess
import sys
import time


class LearningTimer:
    """
    Manages learning sessions with a configurable timer.

    Provides functionalities for a standard 25-minute learning interval and
    a 5-second test mode. It includes a countdown display.
    """

    def __init__(
        self,
        interval_seconds: int = 1500,
        enable_sound: bool = True,
        notification_type: str = "bell",
    ) -> None:
        """
        Initializes the LearningTimer.

        Args:
            interval_seconds (int): The duration of the waiting interval in seconds.
                                  Defaults to 1500 (25 minutes).
            enable_sound (bool): Enables or disables the notification sound.
                                 Defaults to True.
            notification_type (str): The type of notification to use.
                                     Defaults to "bell".
        """
        self.interval_seconds = interval_seconds
        self.enable_sound = enable_sound
        self.notification_type = notification_type
        self.is_test = interval_seconds == 5
        logging.info(
            f"Timer initialized for {self.interval_seconds} seconds. "
            f"Test mode: {self.is_test}"
        )

    def wait_for_next_session(self) -> None:
        """
        Waits for the configured interval while displaying a countdown.

        Handles KeyboardInterrupt (Ctrl+C) to allow the user to exit gracefully.
        """
        try:
            logging.info(f"Starting to wait for {self.interval_seconds} seconds.")
            for i in range(self.interval_seconds, 0, -1):
                self.show_countdown(i)
                time.sleep(1)
            # The terminal is cleared in the main app loop.
            if self.enable_sound:
                self.play_notification_sound()
            print("\nStarting next session...")
            logging.info("Interval finished. Starting next session.")
        except KeyboardInterrupt:
            print("\nTimer stopped by user. Exiting.")
            logging.info("Timer stopped by user.")
            sys.exit(0)

    def play_notification_sound(self) -> None:
        """
        Plays a notification based on the configured type.

        This is used to notify the user that the timer has finished.
        """
        logging.info("Playing notification sound...")
        
        if self.notification_type == "bell":
            self._play_bell_sound()
        elif self.notification_type == "desktop":
            self._send_desktop_notification()
        # The "sound" type can be implemented here in the future.

    def _play_bell_sound(self) -> None:
        """
        Plays a bell sound with multiple fallback mechanisms for maximum compatibility.
        
        Uses platform-specific approaches with graceful fallbacks.
        """
        system = platform.system()
        sound_played = False
        
        if system == "Darwin":  # macOS
            # Try multiple macOS system sounds in order of preference
            macos_sounds = [
                "/System/Library/Sounds/Glass.aiff",      # Short, pleasant
                "/System/Library/Sounds/Bottle.aiff",     # Alternative
                "/System/Library/Sounds/Funk.aiff",       # Backup
                "/System/Library/Sounds/Ping.aiff"        # Last resort (has timeout issues)
            ]
            
            for sound_file in macos_sounds:
                try:
                    # Don't capture output to allow audio to play properly
                    subprocess.run([
                        "afplay", sound_file
                    ], check=True, timeout=3.0,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    logging.info(f"Successfully played macOS sound: {sound_file}")
                    sound_played = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                    logging.debug(f"Failed to play {sound_file}: {e}")
                    continue
                    
        elif system == "Linux":
            # Try Linux audio systems
            linux_commands = [
                ["paplay", "/usr/share/sounds/alsa/Front_Left.wav"],
                ["aplay", "/usr/share/sounds/alsa/Front_Left.wav"],
                ["speaker-test", "-t", "sine", "-f", "1000", "-l", "1"]
            ]
            
            for cmd in linux_commands:
                try:
                    subprocess.run(cmd, check=True, capture_output=True, timeout=2)
                    logging.info(f"Successfully played Linux sound with: {' '.join(cmd)}")
                    sound_played = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    continue
                    
        elif system == "Windows":
            # Try Windows system sounds
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
                logging.info("Successfully played Windows system beep")
                sound_played = True
            except ImportError:
                try:
                    subprocess.run([
                        "powershell", "-c",
                        "[console]::beep(800,300)"
                    ], check=True, capture_output=True, timeout=2)
                    logging.info("Successfully played Windows PowerShell beep")
                    sound_played = True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
        
        # Final fallback: System bell (though it often doesn't work in modern terminals)
        if not sound_played:
            print("\a", end="", flush=True)
            logging.warning("Fell back to system bell - may not be audible in all terminals")

    def _send_desktop_notification(self) -> None:
        """Sends a desktop notification."""
        system = platform.system()
        title = "Nihon CLI"
        message = "Time for your next learning session!"
        command = []

        if system == "Darwin":  # macOS
            command = [
                "osascript",
                "-e",
                f'display notification "{message}" with title "{title}"',
            ]
        elif system == "Linux":
            # Assumes 'notify-send' is installed.
            command = ["notify-send", title, message]
        elif system == "Windows":
            # This requires the 'BurntToast' PowerShell module to be installed.
            command = [
                "powershell",
                "-Command",
                f"New-BurntToastNotification -Text '{title}', '{message}'",
            ]

        if command:
            try:
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.info("Desktop notification sent.")
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logging.warning(
                    f"Failed to send desktop notification: {e}. Falling back to bell."
                )
                print("\a")

    def show_countdown(self, remaining_seconds: int) -> None:
        """
        Displays a countdown timer on a single line in the terminal.

        Args:
            remaining_seconds (int): The number of seconds left.
        """
        mins, secs = divmod(remaining_seconds, 60)
        timer_display = f"Next session in: {mins:02d}:{secs:02d}"
        sys.stdout.write(f"\r{timer_display}")
        sys.stdout.flush()

    def is_test_mode(self) -> bool:
        """
        Checks if the timer is running in test mode.

        Returns:
            bool: True if the interval is 5 seconds, False otherwise.
        """
        return self.is_test
