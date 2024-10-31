import helper
import logging
from telebot import types
from datetime import datetime

option = {}

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


def post_category_selection(message, bot):
    chat_id = message.chat.id
    selected_category = message.text

    # Check for "Add new category" option
    if selected_category == "Add new category":
        message1 = bot.send_message(chat_id, "Please enter your category")
        bot.register_next_step_handler(message1, post_append_spend, bot)
        return

    # Confirm the category is valid
    if selected_category not in helper.getSpendCategories():
        bot.send_message(chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove())
        raise Exception(
            f'Sorry, I don\'t recognise this category "{selected_category}"!'
        )

    # Store the category and proceed to currency selection
    option[chat_id] = selected_category
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for c in helper.getCurrencies():
        markup.add(c)
    msg = bot.reply_to(message, "Select Currency", reply_markup=markup)
    bot.register_next_step_handler(msg, post_currency_selection, bot, selected_category)


def post_currency_selection(message, bot, selected_category):
    chat_id = message.chat.id
    selected_currency = message.text

    # Validate currency selection
    if selected_currency not in helper.getCurrencies():
        bot.send_message(
            chat_id, "Invalid currency", reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # Ask for amount spent in the selected currency
    msg = bot.send_message(
        chat_id, f"How much did you spend on {selected_category}? (Numeric values only)"
    )
    bot.register_next_step_handler(
        msg, post_amount_input, bot, selected_category, selected_currency
    )


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It pop ups a menu on the bot asking the user to choose their expense category,
    after which control is given to post_category_selection(message, bot) for further proccessing.
    It takes 2 arguments for processing - message which is the message from the user,
    and bot which is the telegram bot object from the main code.py function.
    """
    helper.read_json()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    chat_id = message.chat.id
    expense_history = helper.getUserHistory(chat_id)
    if expense_history:
        recur_msg = bot.send_message(
            chat_id,
            "You have previously recorded expenses. Do you want to repeat one of these expenses?(Y/N)",
        )
        bot.register_next_step_handler(recur_msg, record_expense, bot, expense_history)
    else:
        for c in helper.getSpendCategories():
            markup.add(c)
        markup.add("Add new category")
        msg = bot.reply_to(message, "Select Category", reply_markup=markup)
        bot.register_next_step_handler(msg, post_category_selection, bot)


def post_append_spend(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category not in allocated_categories.keys():
        helper.updateBudgetCategory(chat_id, selected_category)
    helper.spend_categories.insert(0, selected_category)
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


def record_expense(message, bot, previous_expenses):
    print("In function to record expense")
    selection = message.text
    print(selection)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    if selection == "Y" or selection == "y":
        for record in previous_expenses:
            markup.add(record)
        msg = bot.reply_to(
            message, "Select the expense you want to repeat", reply_markup=markup
        )
        bot.register_next_step_handler(msg, post_expense_selection, bot)
    else:
        for c in helper.getSpendCategories():
            markup.add(c)
        markup.add("Add new category")
        msg = bot.reply_to(message, "Select Category", reply_markup=markup)
        bot.register_next_step_handler(msg, post_category_selection, bot)


def post_expense_selection(message, bot):
    chat_id = message.chat.id
    expense_record = message.text
    expense_data = expense_record.split(",")
    amount = expense_data[2]
    category = expense_data[1]
    print(amount)
    amount_value = helper.validate_entered_amount(amount)  # validate
    try:
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")
        date_of_entry = datetime.today().strftime(helper.getDateFormat())
        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(category),
            str(amount_value),
        )
        helper.write_json(
            add_user_record(
                chat_id, "{},{},{}".format(date_str, category_str, amount_str)
            )
        )
        bot.send_message(
            chat_id,
            "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                amount_str, category_str, date_str
            ),
        )
        helper.display_remaining_budget(message, bot, category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no. " + str(e))


def post_amount_input(message, bot, selected_category, selected_currency):
    chat_id = message.chat.id
    amount_entered = message.text
    amount_value = helper.validate_entered_amount(amount_entered)

    # Convert amount to USD
    converted_amount = convert_currency(selected_currency, "USD", float(amount_value))
    if converted_amount is None:
        bot.send_message(chat_id, "Error converting currency. Please try again.")
        return

    amount_value = str(round(converted_amount, 2))
    if float(amount_value) == 0:
        raise Exception("Spent amount has to be a non-zero number.")

    # Record expenditure
    date_of_entry = datetime.today().strftime(
        helper.getDateFormat() + " " + helper.getTimeFormat()
    )
    date_str, category_str, amount_str = (
        str(date_of_entry),
        str(option[chat_id]),
        str(amount_value),
    )
    helper.write_json(
        add_user_record(chat_id, f"{date_str},{category_str},{amount_str}")
    )
    bot.send_message(
        chat_id,
        f"The following expenditure has been recorded: You have spent ${amount_str} for {category_str} on {date_str}",
    )

    helper.display_remaining_budget(message, bot, selected_category)


def add_user_record(chat_id, record_to_be_added):
    """
    add_user_record(chat_id, record_to_be_added): Takes 2 arguments -
    chat_id or the chat_id of the user's chat, and record_to_be_added which
    is the expense record to be added to the store. It then stores this expense record in the store.
    """
    user_list = helper.read_json()
    print("!" * 5)
    print("before")
    print(user_list)
    print("!" * 5)
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]["data"].append(record_to_be_added)
    print("!" * 5)
    print("after")
    print(user_list)
    print("!" * 5)
    return user_list
