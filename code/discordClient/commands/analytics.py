from discord import app_commands
import discord
import helper
from datetime import datetime
import os
from tabulate import tabulate
import graphing
import asyncio

OPTIONS = [
    app_commands.Choice(name="Overall budget split by Category", value="overall"),
    app_commands.Choice(name="Split of current month expenditure", value="spend"),
    app_commands.Choice(name="Remaining value", value="remaining"),
    app_commands.Choice(name="Time series graph of spend history", value="history"),
]


@app_commands.describe(
    option="Select an option",
)
@app_commands.choices(option=OPTIONS)
async def analytics(
    interaction: discord.Interaction,
    option: app_commands.Choice[str],
):
    # Defer the reply immediately to prevent timeout
    await interaction.response.defer()

    try:
        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
        op = option
        options = helper.getAnalyticsOptions()

        if op.value not in options.keys():
            await interaction.followup.send("Invalid option selected!")
            return

        if op.value == "overall":
            helper.read_category_json()

            if not helper.isCategoryBudgetAvailable(chat_id):
                await interaction.followup.send("No category budget available")
                return

            category_budget = {}
            for cat in helper.getCategoryBudget(chat_id):
                if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
                    cat_budget = helper.getCategoryBudgetByCategory(chat_id, cat)
                    if cat_budget != "0":
                        category_budget[cat] = cat_budget

            if category_budget == {}:
                await interaction.followup.send(
                    "You are yet to set your budget for different categories."
                )
            else:
                graphing.overall_split(category_budget)

                with open("overall_split.png", "rb") as file:
                    files = [discord.File(file)]
                    await interaction.followup.send(files=files)

                # Add a small delay to ensure file is fully processed
                await asyncio.sleep(0.5)
                try:
                    os.remove("overall_split.png")
                except OSError:
                    # If file is still locked, try again after a longer delay
                    await asyncio.sleep(1)
                    os.remove("overall_split.png")

        elif op.value == "spend":
            category_spend = {}
            user_history = helper.getUserHistory(chat_id)

            category_spend = {}
            current_month = datetime.now().today().strftime("%Y-%m")
            for spend in user_history:
                if current_month in spend["date"]:
                    category_spend[spend["category"]] = (
                        category_spend.get(spend["category"], 0) + spend["amount"]
                    )
            if category_spend != {}:
                graphing.spend_wise_split(category_spend)

            if category_spend == {}:
                await interaction.followup.send(
                    "No expenditure available for this month"
                )
                return

            graphing.spend_wise_split(category_spend)

            with open("spend_wise.png", "rb") as file:
                files = [discord.File(file)]
                await interaction.followup.send(files=files)

            # Add a small delay to ensure file is fully processed
            await asyncio.sleep(0.5)
            try:
                os.remove("spend_wise.png")
            except OSError:
                # If file is still locked, try again after a longer delay
                await asyncio.sleep(1)
                os.remove("spend_wise.png")

        elif op.value == "remaining":
            categoryBudget = helper.getCategoryBudget(chat_id)
            user_history = helper.getUserHistory(chat_id)
            if categoryBudget == {}:
                await interaction.followup.send("No category budget available")
                return

            category_spend_percent = {}
            categories = helper.getSpendCategories()

            category_spend = {}
            for spend in user_history:
                category_spend[spend["category"]] = (
                    category_spend.get(spend["category"], 0) + spend["amount"]
                )
            if category_spend != {}:
                graphing.spend_wise_split(category_spend)

            for cat in categoryBudget.keys():
                percent = (category_spend.get(cat, 0) / categoryBudget[cat]) * 100
                if percent > 0:
                    category_spend_percent[cat] = percent

            if category_spend_percent != {}:
                graphing.remaining(category_spend_percent)
                # Properly handle file opening and closing using context manager
                with open("remaining.png", "rb") as file:
                    files = [discord.File(file)]
                    await interaction.followup.send(files=files)

                # Add a small delay to ensure file is fully processed
                await asyncio.sleep(0.5)
                try:
                    os.remove("remaining.png")
                except OSError:
                    # If file is still locked, try again after a longer delay
                    await asyncio.sleep(1)
                    os.remove("remaining.png")
            else:
                await interaction.followup.send(
                    "You are yet to set your budget for different categories."
                )

        elif op.value == "history":
            if not helper.getUserHistory(chat_id):
                await interaction.followup.send("No history available")
                return

            cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)

            graphing.time_series(cat_spend_dict)

            # Properly handle file opening and closing using context manager
            with open("time_series.png", "rb") as file:
                files = [discord.File(file)]
                await interaction.followup.send(files=files)

            # Add a small delay to ensure file is fully processed
            await asyncio.sleep(0.5)
            try:
                os.remove("time_series.png")
            except OSError:
                # If file is still locked, try again after a longer delay
                await asyncio.sleep(1)
                os.remove("time_series.png")

    except Exception as e:
        await interaction.followup.send("An error occurred!" + str(e))


async def setup(tree: app_commands.CommandTree):
    """Register the add command with the command tree."""
    tree.command(name="analytics", description="add details here")(analytics)
