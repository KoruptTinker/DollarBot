from discord import app_commands
import discord
import helper


async def link(interaction: discord.Interaction, code: str):
    """Link a Discord account to an existing Telegram account using a verification code.

    This command allows users to connect their Discord account with their Telegram account
    using a 6-digit verification code generated from the Telegram bot.
    
    The function:
        1. Validates the format of the provided code (must be 6 digits)
        2. Checks if the code exists in the pending link requests
        3. If valid, links the Discord user ID to the corresponding Telegram chat ID
        4. Deletes the used verification code
        5. Confirms successful linking or returns an error message
    """
    if not code.isdigit() or len(code) != 6:
        await interaction.response.send_message(
            "Please provide a valid 6-digit code.", ephemeral=True
        )
        return

    existing_code = helper.fetchLinkCode(code)
    if existing_code is not None:
        helper.linkDiscordToTelegram(existing_code["chat_id"], interaction.user.id)
        helper.deleteLinkCode(existing_code["link_code"])

        await interaction.response.send_message(
            "Successfully linked your discord account to your telegram account!"
        )
    else:
        await interaction.response.send_message(
            "Code you've entered is invalid! Please get a new code from the Telegram app!"
        )


async def setup(tree: app_commands.CommandTree):
    tree.command(name="link", description="Link your Discord account with Telegram")(
        link
    )
