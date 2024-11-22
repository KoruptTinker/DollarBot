import discord
from discord import app_commands


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

        @self.tree.command(name="dm", description="Sends a DM")
        async def dm(interaction: discord.Interaction):
            await interaction.user.send("Hello")
            await interaction.response.send_message("Sent you a DM!")

        @self.tree.command(name="sync", description="Syncs commands")
        async def sync(interaction: discord.Interaction):
            await self.tree.sync()

    async def setup_hook(self):
        await self.tree.sync(guild=self._guild_id)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    def start_bot(self):
        self.run(self._bot_token)
