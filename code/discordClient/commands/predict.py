import time
import logging
from datetime import datetime
import pymongo
import discord
from discord import app_commands
from config import Secrets
import asyncio
import helper

secrets = Secrets()

async def predict(interaction: discord.Interaction):
    await interaction.response.defer()
    user_id = interaction.user.id
    user_details = helper.fetchUserFromDiscord(user_id)
    chat_id = user_details["telegram_chat_id"]
    history = helper.getUserHistory(chat_id)
    if history is None or len(history) < 2:
        await interaction.followup.send(
            "Sorry, you do not have sufficient spending records to predict a future budget",
        )
    else:
        try:
            available_categories = helper.getAvailableCategories(history)
            category_wise_history = helper.getCategoryWiseSpendings(
                available_categories, history
            )
            await interaction.followup.send("Hold on! Calculating...")
            # show the bot "typing" (max. 5 secs)
            category_spendings = {}
            for category in available_categories:
                category_spendings[category] = predict_category_spending(
                    category_wise_history[category]
                )
            overall_spending = predict_overall_spending(chat_id, category_spendings)
            await interaction.followup.send(
                "Your overall budget for next month can be: ${}".format(overall_spending),
            )
            category_budgets = helper.getFormattedPredictions(category_spendings)
            await interaction.followup.send(category_budgets)
        except Exception as e:
            logging.exception(str(e))
            interaction.followup.send(f"Something went wrong: {str(e)}")

def predict_category_spending(category_history):
    """
    predict_category_spending(history): Takes 1 arguments for processing - category_history
    which is the record of all expenses from a category. It parses the history
    and turns it into a form suitable for display on the UI by the user.
    """
    if len(category_history) < 2:
        return "Not enough records to predict spendings"
    total_spent = 0
    recorded_days = []
    for record in category_history:
        total_spent += float(record["amount"])
        date = datetime.strptime(record["date"], "%Y-%m-%d")
        recorded_days.append(date)
    first = min(recorded_days)
    last = max(recorded_days)
    day_difference = abs(int((last - first).days)) + 1
    avg_per_day = total_spent / day_difference
    predicted_spending = avg_per_day * 30
    return round(predicted_spending, 2)


def predict_overall_spending(chat_id, category_wise_spending):
    """
    predict_overall_spending(chat_id, category_wise_spending): Takes 2 arguments for processing
    chatId and category_wise_spending. It parses the history
    and turns it into a form suitable for display on the UI by the user.
    """
    overall_spending = 0
    for category in category_wise_spending.keys():
        if type(category_wise_spending[category]) == float:
            overall_spending += category_wise_spending[category]
    if overall_spending != 0:
        return overall_spending
    else:
        history = helper.getUserHistory(chat_id)
        overall_spending = predict_category_spending(history)
        return overall_spending


async def setup(tree: app_commands.CommandTree):
    tree.command(name="predict", description="Predicts monthly expenditure")(predict)