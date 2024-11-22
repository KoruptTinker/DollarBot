from discord import app_commands
import discord
import helper


async def link(interaction: discord.Interaction, code: str):
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
