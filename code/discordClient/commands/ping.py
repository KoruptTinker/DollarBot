from discord import app_commands
import discord


async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


async def setup(tree: app_commands.CommandTree):
    tree.command(name="ping", description="Sends a pong response")(ping)
