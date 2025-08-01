import os
import discord
from discord.ext.commands import Bot
from discord import TextChannel, app_commands
from discord import Interaction, Intents, Forbidden, HTTPException
import argparse
# Assuming your config file logic is in a file named config.py in the same directory
# If not, you may need to adjust the import path (e.g., from config import ...)
from .config import Config, create_example_config
from .cogs.minecraft import MinecraftCog
from .cogs.admin import AdminCog
from .admins import Admins


class MinecordBot(Bot):
    """
    A refactored version of the bot that handles command registration
    and syncing within the class using modern discord.py practices.
    """
    def __init__(self, config: Config):
        # Intents.all() is powerful; for a production bot, you might want to
        # specify only the intents you truly need.
        super().__init__(command_prefix="/", intents=Intents.all())
        self.startup_channel_id=config.minecord_channel_id
        self.guild_id=config.guild_id
        self.config = config
        self.admins = Admins(config.admins_yaml)
    

    async def setup_hook(self) -> None:
        """
        This special method is called once when the bot is setting up.
        It's the perfect place to load extensions and sync commands.
        """
        print("Running setup_hook...")

        print("Loading extensions...")
        await self.add_cog(MinecraftCog(self))
        await self.add_cog(AdminCog(self))
        print("Extensions loaded.")

        # 2. Sync the commands that were loaded from the cog.
        print("Syncing commands...")
        if self.guild_id:
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {self.guild_id}.")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s) globally.")


    async def on_ready(self):
        """Called when the bot is connected and ready."""
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

        # Send a startup message if a channel is configured.
        if self.startup_channel_id:
            try:
                channel = self.get_channel(self.startup_channel_id)
                if channel and isinstance(channel, TextChannel):
                    await channel.send("Hello! The Minecord bot is now online.")
                else:
                    print(f"Warning: Could not find channel with ID {self.startup_channel_id}.")
            except (ValueError, Forbidden, HTTPException) as e:
                print(f"Error sending startup message to channel {self.startup_channel_id}: {e}")

# --- Command Definition ---
# By defining the command outside the class but attaching it to an instance,
# we need to make sure the instance is created first. The refactor below is cleaner.
# The best practice is to define commands within Cogs or directly on the bot instance
# before running it. Let's create the bot instance first, then define the command.

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
    parser.add_argument("--config", type=str, help="Path to configuration file (YAML format)")
    parser.add_argument("--print-sample-config", action="store_true", help="Print a sample configuration file and exit")
    args = parser.parse_args()

    if args.print_sample_config:
        print(create_example_config())
        exit(0)

    try:
        config = Config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}")
        print("\nTo create an example configuration file, run:")
        print("  python -m minecord.bot --help")
        exit(1)

    # Create the bot instance
    bot = MinecordBot(config)

    # Run the bot with the token from your config
    bot.run(config.discord_token)

# This allows the script to be run directly
if __name__ == '__main__':
    run_bot()
