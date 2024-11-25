from discord import app_commands
import discord
import helper
import graphing
from datetime import datetime
from tabulate import tabulate
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def display(interaction: discord.Interaction):
    try:
        # Get user details and log
        user_details = helper.fetchUserFromDiscord(interaction.user.id)
        logger.debug(f"User details: {user_details}")

        if user_details is None:
            await interaction.response.send_message(
                "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
            )
            return

        chat_id = user_details["telegram_chat_id"]
        logger.debug(f"Chat ID: {chat_id}")

        history = helper.getUserHistory(chat_id)
        logger.debug(f"User history: {history}")

        if history is None or len(history) == 0:
            await interaction.response.send_message(
                "Oops! Looks like you do not have any spending records!"
            )
            return

        # Get current day and month data
        current_date = datetime.now()
        day_query = current_date.strftime(helper.getDateFormat())
        month_query = current_date.strftime(helper.getMonthFormat())

        logger.debug(f"Day query: {day_query}")
        logger.debug(f"Month query: {month_query}")

        # Query for daily records
        day_records = [value for value in history if str(day_query) in value]
        # Query for monthly records
        month_records = [value for value in history if str(month_query) in value]

        logger.debug(f"Day records: {day_records}")
        logger.debug(f"Month records: {month_records}")

        # Calculate daily and monthly totals
        day_total_text, day_total_dict = calculate_spendings(day_records)
        month_total_text, month_total_dict = calculate_spendings(month_records)

        logger.debug(f"Day totals: {day_total_dict}")
        logger.debug(f"Month totals: {month_total_dict}")

        # Format response message
        response = []

        # Daily spending table
        if day_total_dict:
            day_table = [["Category", "Amount"]]
            for category, amount in day_total_dict.items():
                day_table.append([str(category), f"$ {amount}"])
            day_formatted = (
                "**Daily Spending:**\n```\n"
                + tabulate(day_table, headers="firstrow", tablefmt="grid")
                + "\n```"
            )
            response.append(day_formatted)

        # Monthly spending table
        if month_total_dict:
            month_table = [["Category", "Amount"]]
            for category, amount in month_total_dict.items():
                month_table.append([str(category), f"$ {amount}"])
            month_formatted = (
                "**Monthly Spending:**\n```\n"
                + tabulate(month_table, headers="firstrow", tablefmt="grid")
                + "\n```"
            )
            response.append(month_formatted)

        if not response:
            await interaction.response.send_message(
                "You have no spending records for today or this month!"
            )
            return

        # Send text response
        await interaction.response.send_message("\n".join(response))

        # Generate and send graphs
        monthly_budget = helper.getCategoryBudget(chat_id)
        logger.debug(f"Monthly budget: {monthly_budget}")

        if month_total_text:
            photo_paths = graphing.visualize_new(month_total_text, monthly_budget)
            logger.debug(f"Generated photo paths: {photo_paths}")

            for photo_path in photo_paths:
                with open(photo_path, "rb") as photo:
                    await interaction.followup.send(file=discord.File(photo))
                os.remove(photo_path)

    except Exception as e:
        logger.error(f"Error in display command: {str(e)}", exc_info=True)
        await interaction.response.send_message(f"Oops! An error occurred: {str(e)}")


def calculate_spendings(queryResult):
    try:
        total_dict = {}

        for row in queryResult:
            s = row.split(",")
            cat = s[1]
            if cat in total_dict:
                total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
            else:
                total_dict[cat] = float(s[2])

        total_text = ""
        for key, value in total_dict.items():
            total_text += f"{key} ${value}\n"

        logger.debug(f"Calculated totals - text: {total_text}, dict: {total_dict}")
        return total_text, total_dict

    except Exception as e:
        logger.error(f"Error in calculate_spendings: {str(e)}", exc_info=True)
        raise


async def setup(tree: app_commands.CommandTree):
    tree.command(
        name="display", description="View spending statistics for today and this month"
    )(display)
