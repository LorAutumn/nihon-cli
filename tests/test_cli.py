import unittest
from unittest.mock import patch, MagicMock

from nihon_cli.cli.commands import parse_and_execute
from nihon_cli.core.config import Config

class TestCliCommands(unittest.TestCase):
    """Tests for the CLI command integration."""

    @patch("nihon_cli.cli.commands.NihonCli")
    @patch("nihon_cli.cli.commands.Config")
    def test_hiragana_command_default(self, MockConfig, MockNihonCli):
        """Test that the hiragana command uses default config values."""
        mock_config_instance = MagicMock()
        MockConfig.return_value = mock_config_instance
        
        mock_app_instance = MagicMock()
        MockNihonCli.return_value = mock_app_instance

        parse_and_execute(["cli", "hiragana"])

        # Verify that config is not modified by default
        self.assertNotEqual(mock_config_instance.enable_sound, False)

        MockNihonCli.assert_called_once_with(mock_config_instance)
        mock_app_instance.run_training_session.assert_called_once_with("hiragana", False)

    @patch("nihon_cli.cli.commands.NihonCli")
    @patch("nihon_cli.cli.commands.Config")
    def test_hiragana_command_with_flags(self, MockConfig, MockNihonCli):
        """Test that CLI flags override the config for the hiragana command."""
        mock_config_instance = MagicMock()
        MockConfig.return_value = mock_config_instance
        
        mock_app_instance = MagicMock()
        MockNihonCli.return_value = mock_app_instance

        args = [
            "cli",
            "hiragana",
            "--test",
            "--no-sound",
            "--notification-type",
            "desktop",
        ]
        parse_and_execute(args)

        # Verify that config is modified by flags
        self.assertEqual(mock_config_instance.enable_sound, False)
        self.assertEqual(mock_config_instance.notification_type, "desktop")

        MockNihonCli.assert_called_once_with(mock_config_instance)
        mock_app_instance.run_training_session.assert_called_once_with("hiragana", True)

    @patch("nihon_cli.app.LearningTimer")
    @patch("nihon_cli.app.NihonCli._handle_session_loop")
    def test_app_setup_components_with_config(self, mock_loop, MockLearningTimer):
        """Test that NihonCli correctly initializes LearningTimer based on config."""
        from nihon_cli.app import NihonCli

        # Create a config object with specific settings
        config = Config()
        config.enable_sound = False
        config.notification_type = "desktop"

        app = NihonCli(config)
        app.run_training_session("katakana", test_mode=True)

        # Check that LearningTimer was initialized with values from the config
        MockLearningTimer.assert_called_once_with(
            5,  # 5 seconds for test mode
            enable_sound=False,
            notification_type="desktop",
        )
        # Ensure the main loop was not called
        mock_loop.assert_called_once()

if __name__ == "__main__":
    unittest.main()