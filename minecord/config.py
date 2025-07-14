import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


DEFAULT_ADMINS_YAML = os.path.join(os.getcwd(), "admins.yaml")


class Config:
    """
    Configuration manager for Minecord that loads settings from YAML files.

    Supports multiple default locations:
    - $PWD/minecord.yaml
    - $HOME/.config/minecord.yaml
    - /etc/minecord.yaml

    Can be overridden with --config=PATH command line argument.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Optional path to config file. If None, will search default locations.
        """
        self.config_path = config_path
        self.config_data = self._load_config()

    def _get_default_config_paths(self) -> list[Path]:
        """Get list of default config file paths in order of preference."""
        paths = []

        # 1. Current working directory
        paths.append(Path.cwd() / "minecord.yaml")

        # 2. User's home directory
        home_config = Path.home() / ".config" / "minecord.yaml"
        paths.append(home_config)

        # 3. System-wide configuration
        paths.append(Path("/etc/minecord.yaml"))

        return paths

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = None

        if self.config_path:
            # Use explicitly provided path
            config_path = Path(self.config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
        else:
            # Search default locations
            for path in self._get_default_config_paths():
                if path.exists():
                    config_path = path
                    break
            else:
                raise FileNotFoundError(
                    f"No configuration file found. Searched in:\n"
                    + "\n".join(f"  - {p}" for p in self._get_default_config_paths())
                )

        print(f"Loading configuration from: {config_path}")

        try:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
                if not isinstance(config_data, dict):
                    raise ValueError("Configuration file must contain a YAML object")
                return config_data
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config_data.get(key, default)

    def get_required(self, key: str) -> Any:
        """Get a required configuration value, raising an error if not found."""
        value = self.config_data.get(key)
        if value is None:
            raise ValueError(f"Required configuration key '{key}' not found")
        return value

    @property
    def admins_yaml(self) -> str:
        """Get the admins YAML file path."""
        return self.get("admins_yaml") or DEFAULT_ADMINS_YAML

    @property
    def discord_token(self) -> str:
        """Get the Discord bot token."""
        return self.get_required("discord_token")

    @property
    def guild_id(self) -> Optional[int]:
        """Get the Discord server ID, if configured."""
        guild_id = self.get("discord_guild_id")
        if guild_id is not None:
            try:
                return int(guild_id)
            except (ValueError, TypeError):
                print(
                    f"Warning: minecord_channel_id ('{guild_id}') is not a valid integer. Ignoring."
                )
                return None
        return None

    @property
    def minecord_channel_id(self) -> Optional[int]:
        """Get the startup channel ID, if configured."""
        channel_id = self.get("minecord_channel_id")
        if channel_id is not None:
            try:
                return int(channel_id)
            except (ValueError, TypeError):
                print(
                    f"Warning: minecord_channel_id ('{channel_id}') is not a valid integer. Ignoring."
                )
                return None
        return None

    @property
    def rcon_host(self) -> str:
        """Get the RCON host."""
        return self.get("rcon_host", "localhost")

    @property
    def rcon_port(self) -> int:
        """Get the RCON port."""
        port = self.get("rcon_port", 25575)
        try:
            return int(port)
        except (ValueError, TypeError):
            print(
                f"Warning: rcon_port ('{port}') is not a valid integer. Using default 25575."
            )
            return 25575

    @property
    def rcon_password(self) -> Optional[str]:
        """Get the RCON password."""
        return self.get("rcon_password")


def create_example_config() -> str:
    """Create an example YAML configuration."""
    return """# Minecord Configuration File
# This file contains all configuration for the Minecord Discord bot

# Authorization / User mapping
admins_yaml: "/path/to/admins.yaml"

# Discord Bot Configuration
discord_token: "your_bot_token_here"
minecord_channel_id: 123456789012345678  # Optional: Channel ID for startup message

# Minecraft RCON Configuration
rcon_host: "localhost"      # Minecraft server hostname
rcon_port: 25575           # RCON port (default: 25575)
rcon_password: "your_rcon_password_here"  # RCON password
"""
