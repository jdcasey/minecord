import os
import discord
from discord import Client, TextChannel
from discord.app_commands import CommandTree
from discord import Interaction, Intents, Forbidden, HTTPException
import argparse
from .config import Config, create_example_config


class MinecordBot(Client):

    def __init__(self, startup_channel_id: int, guild_id: int):
        super().__init__(command_prefix="/", intents=Intents.all())
        self.startup_channel_id = startup_channel_id
        self.guild_id = guild_id
        self.tree = CommandTree(self)

    async def on_ready(self):
        """Called when the bot is connected and ready."""
        print("Syncing commands...")

        # Sync slash commands with Discord
        try:
            # During development, sync to your test server for instant updates
            if self.guild_id is not None:
                print(f"Syncing commands to server: {self.guild_id}")
                synced = await self.tree.sync(guild=discord.Object(id=self.guild_id))

            # For production, sync globally (this can take up to an hour)
            else:
                print(f"Syncing commands globally")
                synced = await self.tree.sync()

            print(f"Synced {len(synced)} command(s):\n\n{synced}")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

        if self.startup_channel_id:
            try:
                channel = self.get_channel(self.startup_channel_id)
                if channel and isinstance(channel, TextChannel):
                    await channel.send("Hello! The Minecord bot is now online.")
                else:
                    print(
                        f"Warning: Could not find channel with ID {self.startup_channel_id}."
                    )
            except (ValueError, Forbidden, HTTPException) as e:
                print(
                    f"Error sending startup message to channel {self.startup_channel_id}: {e}"
                )


def run_bot():
    parser = argparse.ArgumentParser(
        description="Runs the Minecord Discord bot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\
    Configuration is loaded from YAML files.
    The bot will search for configuration in the following order:
    1. $PWD/minecord.yaml
    2. $HOME/.config/minecord.yaml
    3. /etc/minecord.yaml

    You can override the config location with --config=PATH.
    Use --print-sample-config to see an example configuration file.
    """,
    )
    parser.add_argument(
        "--config", type=str, help="Path to configuration file (YAML format)"
    )
    parser.add_argument(
        "--print-sample-config",
        action="store_true",
        help="Print a sample configuration file and exit"
    )
    args = parser.parse_args()

    # Handle --print-sample-config option
    if args.print_sample_config:
        print(create_example_config())
        exit(0)

    try:
        # Load configuration from YAML file
        config = Config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}")
        print("\nTo create an example configuration file, run:")
        print("  python -m minecord.bot --help")
        exit(1)

    bot = MinecordBot(
        startup_channel_id=config.minecord_channel_id,
        guild_id=config.guild_id
    )

    @bot.tree.command()
    async def echo(interaction: Interaction):
        await interaction.response.send_message(interaction.message)

    bot.run(config.discord_token)

