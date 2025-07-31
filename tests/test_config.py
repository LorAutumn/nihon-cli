import unittest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from nihon_cli.core.config import Config, DEFAULT_CONFIG_FILE

class TestConfig(unittest.TestCase):
    """Tests for the Config class."""

    def setUp(self):
        """Set up a temporary config path for each test."""
        self.mock_config_path = Path("/tmp/test_config.json")

    @patch("pathlib.Path.exists", return_value=False)
    def test_initialization_with_no_file(self, mock_exists):
        """Test that Config initializes with defaults when no file exists."""
        config = Config(config_path=self.mock_config_path)
        
        self.assertEqual(config.enable_sound, True)
        self.assertEqual(config.notification_type, "bell")
        mock_exists.assert_called_once()

    def test_default_values(self):
        """Test that default values are correct."""
        config = Config(config_path=self.mock_config_path)
        defaults = config._load_defaults()
        
        self.assertEqual(defaults["enable_sound"], True)
        self.assertEqual(defaults["notification_type"], "bell")

    @patch("pathlib.Path.exists", return_value=True)
    def test_load_valid_config(self, mock_exists):
        """Test loading a valid configuration file."""
        user_settings = {
            "enable_sound": False,
            "notification_type": "desktop"
        }
        mock_file_content = json.dumps(user_settings)
        
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            config = Config(config_path=self.mock_config_path)
            
            self.assertEqual(config.enable_sound, False)
            self.assertEqual(config.notification_type, "desktop")
            mock_file.assert_called_once_with(self.mock_config_path, "r")

    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corrupted_config(self, mock_exists):
        """Test that loading a corrupted JSON file falls back to defaults."""
        mock_file_content = "this is not json"
        
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            config = Config(config_path=self.mock_config_path)
            
            # Should revert to defaults
            self.assertEqual(config.enable_sound, True)
            self.assertEqual(config.notification_type, "bell")

    @patch("pathlib.Path.exists", return_value=True)
    def test_load_io_error(self, mock_exists):
        """Test that an IOError during load falls back to defaults."""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            config = Config(config_path=self.mock_config_path)
            
            # Should revert to defaults
            self.assertEqual(config.enable_sound, True)
            self.assertEqual(config.notification_type, "bell")

    @patch("pathlib.Path.mkdir")
    def test_save_config(self, mock_mkdir):
        """Test saving the configuration to a file."""
        config = Config(config_path=self.mock_config_path)
        config.enable_sound = False
        config.notification_type = "sound"
        
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            config.save()
            
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            mock_file.assert_called_once_with(self.mock_config_path, "w")
            
            handle = mock_file()
            # When using json.dump with indent, `write` is called multiple times.
            # We need to join the content from all calls.
            written_content = "".join(call.args[0] for call in handle.write.call_args_list)
            saved_data = json.loads(written_content)
            
            self.assertEqual(saved_data["enable_sound"], False)
            self.assertEqual(saved_data["notification_type"], "sound")

    def test_property_setters(self):
        """Test that property setters update the internal config dictionary."""
        config = Config(config_path=self.mock_config_path)
        
        config.enable_sound = False
        self.assertEqual(config._config["enable_sound"], False)
        
        config.notification_type = "desktop"
        self.assertEqual(config._config["notification_type"], "desktop")

if __name__ == "__main__":
    unittest.main()