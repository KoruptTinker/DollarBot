import discord
from discord import app_commands
from .commands import ping, link, history, add, weekly, monthly, budget


class DiscordClient(discord.Client):
    def __init__(self, guild_id: int = 0, bot_token: str = ""):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self._guild_id = discord.Object(guild_id)
        self._bot_token = bot_token
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.load_commands()
        self.tree.copy_global_to(guild=self._guild_id)
        await self.tree.sync(guild=self._guild_id)

    async def load_commands(self):
        await ping.setup(self.tree)
        await link.setup(self.tree)
        await history.setup(self.tree)
        await add.setup(self.tree)
        await weekly.setup(self.tree)
        await monthly.setup(self.tree)
        await budget.setup(self.tree)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    def start_bot(self):
        self.run(self._bot_token)
