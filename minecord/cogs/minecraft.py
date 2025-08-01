import discord
from discord import app_commands, Interaction
from discord.ext import commands
from minecord.backend.rcon import MinecraftRCONClient
from minecord.config import Config

class MinecraftCog(commands.Cog):
    """A cog for holding the bot's commands."""

    def __init__(self, bot):
        """
        Initializes the cog.

        Args:
            bot: The bot instance.
        """
        self.bot = bot
        self.minecraft = MinecraftRCONClient(bot.config.rcon_host, bot.config.rcon_port, bot.config.rcon_password)
        self.admins = bot.admins

    @app_commands.command(name="online", description="List online players.")
    async def online(self, interaction: Interaction):
        """
        Lists the players currently online on the Minecraft server.
        Handles connection errors gracefully.
        """
        try:
            online_players = self.minecraft.list_players()

            if not online_players:
                message = "No players are currently online."
            else:
                player_list = ", ".join(online_players)
                message = f"**Online players ({len(online_players)}):** {player_list}"

            await interaction.response.send_message(message, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                "Error: Could not connect to the Minecraft server. "
                "Please check if the server is running and if RCON is enabled and configured correctly.",
                ephemeral=True,
            )

    @app_commands.command(name="fingerprint", description="Retrieve the server automodpack fingerprint.")
    async def fingerprint(self, interaction: Interaction):
        """
        Retrieves the automodpack fingerprint for the Minecraft server.
        Handles connection errors gracefully.
        """
        try:
            fingerprint = self.minecraft.get_fingerprint()

            message = f"**Automodpack fingerprint:** ```{fingerprint}```"
            await interaction.response.send_message(message, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                "Error: Could not connect to the Minecraft server. "
                "Please check if the server is running and if RCON is enabled and configured correctly.",
                ephemeral=True,
            )

    @app_commands.command(name="allow", description="Add a Minecraft user to the server allowlist.")
    async def allow(self, interaction: Interaction, username: str):
        """
        Adds the specified Minecraft user to the server allowlist.
        Requires administrator authorization.
        """
        try:
            if await self.admins.check_authorization(interaction, "allow"):
                response = self.minecraft.whitelist_add(username)
                
                # Check if the response indicates success or failure
                if "Failed to add" in response:
                    await interaction.response.send_message(
                        f"❌ Error: {response}",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"✅ **{username}** is now allowed to join the server.\n```{response}```",
                        ephemeral=True,
                    )
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while adding the user to the server allowlist.",
                ephemeral=True,
            )

    @app_commands.command(name="list-allowed", description="Show users allowed to join the server.")
    async def list_allowed(self, interaction: Interaction):
        """
        Shows the users currently allowed to join the server.
        Requires administrator authorization.
        """
        try:
            if await self.admins.check_authorization(interaction, "list_allowed"):
                response = self.minecraft.whitelist_list()
                
                # Check if the response indicates success or failure
                if "Failed to retrieve" in response:
                    await interaction.response.send_message(
                        f"❌ Error: {response}",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"**These users are allowed to join the server:**\n```{response}```",
                        ephemeral=True,
                    )
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while retrieving the server allowlist.",
                ephemeral=True,
            )

async def setup(bot: commands.Bot) -> None:
    """
    This special function is called by discord.py when the extension is loaded.
    It is used to add the cog to the bot.
    """
    await bot.add_cog(MinecraftCog(bot))
