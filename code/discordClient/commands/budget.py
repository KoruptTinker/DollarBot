from discord import app_commands
import discord
from discord.ui import Modal, TextInput
import helper
import logging
import asyncio
from telebot import types
import graphing
import os

BUDGET_OPTIONS = [
    app_commands.Choice(name="Add/Update", value="update"),
    app_commands.Choice(name="View", value="view"),
    app_commands.Choice(name="Delete", value="delete"),
    app_commands.Choice(name="Exit", value="exit"),
]

BUDGET_TYPE = {
    app_commands.Choice(name="Category-Wise Budget", value="category"),
    app_commands.Choice(name="Exit", value="exit"),
}


@app_commands.describe(option="Select an option")
@app_commands.choices(option=BUDGET_OPTIONS)
async def budget(interaction: discord.Interaction, option: app_commands.Choice[str]):
    await interaction.response.defer()

    try:
        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]

        if option.value == "update":
            await budget_edit(interaction)
        elif option.value == "view":
            if helper.isOverallBudgetAvailable(
                chat_id
            ) or helper.isCategoryBudgetAvailable(chat_id):
                await display_overall_budget(interaction)
                await display_category_budget(interaction)
            else:
                await interaction.followup.send(
                    "Budget does not exist. Use the update option to add/update the budget"
                )
        elif option.value == "delete":
            helper.resetBudget(chat_id)
            await interaction.followup.send("Budget deleted!")
        elif option.value == "exit":
            await interaction.followup.send("Budget management cancelled.")

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")


class BudgetModal(Modal, title="Enter Budget Amount"):
    budget_amount = TextInput(
        label="Budget Amount",
        placeholder="Enter the budget amount (e.g., 100.00)",
        required=True,
        min_length=1,
        max_length=10,
    )

    def __init__(
        self, selected_category: str, chat_id: int, interaction: discord.Interaction
    ):
        super().__init__()
        self.selected_category = selected_category
        self.chat_id = chat_id
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = float(self.budget_amount.value)
            helper.update_budget(self.chat_id, self.selected_category, amount)
            await interaction.response.send_message(
                f"Budget updated for {self.selected_category}: ${amount}"
            )
        except ValueError:
            await interaction.response.send_message(
                "Invalid amount. Please enter a numeric value.", ephemeral=True
            )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )
        logging.error(f"Error in BudgetModal: {error}")


class BudgetCategorySelect(discord.ui.Select):
    def __init__(self):
        categories = helper.read_category_json()
        options = [
            discord.SelectOption(
                label=category.strip(), description=f"Set budget for {category.strip()}"
            )
            for category in categories["categories"].split(",")
        ]
        super().__init__(
            placeholder="Select a category", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
        modal = BudgetModal(
            selected_category=self.values[0], chat_id=chat_id, interaction=interaction
        )
        await interaction.response.send_modal(modal)


class BudgetView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(BudgetCategorySelect())


async def budget_edit(interaction: discord.Interaction):
    try:
        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
        view = BudgetView()
        await interaction.followup.send("Select a category:", view=view)
    except Exception as e:
        logging.error(f"Error in budget_edit: {str(e)}")
        await interaction.followup.send(f"Error: {str(e)}")


async def display_category_budget(interaction: discord.Interaction):
    """
    display_category_budget(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object
    from the run(message, bot): in the same file. It gets the category-wise budget for the
    user based on their chat ID using the helper module.It then processes it into a string
    format suitable for display, and returns the same through the bot to the Telegram UI.
    """
    chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
    if helper.isCategoryBudgetAvailable(chat_id):
        data = helper.getCategoryBudget(chat_id)
        print(data, "data")
        if graphing.viewBudget(data):
            with open("budget.png", "rb") as file:
                files = [discord.File(file)]
                await interaction.followup.send(files=files)

            # Add a small delay to ensure file is fully processed
            await asyncio.sleep(0.5)
            try:
                os.remove("budget.png")
            except OSError:
                # If file is still locked, try again after a longer delay
                await asyncio.sleep(1)
                os.remove("budget.png")
        else:
            await interaction.followup.send(
                "You are yet to set your budget for different categories."
            )
    else:
        await interaction.followup.send(
            "You are yet to set your budget for different categories."
        )


async def display_overall_budget(interaction: discord.Interaction):
    """
    display_overall_budget(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot
    object from the run(message, bot): in the same file. It gets the budget for the
    user based on their chat ID using the helper module and returns the same through the bot to the Telegram UI.
    """
    chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
    data = helper.getOverallBudget(chat_id)
    await interaction.followup.send("Overall Budget: $" + str(data))


async def setup(tree: app_commands.CommandTree):
    tree.command(name="budget", description="Manage your budget settings")(budget)
