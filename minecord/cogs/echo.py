import discord
from discord import app_commands, Interaction
from discord.ext import commands

class EchoCog(commands.Cog):
    """A cog for holding the bot's commands."""

    def __init__(self, bot: commands.Bot):
        """
        Initializes the cog.

        Args:
            bot: The bot instance.
        """
        self.bot = bot

    @app_commands.command(name="echo", description="Repeats a message you provide.")
    @app_commands.describe(message="The message to echo back")
    async def echo(self, interaction: Interaction, message: str):
        """
        A proper slash command. Note: `interaction.message` does not exist
        for slash commands; arguments are passed directly.
        """
        # You can make the response "ephemeral" so only the user who ran it can see it.
        await interaction.response.send_message(f"You said: {message}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    """
    This special function is called by discord.py when the extension is loaded.
    It is used to add the cog to the bot.
    """
    await bot.add_cog(EchoCog(bot))
