import discord
from discord.ext import commands
import time
import json
import logging
from datetime import datetime

class PredictionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "user_data.json"
        
    def read_json(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_json(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_user_history(self, user_id):
        data = self.read_json()
        return data.get(str(user_id), [])

    def get_available_categories(self, history):
        return list(set(record["category"] for record in history))

    def get_category_wise_spendings(self, categories, history):
        category_wise = {}
        for category in categories:
            category_wise[category] = [
                record for record in history 
                if record["category"] == category
            ]
        return category_wise

    @commands.command(name="predict")
    async def predict(self, ctx):
        """Predicts future budget based on spending history"""
        try:
            user_id = ctx.author.id
            history = self.get_user_history(user_id)
            
            if not history or len(history) < 2:
                await ctx.send("Sorry, you don't have sufficient spending records to predict a future budget")
                return

            await self.predict_total(ctx)

        except Exception as e:
            logging.exception(str(e))
            await ctx.send(f"Error: {str(e)}")

    async def predict_total(self, ctx):
        """Calculate and display total budget predictions"""
        try:
            user_id = ctx.author.id
            history = self.get_user_history(user_id)
            available_categories = self.get_available_categories(history)
            category_wise_history = self.get_category_wise_spendings(
                available_categories, history
            )

            processing_msg = await ctx.send("Hold on! Calculating...")
            
            category_spendings = {}
            for category in available_categories:
                category_spendings[category] = self.predict_category_spending(
                    category_wise_history[category]
                )

            overall_spending = self.predict_overall_spending(user_id, category_spendings)

            embed = discord.Embed(
                title="Budget Prediction",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Overall Monthly Budget",
                value=f"${overall_spending:,.2f}",
                inline=False
            )

            for category, amount in category_spendings.items():
                if isinstance(amount, float):
                    embed.add_field(
                        name=category,
                        value=f"${amount:,.2f}",
                        inline=True
                    )

            await processing_msg.delete()
            await ctx.send(embed=embed)

        except Exception as e:
            logging.exception(str(e))
            await ctx.send(f"Error: {str(e)}")

    def predict_category_spending(self, category_history):
        """Predict spending for a specific category"""
        if len(category_history) < 2:
            return "Not enough records"
            
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

    def predict_overall_spending(self, user_id, category_wise_spending):
        """Predict overall monthly spending"""
        overall_spending = sum(
            amount for amount in category_wise_spending.values() 
            if isinstance(amount, float)
        )
        
        if overall_spending != 0:
            return overall_spending
            
        history = self.get_user_history(user_id)
        return self.predict_category_spending(history)

async def setup(bot):
    await bot.add_cog(PredictionCog(bot))