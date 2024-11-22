import discord
from discord import app_commands
import helper


class DiscordClient(discord.Client):
    _guild_id: discord.Object = None
    _bot_token: str = None

    def __init__(self, guild_id: int = 0, bot_token: str = ""):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self._guild_id = discord.Object(guild_id)
        self._bot_token = bot_token
        self.tree = app_commands.CommandTree(self)

        @self.tree.command(name="ping", description="Sends a pong response")
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message("Pong!")

        @self.tree.command(name="link", description="Link your Discord account with Telegram")
        async def link(interaction: discord.Interaction, code: str):
            if not code.isdigit() or len(code) != 6:
                await interaction.response.send_message(
                    "Please provide a valid 6-digit code.", 
                    ephemeral=True
                )
                return

            existing_code = helper.fetchLinkCode(code)
            if existing_code != None:
                helper.linkDiscordToTelegram(existing_code["chat_id"], interaction.user.id)
                helper.deleteLinkCode(existing_code["link_code"])

                await interaction.response.send_message(
                    "Successfully linked your discord account to your telegram account!", 
                )
            else:
                await interaction.response.send_message(
                    "Code you've entered is invalid! Please get a new code from the Telegram app!", 
                )
                
    async def setup_hook(self):
        self.tree.copy_global_to(guild=self._guild_id)
        await self.tree.sync(guild=self._guild_id)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    def start_bot(self):
        self.run(self._bot_token)
