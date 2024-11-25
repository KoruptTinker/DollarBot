from discord import app_commands
import discord
import csv
import re
import helper
import logging
from gmail import GMailClient
from config import Secrets
import asyncio

secrets = Secrets()
emailClient = GMailClient(secrets.GmailAccount, secrets.GmailPassword)

async def run(interaction: discord.Interaction):
    """
    Handles the email functionality as a slash command.
    """
    try:
        # Defer the interaction to prevent timeout
        await interaction.response.defer()

        helper.read_json()
        
        user_id = interaction.user.id
        if user_id is None:
            await interaction.response.send_message("You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more")
            return

        # Ensure we get the correct telegram_chat_id
        user_details = helper.fetchUserFromDiscord(user_id)
        if not user_details or "telegram_chat_id" not in user_details:
            await interaction.response.send_message("No linked Telegram account found.")
            return

        user_history = helper.getUserHistory(user_details["telegram_chat_id"])
        if not user_history:
            await interaction.response.send_message("Sorry! No spending records found.")
            return

        # Ask for the email address
        await interaction.followup.send("Please enter your email address:")

        # Wait for the email response
        def check(m):
            print(f"Message received :{m}from {m.author.id} Content : {m.content}") 
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            email_message = await interaction.client.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond. Please try again.")
            return

        email = email_message.content
        print(f"Received email: {email}")  # Debugging line
        email = email.strip()

        # Validate email format
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.fullmatch(regex, email):
            await interaction.followup.send("Invalid email address. Please try again.")
            return

        # Prepare the CSV file
        table = [["Date", "Category", "Amount"]]
        for rec in user_history:
            date = rec["date"]
            category = rec["category"]
            amount = f"$ {rec['amount']}"
            table.append([date, category, amount])

        with open("history.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(table)

        # Send the email
        mail_content = """Hello,
        This email has an attached copy of your expenditure history.
        Thank you!
        """
        emailClient.send_email(email, "Spending History Document", mail_content, "history.csv")

        # Respond with success
        await interaction.followup.send("Mail sent successfully!")

    except Exception as ex:
        logging.error(str(ex), exc_info=True)
        await interaction.followup.send(f"An error occurred: {str(ex)}")
