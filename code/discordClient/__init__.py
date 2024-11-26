import discord
from discord import app_commands

from .commands import (
    ping,
    link,
    history,
    add,
    weekly,
    monthly,
    predict,
    sendEmail,
    delete,
    insight,
    budget,
    pdf,
    analytics,
)


class DiscordClient(discord.Client):
    """A custom Discord client for handling bot functionality.

    This client extends discord.Client to provide command handling and setup capabilities
    for a Discord bot. It includes command tree initialization and management.
    """

    def __init__(self, guild_id: int = 0, bot_token: str = ""):
        """Initialize the Discord client with specified guild and token.

        Args:
            guild_id (int): The ID of the server to operate in.
            bot_token (str): The bot's authentication token.
        """
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self._guild_id = discord.Object(guild_id)
        self._bot_token = bot_token
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        """Set up the bot's command tree and sync commands.

        This method is called automatically when the bot starts up. It loads all commands
        and syncs them with the specified guild.
        """
        await self.load_commands()
        self.tree.copy_global_to(guild=self._guild_id)
        await self.tree.sync(guild=self._guild_id)

    async def load_commands(self):
        """Load all command modules into the command tree."""
        await ping.setup(self.tree)
        await link.setup(self.tree)
        await history.setup(self.tree)
        await add.setup(self.tree)
        await weekly.setup(self.tree)
        await predict.setup(self.tree)
        await monthly.setup(self.tree)
        await analytics.setup(self.tree)
        await pdf.setup(self.tree)
        await budget.setup(self.tree)
        await sendEmail.setup(self.tree)
        await delete.setup(self.tree)
        await insight.setup(self.tree)

    async def on_ready(self):
        """Event handler that executes when the bot is ready.

        Prints a confirmation message with the bot's username when successfully logged in.
        """
        print(f"Logged in as {self.user}")

    def start_bot(self):
        """Start the Discord bot.

        Initiates the bot's operation using the provided bot token.
        """
        self.run(self._bot_token)
