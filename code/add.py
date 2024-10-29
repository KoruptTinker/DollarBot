import helper
import logging
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime
import requests

option = {}

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

def run(message, bot):
    """
    run(message, bot): Starts the add feature by prompting the user for a date selection.
    """
    helper.display_remaining_budget(message, bot)
    helper.read_json()
    helper.read_category_json()
    chat_id = message.chat.id
    message = bot.send_message(chat_id, "Select date")
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(chat_id, f"Select {LSTEP[step]}", reply_markup=calendar)

    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal(c):
        chat_id = c.message.chat.id
        result, key, step = DetailedTelegramCalendar().process(c.data)

        if not result and key:
            bot.edit_message_text(
                f"Select {LSTEP[step]}",
                chat_id,
                c.message.message_id,
                reply_markup=key,
            )
        elif result:
            data = datetime.today().date()
            if result > data:
                bot.send_message(chat_id, "Cannot select future dates. Please try /add again with a valid date.")
            else:
                category_selection(message, bot, result)

def category_selection(msg, bot, date):
    """
    Prompts the user to select an expense category, then proceeds to currency selection.
    """
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        categories = helper.getSpendCategories()
        if not categories:
            bot.reply_to(msg, "You don't have any categories. Please add a category!")
        else:
            for c in categories:
                markup.add(c)
            msg = bot.reply_to(msg, "Select Category", reply_markup=markup)
            bot.register_next_step_handler(msg, post_category_selection, bot, date)
    except Exception as e:
        print(e)

def post_category_selection(message, bot, date):
    """
    Handles category selection and prompts the user to select a currency.
    """
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category == "Add new category":
            message1 = bot.send_message(chat_id, "Please enter your category")
            bot.register_next_step_handler(message1, post_append_spend, bot)
            return
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove())
            raise Exception(f'Sorry, I don\'t recognize this category "{selected_category}"!')

        option[chat_id] = selected_category
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getCurrencies():
            markup.add(c)
        msg = bot.reply_to(message, "Select Currency", reply_markup=markup)
        bot.register_next_step_handler(msg, post_currency_selection, bot, selected_category, date)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
        display_text = "\n".join(f"/{c}: {desc}" for c, desc in helper.getCommands().items())
        bot.send_message(chat_id, "Please select a menu option from below:")
        bot.send_message(chat_id, display_text)

def post_currency_selection(message, bot, selected_category, date):
    """
    Handles currency selection and prompts the user for the expense amount.
    """
    chat_id = message.chat.id
    selected_currency = message.text

    if selected_currency not in helper.getCurrencies():
        bot.send_message(chat_id, 'Invalid currency', reply_markup=types.ReplyKeyboardRemove())
        return

    msg = bot.send_message(chat_id, f'How much did you spend on {selected_category}? (Numeric values only)')
    bot.register_next_step_handler(msg, post_amount_input, bot, selected_category, selected_currency, date)

def post_amount_input(message, bot, selected_category, selected_currency, date):
    """
    Validates and converts the amount, records the entry, and provides a success message.
    """
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)

        # Convert to USD
        converted_amount = convert_currency(selected_currency, 'USD', float(amount_value))
        if converted_amount is None:
            bot.send_message(chat_id, "Error converting currency. Please try again.")
            return

        amount_value = str(round(converted_amount, 2))
        if float(amount_value) == 0:
            raise Exception("Spent amount has to be a non-zero number.")

        date_str, category_str, amount_str = date.strftime(helper.getDateFormat()), str(option[chat_id]), str(amount_value)
        helper.write_json(add_user_record(chat_id, f"{date_str},{category_str},{amount_str}"))
        bot.send_message(chat_id, f'The following expenditure has been recorded: You have spent ${amount_str} for {category_str} on {date_str}')

        helper.display_remaining_budget(message, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))

def add_user_record(chat_id, record_to_be_added):
    """
    Adds an expense record to the user's data in the JSON file.
    """
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()
    user_list[str(chat_id)]["data"].append(record_to_be_added)
    return user_list
