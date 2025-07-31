import json
from pathlib import Path
from typing import Any, Dict, Literal

DEFAULT_CONFIG_DIR = Path.home() / ".nihon-cli"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"

NotificationType = Literal["bell", "sound", "desktop"]

class Config:
    """
    Manages user configuration settings for the application.

    This class handles loading, saving, and providing access to configuration
    options stored in a JSON file. It ensures that a default configuration
    is always available.
    """

    def __init__(self, config_path: Path = DEFAULT_CONFIG_FILE):
        """
        Initializes the Config object.

        Args:
            config_path (Path, optional): The path to the configuration file.
                Defaults to DEFAULT_CONFIG_FILE.
        """
        self.config_path = config_path
        self._config = self._load_defaults()
        self.load()

    def _load_defaults(self) -> Dict[str, Any]:
        """
        Returns the default configuration values.

        Returns:
            Dict[str, Any]: A dictionary with default settings.
        """
        return {
            "enable_sound": True,
            "notification_type": "bell",
        }

    def load(self) -> None:
        """
        Loads the configuration from the JSON file.

        If the file doesn't exist or is invalid, the configuration
        reverts to the default settings.
        """
        if not self.config_path.exists():
            # If no config file exists, we just use the defaults.
            # The file will be created on the first save.
            return

        try:
            with open(self.config_path, "r") as f:
                user_config = json.load(f)
            self._config.update(user_config)
        except (json.JSONDecodeError, IOError):
            # If the file is corrupted or unreadable, fall back to defaults.
            # The next save will fix the file.
            self._config = self._load_defaults()

    def save(self) -> None:
        """
        Saves the current configuration to the JSON file.

        This method will create the configuration directory if it
        does not exist.
        """
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self._config, f, indent=4)
        except IOError:
            # Handle cases where the file cannot be written.
            # For a CLI tool, we might print an error to stderr.
            # For now, we'll fail silently.
            pass

    @property
    def enable_sound(self) -> bool:
        """Whether to play a sound on correct/incorrect answers."""
        return self._config.get("enable_sound", True)

    @enable_sound.setter
    def enable_sound(self, value: bool) -> None:
        self._config["enable_sound"] = value

    @property
    def notification_type(self) -> NotificationType:
        """The type of notification to use."""
        return self._config.get("notification_type", "bell")

    @notification_type.setter
    def notification_type(self, value: NotificationType) -> None:
        self._config["notification_type"] = value
