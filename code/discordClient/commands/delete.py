import discord
from discord import app_commands
from datetime import datetime
import helper


async def run(interaction: discord.Interaction, option: str, date: str = None):
    """
    Handles the `/delete` command.

    :param interaction: The Discord interaction object.
    :param option: The option for deletion ('all' or 'date').
    :param date: Optional date for date-specific deletion.
    """
    try:
        # Fetch user details based on Discord ID
        user_details = helper.fetchUserFromDiscord(interaction.user.id)

        # Check if the user's Discord account is linked
        if user_details is None:
            await interaction.response.send_message(
                "You don't have your Discord account linked to an active Telegram account. Use the /link command on Telegram to learn more.",
                ephemeral=True,
            )
            return

        # Get the Telegram chat ID
        telegram_chat_id = user_details["telegram_chat_id"]

        # Handle "all" option
        if option.lower() == "all":
            deleted_count = helper.erase_spend_history(telegram_chat_id)
            if deleted_count > 0:
                await interaction.response.send_message(
                    f"Deleted {deleted_count} records successfully.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "No records found to delete!", ephemeral=True
                )
            return

        # Handle "date" option
        if option.lower() == "date" and date:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                deleted_count = helper.delete_spend_history(
                    telegram_chat_id, formatted_date
                )
                if deleted_count > 0:
                    await interaction.response.send_message(
                        f"Deleted {deleted_count} records for {formatted_date}.",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"No records found for {formatted_date}.", ephemeral=True
                    )
            except ValueError:
                await interaction.response.send_message(
                    "Invalid date format. Please use YYYY-MM-DD.", ephemeral=True
                )
            return

        # Invalid option or missing date
        await interaction.response.send_message(
            "Invalid option or missing date. Use 'all' to delete all records or provide a valid 'date' in YYYY-MM-DD format.",
            ephemeral=True,
        )
    except Exception as ex:
        print("Exception occurred:", ex)
        await interaction.response.send_message(
            "An error occurred while processing your request. Please try again later.",
            ephemeral=True,
        )


async def setup(tree: app_commands.CommandTree):
    """
    Sets up the `/delete` command in the Discord command tree.
    """
    @tree.command(name="delete", description="Delete your spending records.")
    async def delete_command(
        interaction: discord.Interaction,
        option: str,
        date: str = None,
    ):
        await run(interaction, option, date)

    # Add autocomplete for the "option" parameter
    @delete_command.autocomplete("option")
    async def autocomplete_option(interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name="All Records", value="all"),
            app_commands.Choice(name="Specific Date", value="date"),
        ]
