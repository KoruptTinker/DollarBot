"""

MIT License

Copyright (c) 2021 Dev Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import helper
import logging
from telebot import types
from datetime import datetime
from forex_python.converter import CurrencyRates
import pytest
import requests


def convert_currency(from_currency, to_currency, amount):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(api_url)
    if response.ok:
        rates = response.json().get("rates")
        rate = rates.get(to_currency)
        return amount * rate
    else:
        print("Error fetching exchange rate.")
        return None


option = {}
currencies = CurrencyRates(force_decimal=False)


# Main run function
def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    print("Categories:")
    for c in helper.getSpendCategories():
        print("\t", c)
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


# Contains step to run after the category is selected
def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognize this category "{}"!'.format(selected_category)
            )

        option[chat_id] = selected_category
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        print("Currencies:")
        for c in helper.getCurrencies():
            print("\t", c)
            markup.add(c)
        msg = bot.reply_to(message, "Select Currency", reply_markup=markup)
        bot.register_next_step_handler(
            msg, post_currency_selection, bot, selected_category
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
        display_text = ""
        commands = helper.getCommands()
        for (
            c
        ) in (
            commands
        ):  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, "Please select a menu option from below:")
        bot.send_message(chat_id, display_text)


# Contains step to run after the currency is selected
def post_currency_selection(message, bot, selected_category):
    try:
        chat_id = message.chat.id
        selected_currency = message.text
        if selected_currency not in helper.getCurrencies():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognize this currency "{}"!'.format(selected_currency)
            )

        message = bot.send_message(
            chat_id,
            "How much did you spend on {}? \n(Enter numeric values only)".format(
                str(option[chat_id])
            ),
        )
        bot.register_next_step_handler(
            message, post_amount_input, bot, selected_category, selected_currency
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
        display_text = ""
        commands = helper.getCommands()
        for (
            c
        ) in (
            commands
        ):  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, "Please select a menu option from below:")
        bot.send_message(chat_id, display_text)


def post_amount_input(message, bot, selected_category, selected_currency):
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate

        # Convert currency with error handling
        converted_amount = convert_currency(
            selected_currency, "USD", float(amount_value)
        )
        if converted_amount is None:
            bot.send_message(chat_id, "Error converting currency. Please try again.")
            return

        amount_value = str(round(float(converted_amount), 2))
        if float(amount_value) == 0:
            raise Exception("Spent amount has to be a non-zero number.")

        # Rest of your code unchanged
        date_of_entry = datetime.today().strftime(
            helper.getDateFormat() + " " + helper.getTimeFormat()
        )
        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(option[chat_id]),
            str(amount_value),
        )
        bot.send_message(
            chat_id,
            "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                amount_str, category_str, date_str
            ),
        )

        helper.display_remaining_budget(message, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no. " + str(e))


# By default, we will use checkings account.
# Only if there was a previous configuration of account change to savings, we will use that.
# def is_Valid_expense(message, amount, bot):
#     acc_type = helper.get_account_type(message, bot)

#     if (float(helper.get_account_balance(message, "", acc_type)) < amount):
#         return False
#     else:
#         return True


def update_balance(message, amount, bot):
    cur_balance = float(
        helper.get_account_balance(
            message, bot, cat=helper.get_account_type(message, bot)
        )
    )
    cur_balance -= float(amount)

    acc_type = helper.get_account_type(message, bot)

    user_list = helper.read_json()
    user_list[str(message.chat.id)]["balance"][acc_type] = str(cur_balance)
    return user_list


# Contains step to on user record addition
def add_user_record(chat_id, record_to_be_added):
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]["data"].append(record_to_be_added)
    return user_list


def add_user_balance_record(chat_id, record_to_be_added):
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]["balance_data"].append(record_to_be_added)
    return user_list
