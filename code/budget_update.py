"""
File: budget_limit.py
Author: Xianting Lu, Xiang Lan, Xingyue Shi
Date: October 24, 2024
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
    run(message, bot): This is the main function used to implement the budget add/update features.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function.
    """
    helper.read_category_json()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getBudgetTypes()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, "Select Budget Type", reply_markup=markup)
    bot.register_next_step_handler(msg, post_type_selection, bot)


def post_type_selection(message, bot):
    """
    post_type_selection(message, bot): It takes 2 arguments for processing - message
    which is the message from the user, and bot which is the telegram bot object.
    This function takes input from the user, making them choose which type of budget they
    would like to create - category-wise or overall, and then calls the corresponding functions for further processing.
    """
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getBudgetTypes()
        if op not in options.values():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception('Sorry I don\'t recognise this operation "{}"!'.format(op))
        if op == options["category"]:
            update_category_budget(message, bot)
        elif op == options["exit"]:
            pass
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def update_category_budget(message, bot):
    """
    update_category_budget(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object.
    This function is called in case the user decides to choose category-wise budgest in the run or
    post_type_selection stages. It gets the spend categories from the helper module's getSpendCategories
    and displays them to the user. It then passes control on to the post_category_selection function.
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = helper.getSpendCategories()
    markup.row_width = 2
    for c in categories:
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


def post_category_selection(message, bot):
    """
    post_category_selection(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object.
    Based on the category chosen by the user, the bot checks if these are part of the pre-defined
    categories in helper.getSpendCategories(), else it throws an exception. If there is a budget
    already existing for the category, it identifies this case through helper.isCategoryBudgetByCategoryAvailable
    and shares this information with the user. If not, it simply proceeds. In either case, it then asks for the
    new/updated budget amount. It passes control onto post_category_amount_input.
    """
    try:
        chat_id = message.chat.id
        selected_category = message.text
        categories = helper.getSpendCategories()
        if selected_category not in categories:
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognise this category "{}"!'.format(
                    selected_category
                )
            )
        budgetCategories = helper.getCategoryBudget(chat_id)
        if budgetCategories and selected_category in budgetCategories.keys():
            currentBudget = budgetCategories[selected_category]
            msg_string = "Current monthly budget for {} is {}\n\nEnter monthly budget for {}\n(Enter numeric values only)"
            message = bot.send_message(
                chat_id,
                msg_string.format(
                    selected_category, currentBudget, selected_category
                ),
            )
        else:
            message = bot.send_message(
                chat_id,
                "Enter monthly budget for "
                + selected_category
                + "\n(Enter numeric values only)",
            )
        bot.register_next_step_handler(
            message, post_category_amount_input, bot, selected_category
        )
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def post_category_amount_input(message, bot, category):
    """
    post_category_amount_input(message, bot, category): It takes 2 arguments for
    processing - message which is the message from the user, and bot which is the telegram
    bot object, and the category chosen by the user.
    """
    try:
        chat_id = message.chat.id
        amount_value = helper.validate_entered_amount(message.text)
        if amount_value == 0:
            raise Exception("Invalid amount.")
        helper.update_budget(chat_id, category, float(amount_value))
        message = bot.send_message(
            chat_id, "Budget for " + category + " is now: $" + amount_value
        )
        budget_view.display_overall_budget(message, bot)
        post_category_add(message, bot)

    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def post_category_add(message, bot):
    """
    post_category_add(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object.
    This exists in case the user wants to add a category-wise budget to another category after adding
    it for one category. It prompts the user to choose an option from helper.getUpdateOptions().values() and
    passes control to post_option_selection to either continue or exit the add/update feature.
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getUpdateOptions().values()
    markup.row_width = 2
    for c in options:
        markup.add(c)
    msg = bot.reply_to(message, "Select Option", reply_markup=markup)
    bot.register_next_step_handler(msg, post_option_selection, bot)


def post_option_selection(message, bot):
    """
    post_option_selection(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object.
    It takes the category chosen by the user from the message object. If the message is "continue",
    then it runs update_category_budget (above) allowing the user to get into the add/update process again.
    Otherwise, it exits the feature.
    """
    print("here")
    selected_option = message.text
    options = helper.getUpdateOptions()
    if selected_option == options["continue"]:
        update_category_budget(message, bot)
