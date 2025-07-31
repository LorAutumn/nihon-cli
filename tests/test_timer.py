import subprocess
import unittest
from unittest.mock import patch, MagicMock, call

from nihon_cli.core.timer import LearningTimer

class TestLearningTimer(unittest.TestCase):
    """Tests for the LearningTimer class."""

    def test_initialization_default(self):
        """Test timer initializes with default values."""
        timer = LearningTimer()
        self.assertEqual(timer.interval_seconds, 1500)
        self.assertTrue(timer.enable_sound)
        self.assertEqual(timer.notification_type, "bell")
        self.assertFalse(timer.is_test_mode())

    def test_initialization_custom(self):
        """Test timer initializes with custom values."""
        timer = LearningTimer(
            interval_seconds=300,
            enable_sound=False,
            notification_type="desktop",
        )
        self.assertEqual(timer.interval_seconds, 300)
        self.assertFalse(timer.enable_sound)
        self.assertEqual(timer.notification_type, "desktop")

    def test_test_mode(self):
        """Test is_test_mode() returns True for 5-second interval."""
        timer = LearningTimer(interval_seconds=5)
        self.assertTrue(timer.is_test_mode())

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd"))
    @patch("builtins.print")
    def test_play_notification_bell_fallback(self, mock_print, mock_run):
        """Test that 'bell' notification falls back to printing the bell character."""
        timer = LearningTimer(notification_type="bell")
        timer.play_notification_sound()
        mock_print.assert_called_with("\a", end="", flush=True)

    @patch("nihon_cli.core.timer.LearningTimer._send_desktop_notification")
    def test_play_notification_desktop(self, mock_send_desktop):
        """Test that 'desktop' notification calls the correct method."""
        timer = LearningTimer(notification_type="desktop")
        timer.play_notification_sound()
        mock_send_desktop.assert_called_once()

    @patch("platform.system", return_value="Darwin")
    @patch("subprocess.run")
    def test_desktop_notification_macos(self, mock_run, mock_system):
        """Test desktop notification command on macOS."""
        timer = LearningTimer(notification_type="desktop")
        timer._send_desktop_notification()
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        self.assertIn("osascript", args[0])
        self.assertIn("display notification", args[0][2])

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_desktop_notification_linux(self, mock_run, mock_system):
        """Test desktop notification command on Linux."""
        timer = LearningTimer(notification_type="desktop")
        timer._send_desktop_notification()
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        self.assertIn("notify-send", args[0])

    @patch("platform.system", return_value="Windows")
    @patch("subprocess.run")
    def test_desktop_notification_windows(self, mock_run, mock_system):
        """Test desktop notification command on Windows."""
        timer = LearningTimer(notification_type="desktop")
        timer._send_desktop_notification()
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        self.assertIn("powershell", args[0])

    @patch("time.sleep")
    @patch("nihon_cli.core.timer.LearningTimer.play_notification_sound")
    @patch("nihon_cli.core.timer.LearningTimer.show_countdown")
    def test_wait_for_next_session_flow(
        self, mock_countdown, mock_sound, mock_sleep
    ):
        """Test the main flow of wait_for_next_session."""
        timer = LearningTimer(interval_seconds=3, enable_sound=True)
        timer.wait_for_next_session()

        self.assertEqual(mock_countdown.call_count, 3)
        mock_countdown.assert_has_calls([call(3), call(2), call(1)])
        mock_sleep.assert_has_calls([call(1), call(1), call(1)])
        mock_sound.assert_called_once()

    @patch("time.sleep")
    @patch("nihon_cli.core.timer.LearningTimer.play_notification_sound")
    def test_wait_for_next_session_disabled_features(
        self, mock_sound, mock_sleep
    ):
        """Test wait_for_next_session with sound disabled."""
        timer = LearningTimer(interval_seconds=1, enable_sound=False)
        timer.wait_for_next_session()

        mock_sound.assert_not_called()

if __name__ == "__main__":
    unittest.main()