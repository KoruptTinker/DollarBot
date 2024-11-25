import discord
from discord.ext import commands
from datetime import datetime
import logging
from typing import Dict, List, Union
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('Mmongodb+srv://bkbhayan:SEProject@cluster0.ceixt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
DISCORD_TOKEN = os.getenv('MTMwOTMzNzE4MzI4NjcyNjY1Nw.GDzL8I.WZSQwd6LFl_XEEZ7os96asynKnAkCfwJcfqjqg')

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client['expense_tracker']
expenses_collection = db['expenses']

bot = commands.Bot(command_prefix='!')

def get_user_history(user_id: int) -> List[Dict]:
    """Fetch user's expense history from MongoDB"""
    history = list(expenses_collection.find({"user_id": str(user_id)}))
    return history if history else []

def get_available_categories(history: List[Dict]) -> List[str]:
    return list(set(record["category"] for record in history))

def get_category_wise_spendings(categories: List[str], history: List[Dict]) -> Dict:
    category_history = {}
    for category in categories:
        category_history[category] = [
            record for record in history if record["category"] == category
        ]
    return category_history

def predict_category_spending(category_history: List[Dict]) -> Union[str, float]:
    if len(category_history) < 2:
        return "Not enough records to predict spendings"
        
    total_spent = sum(float(record["amount"]) for record in category_history)
    recorded_days = [
        datetime.strptime(record["date"], "%Y-%m-%d") 
        for record in category_history
    ]
    
    first = min(recorded_days)
    last = max(recorded_days)
    day_difference = abs((last - first).days) + 1
    avg_per_day = total_spent / day_difference
    predicted_spending = avg_per_day * 30
    
    return round(predicted_spending, 2)

def predict_overall_spending(user_id: int, category_spending: Dict) -> float:
    overall_spending = sum(
        amount for amount in category_spending.values() 
        if isinstance(amount, float)
    )
    
    if overall_spending != 0:
        return overall_spending
        
    history = get_user_history(user_id)
    return predict_category_spending(history)

@bot.command(name='predict')
async def predict(ctx):
    """Predicts next month's budget based on spending history"""
    try:
        user_id = ctx.author.id
        history = get_user_history(user_id)
        
        if not history or len(history) < 2:
            await ctx.send("Sorry, you do not have sufficient spending records to predict a future budget")
            return

        # Send initial processing message
        processing_msg = await ctx.send("Hold on! Calculating...")

        # Get predictions
        available_categories = get_available_categories(history)
        category_wise_history = get_category_wise_spendings(available_categories, history)
        
        category_spendings = {
            category: predict_category_spending(category_wise_history[category])
            for category in available_categories
        }
        
        overall_spending = predict_overall_spending(user_id, category_spendings)

        # Create embed for response
        embed = discord.Embed(
            title="Budget Prediction", 
            color=discord.Color.blue(),
            description=f"Overall budget prediction for next month: ${overall_spending:.2f}"
        )

        # Add category predictions
        for category, amount in category_spendings.items():
            if isinstance(amount, float):
                embed.add_field(
                    name=category.capitalize(),
                    value=f"${amount:.2f}",
                    inline=True
                )

        # Delete processing message and send results
        await processing_msg.delete()
        await ctx.send(embed=embed)

    except Exception as e:
        logging.exception(str(e))
        await ctx.send(f"An error occurred: {str(e)}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)