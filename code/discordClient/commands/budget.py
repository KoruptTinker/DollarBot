from discord import app_commands
import discord
import helper
import budget_view
import budget_update
import budget_delete
import budget_limit
import logging
from telebot import types

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
            await interaction.followup.send("View Budget")
        elif op.value == "delete":
            await interaction.followup.send("Delete Budget")
        elif op.value == "exit":
            return

    except Exception as e:
        await interaction.followup.send("Oops!" + str(e))


async def setup(tree: app_commands.CommandTree):
    """Register the add command with the command tree."""
    tree.command(name="budget", description="add details here")(budget)
