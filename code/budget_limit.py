"""
File: budget_limit.py
Author: Xianting Lu, Xiang Lan, Xingyue Shi
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import helper
import logging
import budget_view
from telebot import types

# === Documentation of budget_update.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the budget limit features.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function.
    """
    helper.read_category_json()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getBudgetLimitOptions()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, "Set Budget Limit Alert", reply_markup=markup)
    bot.register_next_step_handler(msg, post_limit_option_selection, bot)

def post_limit_option_selection(message, bot):
    """
    post_limit_option_selection(message, bot): It takes 2 arguments for processing - message
    which is the message from the user, and bot which is the telegram bot object.
    This function takes input from the user, making them choose which operation of budget limit they
    would like to do - add/update, delete the budget limit or exit the operation, and then calls the corresponding functions for further processing.
    """
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getBudgetLimitOptions()
        if op not in options.values():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception('Sorry I don\'t recognise this operation "{}"!'.format(op))
        if op == options["updatelim"]:
            update_budget_limit(chat_id, bot)
        elif op == options["dellim"]:
            delete_budget_limit(chat_id, bot)
        elif op == options["exit"]:
            return
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def update_budget_limit(chat_id, bot):
    """
    update_budget_limit(message, bot): It takes 2 arguments for processing - message which is the
    message from the user, and bot which is the telegram bot object. This function is called when the
    user wants to either create a new budget limit alert or update an existing one. It checks if there is an
    existing budget limit through the helper module's isBudgetLimitAvailable function and if so, displays this
    along with the prompt for the new (to be updated) budget limit, or just asks for the new budget limit. It passes control
    to the post_budget_limit_input function in the same file.
    """
    if helper.isBudgetLimitAvailable(chat_id):
        currentBudget = helper.getBudgetLimit(chat_id)
        msg_string = "Current Budget Limit Alert is {}% \n\nHow much is your new monthly budget limit alert? \n(Enter numeric values only)"
        message = bot.send_message(chat_id, msg_string.format(currentBudget))
    else:
        msg_string = "How much is your new monthly budget limit alert? \n(Enter numeric values only)"
        message = bot.send_message(chat_id, msg_string)
    bot.register_next_step_handler(message, post_budget_limit_input, bot)

def post_budget_limit_input(message, bot):
    """
    post_budget_limit_input(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object.
    This function is called when the user has entered the new budget limit alert value and write 
    it into the json file.
    """
    try:
        chat_id = message.chat.id
        amount_value = helper.validate_entered_amount(message.text)
        if amount_value == 0:
            raise Exception("Invalid amount.")
        user_list = helper.read_json()
        if str(chat_id) not in user_list:
            user_list[str(chat_id)] = helper.createNewUserRecord()
        user_list[str(chat_id)]["budget"]["limit"] = amount_value
        helper.write_json(user_list)
        bot.send_message(chat_id, f"Budget Limit Alert Updated to {amount_value}%!")
        print(user_list)
        return user_list
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def delete_budget_limit(chat_id, bot):
    user_list = helper.read_json()
    print(user_list)
    if str(chat_id) in user_list:
        user_list[str(chat_id)]["budget"]["limit"] = str(0)
        helper.write_json(user_list)
    bot.send_message(chat_id, "Budget Limit deleted!")
    return

