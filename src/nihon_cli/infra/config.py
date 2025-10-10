"""Configuration management for nihon-cli.

This module handles loading and saving configuration values to a TOML file
stored in the user's home directory at ~/.nihon-cli/config.toml.
"""

import tomli
import tomli_w
from pathlib import Path
from typing import Optional


def _get_config_path() -> Path:
    """Get the path to the configuration file.
    
    Returns:
        Path: Path to ~/.nihon-cli/config.toml
    """
    config_dir = Path.home() / ".nihon-cli"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.toml"


def save_config(key: str, value: str) -> None:
    """Save a configuration key-value pair to the config file.
    
    Creates or updates the configuration file at ~/.nihon-cli/config.toml.
    If the file exists, it loads the existing configuration, updates the
    specified key, and writes it back.
    
    Args:
        key: The configuration key to save
        value: The configuration value to save
        
    Raises:
        OSError: If the configuration file cannot be written
    """
    config_path = _get_config_path()
    
    # Load existing config if it exists
    config = {}
    if config_path.exists():
        with open(config_path, "rb") as f:
            config = tomli.load(f)
    
    # Update the key
    config[key] = value
    
    # Write back to file
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)


def load_config(key: str) -> Optional[str]:
    """Load a configuration value from the config file.
    
    Reads the configuration file at ~/.nihon-cli/config.toml and returns
    the value for the specified key.
    
    Args:
        key: The configuration key to load
        
    Returns:
        The configuration value if found, None otherwise
        
    Raises:
        OSError: If the configuration file cannot be read (when it exists)
    """
    config_path = _get_config_path()
    
    # Return None if config file doesn't exist
    if not config_path.exists():
        return None
    
    # Load and return the value
    with open(config_path, "rb") as f:
        config = tomli.load(f)
        return config.get(key)