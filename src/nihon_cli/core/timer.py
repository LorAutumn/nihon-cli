import time
import os
import sys
import logging

class LearningTimer:
    """
    Manages learning sessions with a configurable timer.

    Provides functionalities for a standard 25-minute learning interval and
    a 5-second test mode. It includes a countdown display and handles
    terminal clearing between sessions for a clean user interface.
    """

    def __init__(self, interval_seconds: int = 1500):
        """
        Initializes the LearningTimer.

        Args:
            interval_seconds (int): The duration of the waiting interval in seconds.
                                  Defaults to 1500 (25 minutes).
        """
        self.interval_seconds = interval_seconds
        self.is_test = (interval_seconds == 5)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f"Timer initialized for {self.interval_seconds} seconds. Test mode: {self.is_test}")

    def wait_for_next_session(self):
        """
        Waits for the configured interval while displaying a countdown.

        Handles KeyboardInterrupt (Ctrl+C) to allow the user to exit gracefully.
        """
        try:
            logging.info(f"Starting to wait for {self.interval_seconds} seconds.")
            for i in range(self.interval_seconds, 0, -1):
                self.show_countdown(i)
                time.sleep(1)
            self.clear_terminal()
            print("Starting next session...")
            logging.info("Interval finished. Starting next session.")
        except KeyboardInterrupt:
            print("\nTimer stopped by user. Exiting.")
            logging.info("Timer stopped by user.")
            sys.exit(0)

    def clear_terminal(self):
        """
        Clears the terminal screen.

        Uses 'cls' for Windows and 'clear' for macOS and Linux.
        """
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        logging.info("Terminal cleared.")

    def show_countdown(self, remaining_seconds: int):
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
