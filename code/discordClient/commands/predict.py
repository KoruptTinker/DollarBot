import time
import logging
from datetime import datetime
import pymongo
import discord
from config import Secrets
import asyncio

secrets = Secrets()

async def run(interaction: discord.Interaction, bot: discord.Client):
    """
    run(interaction, bot): This is the main function used to implement the predict feature.
    It takes 2 arguments for processing - interaction which is the message from the user, and
    bot which is the discord bot object.
    """
    user_id = interaction.user.id
    user_details = fetch_user_from_discord(user_id)
    if user_details is None or len(user_details["history"]) < 2:
        await interaction.response.send_message(
            "Sorry, you do not have sufficient spending records to predict a future budget"
        )
    else:
        await predict_total(interaction, bot, user_details)


async def predict_total(interaction: discord.Interaction, bot: discord.Client, user_details: dict):
    """
    estimate_total(interaction, bot): It takes 2 arguments for processing - interaction which is the message
    from the user, and bot which is the discord bot object. This function loads the user's data.
    """
    try:
        history = user_details["history"]
        available_categories = get_available_categories(history)
        category_wise_history = get_category_wise_spendings(available_categories, history)
        
        await interaction.response.send_message("Hold on! Calculating...")
        # show the bot "typing"
        async with interaction.channel.typing():
            time.sleep(0.5)
        
        category_spendings = {}
        for category in available_categories:
            category_spendings[category] = predict_category_spending(
                category_wise_history[category]
            )
        
        overall_spending = predict_overall_spending(user_details, category_spendings)
        
        await interaction.response.send_message(
            f"Your overall budget for next month can be: ${overall_spending}",
        )
        
        category_budgets = get_formatted_predictions(category_spendings)
        await interaction.response.send_message(category_budgets)
    
    except Exception as e:
        logging.exception(str(e))
        await interaction.response.send_message(f"Error: {str(e)}")


def predict_category_spending(category_history: list):
    """
    predict_category_spending(history): Takes 1 argument for processing - category_history
    which is the record of all expenses from a category.
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


def predict_overall_spending(user_details: dict, category_wise_spending: dict):
    """
    predict_overall_spending(user_details, category_wise_spending): Takes 2 arguments for processing
    user_details and category_wise_spending. It sums the predicted spending for all categories.
    """
    overall_spending = 0
    for category in category_wise_spending.keys():
        if isinstance(category_wise_spending[category], float):
            overall_spending += category_wise_spending[category]
    if overall_spending != 0:
        return overall_spending
    else:
        history = user_details["history"]
        overall_spending = predict_category_spending(history)
        return overall_spending


def fetch_user_from_discord(user_id: int) -> dict:
    """
    Fetches user data from MongoDB based on Discord user ID.
    """
    user_data = user_collection.find_one({"user_id": user_id})
    if user_data:
        return user_data
    return None


def get_available_categories(history: list) -> list:
    """
    Returns a list of available categories from the user's history.
    """
    categories = set()
    for record in history:
        categories.add(record["category"])
    return list(categories)


def get_category_wise_spendings(categories: list, history: list) -> dict:
    """
    Returns a dictionary with category-wise spending history.
    """
    category_wise_history = {category: [] for category in categories}
    for record in history:
        category_wise_history[record["category"]].append(record)
    return category_wise_history


def get_formatted_predictions(category_spendings: dict) -> str:
    """
    Formats the category-wise predicted spendings for display.
    """
    formatted = ""
    for category, spending in category_spendings.items():
        formatted += f"{category}: ${spending}\n"
    return formatted
