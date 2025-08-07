import logging
import os
import platform
import subprocess
import sys
import time
from typing import Optional


class LearningTimer:
    """
    Manages learning sessions with a configurable timer.

    Provides functionalities for a standard 25-minute learning interval and
    a 5-second test mode. It includes a countdown display and robust audio notifications.
    """

    def __init__(self, interval_seconds: int = 1500) -> None:
        """
        Initializes the LearningTimer.

        Args:
            interval_seconds (int): The duration of the waiting interval in seconds.
                                  Defaults to 1500 (25 minutes).
        """
        self.interval_seconds = interval_seconds
        self.is_test = interval_seconds == 5
        self._audio_method: Optional[str] = None
        self._is_vscode_terminal = self._detect_vscode_terminal()
        logging.info(
            f"Timer initialized for {self.interval_seconds} seconds. "
            f"Test mode: {self.is_test}, VSCode terminal: {self._is_vscode_terminal}"
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
            print("\nStarting next session...")
            # Robust audio notification with fallback mechanisms
            self._play_notification_sound()
            logging.info("Interval finished. Starting next session.")
        except KeyboardInterrupt:
            print("\nTimer stopped by user. Exiting.")
            logging.info("Timer stopped by user.")
            sys.exit(0)

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

    def _detect_vscode_terminal(self) -> bool:
        """
        Detects if the application is running in a VSCode terminal.

        Returns:
            bool: True if running in VSCode terminal, False otherwise.
        """
        # Check for VSCode-specific environment variables
        vscode_indicators = [
            'VSCODE_INJECTION',
            'VSCODE_PID',
            'TERM_PROGRAM',
            'VSCODE_IPC_HOOK',
            'VSCODE_IPC_HOOK_CLI'
        ]
        
        for indicator in vscode_indicators:
            if indicator in os.environ:
                if indicator == 'TERM_PROGRAM' and os.environ[indicator] == 'vscode':
                    return True
                elif indicator != 'TERM_PROGRAM':
                    return True
        
        # Additional check for terminal capabilities
        if os.environ.get('TERM', '').startswith('xterm') and 'VSCODE' in str(os.environ):
            return True
            
        return False

    def _play_notification_sound(self) -> None:
        """
        Plays a notification sound using multiple fallback methods.
        
        Tries different audio methods in order of preference:
        1. Platform-specific audio commands (works in VSCode)
        2. System bell (if not in VSCode)
        3. Visual notification as last resort
        """
        methods = [
            ('platform_audio', self._try_platform_audio),
            ('system_bell', self._try_system_bell),
            ('visual_notification', self._show_visual_notification)
        ]
        
        for method_name, method_func in methods:
            try:
                if method_func():
                    self._audio_method = method_name
                    logging.debug(f"Audio notification successful using: {method_name}")
                    return
            except Exception as e:
                logging.debug(f"Audio method {method_name} failed: {e}")
                continue
        
        logging.warning("All audio notification methods failed")

    def _try_system_bell(self) -> bool:
        """
        Tries to play system bell sound.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        # Skip system bell in VSCode as it's suppressed
        if self._is_vscode_terminal:
            return False
            
        try:
            print('\a', end='', flush=True)
            return True
        except Exception:
            return False

    def _try_platform_audio(self) -> bool:
        """
        Tries platform-specific audio commands.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        system = platform.system().lower()
        
        if system == 'darwin':  # macOS
            return self._try_macos_audio()
        elif system == 'linux':
            return self._try_linux_audio()
        elif system == 'windows':
            return self._try_windows_audio()
        
        return False

    def _try_macos_audio(self) -> bool:
        """
        Tries macOS-specific audio using afplay.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        sound_files = [
            '/System/Library/Sounds/Ping.aiff',
            '/System/Library/Sounds/Glass.aiff',
            '/System/Library/Sounds/Pop.aiff'
        ]
        
        for sound_file in sound_files:
            if os.path.exists(sound_file):
                try:
                    result = subprocess.run(
                        ['afplay', sound_file],
                        capture_output=True,
                        timeout=5,
                        check=False
                    )
                    if result.returncode == 0:
                        return True
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    continue
        
        return False

    def _try_linux_audio(self) -> bool:
        """
        Tries Linux-specific audio using paplay or aplay.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        # Try paplay first (PulseAudio)
        try:
            result = subprocess.run(
                ['paplay', '/usr/share/sounds/alsa/Front_Left.wav'],
                capture_output=True,
                timeout=2,
                check=False
            )
            if result.returncode == 0:
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Try aplay (ALSA)
        try:
            result = subprocess.run(
                ['aplay', '/usr/share/sounds/alsa/Front_Left.wav'],
                capture_output=True,
                timeout=2,
                check=False
            )
            if result.returncode == 0:
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Try speaker-test as fallback
        try:
            result = subprocess.run(
                ['speaker-test', '-t', 'sine', '-f', '1000', '-l', '1'],
                capture_output=True,
                timeout=2,
                check=False
            )
            if result.returncode == 0:
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        return False

    def _try_windows_audio(self) -> bool:
        """
        Tries Windows-specific audio using winsound.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import winsound
            winsound.Beep(1000, 500)  # 1000 Hz for 500ms
            return True
        except (ImportError, RuntimeError):
            pass
        
        # Fallback to system sounds
        try:
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            return True
        except (ImportError, RuntimeError):
            pass
        
        return False

    def _show_visual_notification(self) -> bool:
        """
        Shows a visual notification as last resort.
        
        Returns:
            bool: Always True as this is the final fallback.
        """
        print("\n" + "=" * 50)
        print("🔔 SESSION READY! 🔔")
        print("=" * 50)
        return True
