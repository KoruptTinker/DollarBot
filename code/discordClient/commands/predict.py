import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import logging
from typing import Dict, List, Union, Tuple
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get environment variables
MONGO_URI = os.getenv('MONGO_CONNECTION_URL')
DISCORD_TOKEN = os.getenv('BOT_TOKEN')

# Verify environment variables
if not MONGO_URI or not DISCORD_TOKEN:
    raise ValueError("Required environment variables (MONGO_URI, DISCORD_TOKEN) are not set")

# MongoDB setup
try:
    client = MongoClient(MONGO_URI)
    db = client['expense_tracker']
    expenses_collection = db['expenses']
    users_collection = db['users']
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        await self.tree.sync()
        
bot = Bot()

def get_user_details(discord_id: int) -> Dict:
    """Fetch user details from MongoDB using Discord ID"""
    return users_collection.find_one({"discord_id": str(discord_id)})

def get_user_history(telegram_chat_id: str) -> List[Dict]:
    """Fetch user's expense history from MongoDB using Telegram chat ID"""
    return list(expenses_collection.find({"user_id": telegram_chat_id}))

def calculate_budget_predictions(history: List[Dict]) -> Tuple[float, Dict[str, float]]:
    """Calculate monthly budget predictions based on historical data"""
    if len(history) < 2:
        return None, None
    
    category_wise_total = {}
    total_spent = 0.0
    recorded_days = []
    
    for record in history:
        category = record['category']
        amount = float(record['amount'])
        total_spent += amount
        category_wise_total[category] = category_wise_total.get(category, 0) + amount
        recorded_days.append(datetime.strptime(record['date'], '%Y-%m-%d'))
    
    day_difference = (max(recorded_days) - min(recorded_days)).days + 1
    avg_per_day = total_spent / day_difference
    predicted_spending = avg_per_day * 30

    category_predictions = {
        category: round((total / day_difference) * 30, 2) 
        for category, total in category_wise_total.items()
    }
    overall_prediction = round(predicted_spending, 2)

    return overall_prediction, category_predictions

@bot.tree.command(name="predict", description="Predicts next month's budget based on spending history")
async def predict(interaction: discord.Interaction):
    """Predicts next month's budget based on spending history"""
    try:
        # Get user details

        user_details = get_user_details(interaction.user.id)
        if user_details is None:
            await interaction.response.send_message(
                "You don't have your Discord account linked to an active Telegram account. "
                "Use /link command on Telegram to learn more",
                ephemeral=True
            )
            return

        # Get user history
        history = get_user_history(user_details["telegram_chat_id"])
        if not history or len(history) < 2:
            await interaction.response.send_message(
                "Sorry, you do not have sufficient spending records to predict a future budget",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        # Calculate predictions
        overall_prediction, category_predictions = calculate_budget_predictions(history)
        
        if overall_prediction is None:
            await interaction.followup.send("Not enough data to make predictions")
            return

        # Create embed for response
        embed = discord.Embed(
            title="Budget Prediction", 
            color=discord.Color.blue(),
            description=f"Overall budget prediction for next month: ${overall_prediction:.2f}"
        )

        # Add category predictions
        for category, amount in category_predictions.items():
            embed.add_field(
                name=category.capitalize(),
                value=f"${amount:.2f}",
                inline=True
            )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        logger.exception("Error in predict command")
        if not interaction.response.is_done():
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

@bot.event
async def on_ready():
    """Event handler for when the bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')

async def setup(tree: app_commands.CommandTree):
    """Setup function to register commands with the command tree"""
    
    @tree.command(name="predict", description="Predicts next month's budget based on spending history")
    async def predict(interaction: discord.Interaction):
        try:
            # Get user details
            user_details = get_user_details(interaction.user.id)
            if user_details is None:
                await interaction.response.send_message(
                    "You don't have your Discord account linked to an active Telegram account. "
                    "Use /link command on Telegram to learn more",
                    ephemeral=True
                )
                return

            # Get user history
            history = get_user_history(user_details["telegram_chat_id"])
            if not history or len(history) < 2:
                await interaction.response.send_message(
                    "Sorry, you do not have sufficient spending records to predict a future budget",
                    ephemeral=True
                )
                return

            await interaction.response.defer()

            # Calculate predictions
            overall_prediction, category_predictions = calculate_budget_predictions(history)
            
            if overall_prediction is None:
                await interaction.followup.send("Not enough data to make predictions")
                return

            # Create embed for response
            embed = discord.Embed(
                title="Budget Prediction", 
                color=discord.Color.blue(),
                description=f"Overall budget prediction for next month: ${overall_prediction:.2f}"
            )

            # Add category predictions
            for category, amount in category_predictions.items():
                embed.add_field(
                    name=category.capitalize(),
                    value=f"${amount:.2f}",
                    inline=True
                )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.exception("Error in predict command")
            if not interaction.response.is_done():
                await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
            else:
                await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")