#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import pdf
import display
import estimate
import delete
import add
import add_currencies
import budget
import analytics
import predict
import updateCategory
import weekly, new_weekly
import monthly, new_monthly
import sendEmail
import add_recurring
from datetime import datetime
from telebot import types
from helper import migrate_users
from helper import migrate_data_entries
import add_balance
from config import Secrets
from mongo import MongoDB
from discordClient import DiscordClient
import link
import argparse
import sys

import insight


secrets = Secrets()
mongoClient = MongoDB(secrets.MongoConnectionURL, secrets.DBName)
discordClient = DiscordClient(secrets.GuildID, secrets.BotToken)

bot = telebot.TeleBot(secrets.TelegramAPIKey)

telebot.logger.setLevel(logging.INFO)

option = {}

# === Documentation of code.py ===


# Define listener for requests by user
def listener(user_requests):
    """
    listener(user_requests): Takes 1 argument user_requests and logs all user
    interaction with the bot including all bot commands run and any other issue logs.
    """
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )

    message = (
        "Sorry, I can't understand messages yet :/\n"
        "I can only understand commands that start with /. \n\n"
        "Type /faq or /help if you are stuck."
    )

    try:
        helper.read_json()
        chat_id = user_requests[0].chat.id
        if user_requests[0].text[0] != "/":
            bot.send_message(chat_id, message)
    except Exception:
        pass


bot.set_update_listener(listener)


@bot.message_handler(commands=["help"])
def help(m):

    helper.read_json()
    chat_id = m.chat.id

    message = "Here are the commands you can use: \n"
    commands = helper.getCommands()
    for c in commands:
        message += "/" + c + ", "
    message += "\nUse /menu for detailed instructions about these commands."
    bot.send_message(chat_id, message)


@bot.message_handler(commands=["faq"])
def faq(m):

    helper.read_json()
    chat_id = m.chat.id

    faq_message = (
        '"What does this bot do?"\n'
        ">> DollarBot lets you manage your expenses so you can always stay on top of them! \n\n"
        '"How can I add an epxense?" \n'
        ">> Type /add, then select a category to type the expense. \n\n"
        '"Can I see history of my expenses?" \n'
        ">> Yes! Use /analytics to get a graphical display, or /history to view detailed summary.\n\n"
        '"I added an incorrect expense. How can I edit it?"\n'
        ">> Use /edit command. \n\n"
        '"Can I check if my expenses have exceeded budget?"\n'
        ">> Yes! Use /budget and then select the view category. \n\n"
    )
    bot.send_message(chat_id, faq_message)


# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(m):
    """
    start_and_menu_command(m): Prints out the the main menu displaying the features that the
    bot offers and the corresponding commands to be run from the Telegram UI to use these features.
    Commands used to run this: commands=['start', 'menu']
    """
    helper.read_json()

    chat_id = m.chat.id

    addUserHistory(chat_id)

    text_intro = (
        "Welcome to the Dollar Bot! \n"
        "DollarBot can track all your expenses with simple and easy to use commands :) \n"
        "Here is the complete menu. \n\n"
    )

    commands = helper.getCommands()
    for c in commands:
        # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# defines how the /add command has to be handled/processed
@bot.message_handler(commands=["add"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add.run(message, bot)


@bot.message_handler(commands=["sendEmail"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    sendEmail.run(message, bot)


# defines how the /weekly command has to be handled/processed
@bot.message_handler(commands=["weekly"])
def command_weekly(message):
    """
    command_weekly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls weekly.py to run to execute
    the weekly analysis functionality. Commands used to run this: commands=['weekly']
    """
    new_weekly.run(message, bot)


# defines how the /monthly command has to be handled/processed
@bot.message_handler(commands=["monthly"])
def command_monthly(message):
    """
    command_monthly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls monthly.py to run to execute
    the monthly analysis functionality. Commands used to run this: commands=['monthly']
    """
    new_monthly.run(message, bot)


# defines how the /add command has to be handled/processed
@bot.message_handler(commands=["add_currencies"])
def command_add_currencies(message):

    add_currencies.run(message, bot)


# defines how the /add command has to be handled/processed
@bot.message_handler(commands=["add_balance"])
def command_add_balance(message):

    add_balance.run(message, bot)


# handles pdf command
@bot.message_handler(commands=["pdf"])
def command_pdf(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls pdf.py to run to execute
    the add functionality. Commands used to run this: commands=['pdf']
    """
    pdf.run(message, bot)


# function to fetch expenditure history of the user
@bot.message_handler(commands=["history"])
def command_history(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls history.py to run to execute
    the add functionality. Commands used to run this: commands=['history']
    """
    history.run(message, bot)


# function to edit date, category or cost of a transaction
@bot.message_handler(commands=["edit"])
def command_edit(message):
    """
    command_edit(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls edit.py to run to execute
    the add functionality. Commands used to run this: commands=['edit']
    """
    edit.run(message, bot)


# function to display total expenditure
@bot.message_handler(commands=["display"])
def command_display(message):
    """
    command_display(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls display.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    display.run(message, bot)


# function to estimate future expenditure
@bot.message_handler(commands=["estimate"])
def command_estimate(message):
    estimate.run(message, bot)


# handles "/delete" command
@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
    command_delete(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    delete.run(message, bot)


# handles budget command
@bot.message_handler(commands=["budget"])
def command_budget(message):
    budget.run(message, bot)


# handles analytics command
@bot.message_handler(commands=["analytics"])
def command_analytics(message):
    """
    command_analytics(message): Take an argument message with content and chat ID. Calls analytics to
    run analytics. Commands to run this commands=["analytics"]
    """
    analytics.run(message, bot)


# handles predict command
@bot.message_handler(commands=["predict"])
def command_predict(message):
    """
    command_predict(message): Take an argument message with content and chat ID. Calls predict to
    analyze budget and spending trends and suggest a future budget. Commands to run this commands=["predict"]
    """
    predict.run(message, bot)


# defines how the /insights command has to be handled/processed
@bot.message_handler(commands=["insight"])
def command_insight(message):
    """
    command_insight(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls insight.py to run to execute
    """
    insight.run(message, bot)


@bot.message_handler(commands=["link"])
def handle_set_account(message):
    link.run(message, bot)


@bot.message_handler(commands=["set_account"])
def handle_set_account(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Checking", "Savings")
    msg = bot.reply_to(message, "Choose your account type:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_account_choice)


def process_account_choice(message):
    account_type = message.text
    helper.set_account_type(message, account_type)  # Call the helper function
    bot.send_message(message.chat.id, f"Account type set to {account_type}")


def addUserHistory(chat_id):
    userData = mongoClient.fetch_user_from_telegram(chat_id=chat_id)
    if userData == None:
        mongoClient.create_user_from_telegram(chat_id)
        mongoClient.create_budget_from_telegram(chat_id)


def main():
    """
    main() The entire bot's execution begins here. It allows selecting
    which bot to run based on command line arguments.
    """
    parser = argparse.ArgumentParser(description="Bot runner script")
    parser.add_argument(
        "--bot",
        type=str,
        choices=["telegram", "discord"],
        default="both",
        help="Select which bot to run",
    )[1]

    args = parser.parse_args()

    try:
        if args.bot == "telegram":
            bot.polling(none_stop=True)
        elif args.bot == "discord":
            discordClient.start_bot()

    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == "__main__":
    main()
