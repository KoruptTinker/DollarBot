from discord import app_commands
import discord
import helper
# from code.discordClient.commands.budget_view import view_budget
# import budget_update
# import budget_delete
# import budget_limit
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


@app_commands.describe(option="Select an option",)
@app_commands.choices(option=BUDGET_OPTIONS)
async def budget(interaction: discord.Interaction, option: app_commands.Choice[str]):
    # Defer the reply immediately to prevent timeout
    await interaction.response.defer()

    try:
        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
        op = option
        options = helper.getBudgetOptions()
        if op.value not in options.keys():
            await interaction.followup.send("Invalid option selected!")
            return

        if op.value == "update":
            await interaction.followup.send("Update Budget")
            helper.read_category_json()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            # options = helper.getBudgetTypes()
            # markup.row_width = 2
            # for c in options.values():
            #     markup.add(c)
            # msg = bot.reply_to(message, "Select Budget Type", reply_markup=markup)
            # bot.register_next_step_handler(msg, post_type_selection, bot)

        elif op.value == "view":
            try:
                print("here")
                chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
                if helper.isOverallBudgetAvailable(chat_id) or helper.isCategoryBudgetAvailable(
                    chat_id
                ):
                    await display_overall_budget(interaction)
                    await display_category_budget(interaction)
                else:
                    raise Exception(
                        "Budget does not exist. Use "
                        + helper.getBudgetOptions()["update"]
                        + " option to add/update the budget"
                    )
            except Exception as e:
                await interaction.followup.send("An error occurred!" + str(e))

        elif op.value == "delete":
            await interaction.followup.send("Delete Budget")
        elif op.value == "exit":
            return

    except Exception as e:
        await interaction.followup.send("Oops!" + str(e))


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


async def setup(tree: app_commands.CommandTree):
    """Register the add command with the command tree."""
    tree.command(name="budget", description="add details here")(budget)
