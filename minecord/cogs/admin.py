import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from minecord.backend.rcon import MinecraftRCONClient
from minecord.config import Config
import traceback

MAKE_ADMIN_COMMAND = 'make-admin'

class AdminCog(commands.Cog):
    """A cog for holding the bot's commands."""

    def __init__(self, bot: commands.Bot):
        """
        Initializes the cog.

        Args:
            bot: The bot instance.
        """
        self.bot = bot
        self.admins = bot.admins

    async def _check_authorization(self, interaction: Interaction, command: str) -> bool:
        print(f"Checking for authorization: {interaction.user.display_name} ({interaction.user.id})")
            
        if self.admins.is_admin(interaction.user.id):
            return True
    
        print(f"DENIED: {command} was denied to user: {interaction.user.display_name} ({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to access this command. Your attempt has been logged.", ephemeral=True)
        return False


    @app_commands.command(name=MAKE_ADMIN_COMMAND, description="Add user to admins list.")
    async def make_admin(self, interaction: Interaction, user_mention: str):
        """
        Adds the specified user to the admins list.
        """
        try:
            print(f"Looking up user: {user_mention}")
            user = await self.bot.fetch_user(int(user_mention[2:-1]))
            print(f"Got: {user}")
            if await self._check_authorization(interaction, MAKE_ADMIN_COMMAND):
                if not self.admins.can_add_admin(interaction.user.id):
                    print(f"DENIED: {MAKE_ADMIN_COMMAND} was denied to user: {interaction.user.display_name} ({interaction.user.id})")
                    await interaction.response.send_message("You are not authorized to make new admins. Your attempt has been logged.", ephemeral=True)
                else:
                    self.admins.add_admin(user.id, user.display_name)
                    await interaction.response.send_message(f"{user.display_name} is now an admin on Discord (not a Minecraft op)! 🎉", ephemeral=True)

        except Exception as e:
            traceback.format_exc()
            await interaction.response.send_message(
                "An error occurred in this bot's admins module.",
                ephemeral=True,
            )

    @app_commands.command(name="am-i-admin", description="Check whether you're an admin.")
    async def am_i_admin(self, interaction: Interaction):
        try:
            print("checking")
            if await self._check_authorization(interaction, "am-i-admin"):
                await interaction.response.send_message("You **are** an admin (here on Discord)! 🎉", ephemeral=True)
            print("returned")
        except Exception as e:
            traceback.format_exc()
            await interaction.response.send_message(
                "An error occurred in this bot's admins module.",
                ephemeral=True,
            )

async def setup(bot: commands.Bot) -> None:
    """
    This special function is called by discord.py when the extension is loaded.
    It is used to add the cog to the bot.
    """
    await bot.add_cog(AdminCog(bot))
