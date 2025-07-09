# Minecord Configuration

Minecord now uses YAML configuration files instead of environment variables. This provides better structure and type safety for configuration.

## Configuration File Locations

The bot will search for configuration files in the following order:

1. `$PWD/minecord.yaml` (current working directory)
2. `$HOME/.config/minecord.yaml` (user's home directory)
3. `/etc/minecord.yaml` (system-wide configuration)

You can also specify a custom location using the `--config=PATH` command line argument.

## Configuration Format

Create a YAML file with the following structure:

```yaml
# Discord Bot Configuration
discord_token: "your_bot_token_here"
minecord_channel_id: 123456789012345678  # Optional: Channel ID for startup message

# Minecraft RCON Configuration
rcon_host: "localhost"      # Minecraft server hostname
rcon_port: 25575           # RCON port (default: 25575)
rcon_password: "your_rcon_password_here"  # RCON password
```

## Required Configuration

- `discord_token`: Your Discord bot token from the Discord Developer Portal
- `rcon_password`: The RCON password for your Minecraft server

## Optional Configuration

- `minecord_channel_id`: Channel ID where the bot will send startup messages
- `rcon_host`: Minecraft server hostname (default: localhost)
- `rcon_port`: RCON port (default: 25575)

## Example Usage

1. Copy the example configuration:
   ```bash
   cp minecord.yaml.example minecord.yaml
   ```

2. Edit the configuration file with your values:
   ```bash
   nano minecord.yaml
   ```

3. Run the bot:
   ```bash
   python -m minecord.bot
   ```

## Command Line Options

- `--config=PATH`: Specify a custom configuration file path
- `--help`: Show help information

## Migration from Environment Variables

If you were previously using environment variables, here's how to migrate:

| Environment Variable | YAML Key |
|---------------------|----------|
| `DISCORD_TOKEN` | `discord_token` |
| `MINECORD_CHANNEL_ID` | `minecord_channel_id` |
| `RCON_HOST` | `rcon_host` |
| `RCON_PORT` | `rcon_port` |
| `RCON_PASSWORD` | `rcon_password` | 