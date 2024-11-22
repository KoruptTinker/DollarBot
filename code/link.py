import helper
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime


def run(message, bot):
    chat_id = message.chat.id

    user = helper.fetchUserFromTelegram(chat_id)
    existing_link_code = helper.fetchLinkCodeFromTelegram(chat_id)

    if user["discord_id"] is not None and user["discord_id"] != 0:
        bot.reply_to(message, "You already have a discord account linked!")
    elif existing_link_code is not None:
        bot.reply_to(message, f"Use the following code on discord to link your account: {existing_link_code["link_code"]}")
    else:
        link_code = helper.generateRandomLinkCode()
        helper.createLinkCodeTelegram(chat_id, link_code)
        bot.reply_to(message, f"Use the following code on discord to link your account: {link_code}")
