from discord import app_commands
import discord
import helper
from datetime import datetime
from tabulate import tabulate

CATEGORIES = [
    app_commands.Choice(name="Food", value="Food"),
    app_commands.Choice(name="Transport", value="Transport"),
    app_commands.Choice(name="Groceries", value="Groceries"),
    app_commands.Choice(name="Shopping", value="Shopping"),
    app_commands.Choice(name="Utilities", value="Utilities"),
    app_commands.Choice(name="Miscellaneous", value="Miscellaneous"),
]


@app_commands.describe(
    date="Date of expense (YYYY-MM-DD)",
    category="Category of expense",
    amount="Amount spent (must be greater than 0)",
)
@app_commands.choices(category=CATEGORIES)
async def add(
    interaction: discord.Interaction,
    date: str,
    category: app_commands.Choice[str],
    amount: float,
):
    """Add a new expense entry for the user.

    This command allows users to add a new expense record with date, category, and amount.
    It performs validation on the input data and stores the expense in the database if valid.

    The function validates:
        - User has a linked Telegram account
        - Date format and ensures it's not in the future
        - Amount is positive
    
    On success, it stores the expense and sends a confirmation message.
    On failure, it sends an appropriate error message.
    """
    # Validate date
    try:
        user_data = helper.fetchUserFromDiscord(interaction.user.id)
        if user_data is None:
            await interaction.response.send_message(
                "Error: Please connect your telegram account to proceed"
            )
            return
        expense_date = datetime.strptime(date, "%Y-%m-%d")
        if expense_date > datetime.now():
            await interaction.response.send_message(
                "Error: Date cannot be in the future!", ephemeral=True
            )
            return
    except ValueError:
        await interaction.response.send_message(
            "Error: Invalid date format. Use YYYY-MM-DD", ephemeral=True
        )
        return

    # Validate amount
    if amount <= 0:
        await interaction.response.send_message(
            "Error: Amount must be greater than 0!", ephemeral=True
        )
        return

    helper.createSpends(user_data["telegram_chat_id"], date, category.value, amount)

    # If all validations pass, process the expense
    await interaction.response.send_message(
        f"Expense added successfully!\n"
        f"Date: {date}\n"
        f"Category: {category.name}\n"
        f"Amount: ${amount:.2f}"
    )


async def setup(tree: app_commands.CommandTree):
    """Register the add command with the command tree.
    """
    tree.command(name="add", description="Add a new expenditure")(add)
