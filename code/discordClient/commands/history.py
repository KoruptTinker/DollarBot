from discord import app_commands
import discord
import helper
from datetime import datetime
from tabulate import tabulate


async def history(interaction: discord.Interaction):
    try:
        user_details = helper.fetchUserFromDiscord(interaction.user.id)
        if user_details is None:
            interaction.response.send_message(
                "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
            )
            return

        user_history = helper.getUserHistory(user_details["telegram_chat_id"])

        if user_history is None or len(user_history) == 0:
            await interaction.response.send_message(
                "Sorry! No spending records found!", ephemeral=True
            )
            return

        table = [["Date", "Category", "Amount"]]
        current_date = datetime.now()

        for rec in user_history:
            date = rec["date"]
            category = rec["category"]
            amount = rec["amount"]

            date_time = datetime.strptime(date, "%Y-%m-%d")

            if date_time <= current_date:
                table.append([date, category, f"$ {amount}"])

        # Format table with code block for better Discord display
        formatted_table = (
            "```\n" + tabulate(table, headers="firstrow", tablefmt="grid") + "\n```"
        )

        await interaction.response.send_message(formatted_table)
    except Exception as e:
        await interaction.response.send_message("Oops! " + str(e))


async def setup(tree: app_commands.CommandTree):
    tree.command(name="history", description="View a detailed summary of expenditure")(
        history
    )