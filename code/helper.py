"""
File: helper.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
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

import re
import json
import os
from datetime import datetime
from mongo import MongoDB
from config import Secrets
import random


secrets = Secrets()
mongoClient = MongoDB(secrets.MongoConnectionURL, secrets.DBName)

spend_categories = []
choices = ["Date", "Category", "Cost"]
spend_display_option = ["Day", "Month"]
spend_estimate_option = ["Next day", "Next month"]
update_options = {"continue": "Continue", "exit": "Exit"}
budget_options = {
    "update": "Add/Update",
    "view": "View",
    "delete": "Delete",
    "exit": "Exit",
}
budget_types = {
    "category": "Category-Wise Budget",
    "exit": "Exit",
}
data_format = {"data": [], "budget": {"overall": "0", "category": None, "limit": None}}
analytics_options = {
    "overall": "Overall budget split by Category",
    "spend": "Split of current month expenditure",
    "remaining": "Remaining value",
    "history": "Time series graph of spend history",
}

# set of implemented commands and their description
commands = {
    "menu": "Display commands with their descriptions.",
    "help": "Display the list of commands.",
    "pdf": "Provides expense history as PDF. It contains the following expense charts - \
       \n 1. Budget split - total budget and budget for various categories as a pie chart \
       \n 2. Category wise spend split - Distribution of expenses for each category as a pie chart \
       \n 3. Category wise budget command - Split of used and remaining percentage of the budget amount for every category  \
       \n 4. Time series of the expense - Time Vs Expense in $",
    "add": " Option to add expenses including currency and category. \
       \n 1. It will give you the list of categories to choose from. \
       \n 2. You will be prompted to enter the amount corresponding to your spending \
       \n 3.The message will be prompted to notify the addition of your expense with the amount,date, time and category ",
    "add_recurring": "This option is to add a recurring expense for future months",
    "analytics": "This option gives user a graphical representation of their expenditures \
        \n You will get an option to choose the type of data you want to see.",
    "predict": "This option analyzes your recorded spendings and gives you a budget that will accommodate for them.",
    "history": "This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spendings",
    "delete": "This option is to Clear/Erase specific records or all your records based on your Choice",
    "display": "This option is to display your records for the current month or for the current day as per the user's choice.",
    "edit": "This option helps you to go back and correct/update the missing details \
        \n 1. It will give you the list of your expenses you wish to edit \
        \n 2. It will let you change the specific field based on your requirements like amount/date/category",
    "budget": "This option is to set/update/delete the budget. \
        \n 1. The Add/update category is to set the new budget or update the existing budget \
        \n 2. The view category gives the detail if budget is exceeding or in limit with the difference amount \
        \n 3. The delete category allows to delete the budget and start afresh! \
        \n 4. The Budget Limit option is to set/update/delete the limit for the budget alert",
    "updateCategory": "This option is to add/delete/edit the categories. \
        \n 1. The Add Category option is to add a new category which dosen't already exist \
        \n 2. The Delete Category option is to delete an existing category \
        \n 3. The Edit Category option is to edit an existing category. ",
    "weekly": "This option is to get the weekly analysis report of the expenditure",
    "monthly": "This option is to get the monthly analysis report of the expenditure",
    "insight": "This option is to get the insights of the expenditure",
    "sendEmail": "Send an email with an attachment showing your history",
}

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"


# === Documentation of helper.py ===


# function to load .json expense record data
def read_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("expense_record.json"):
            with open("expense_record.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("expense_record.json").st_size != 0:
            with open("expense_record.json", encoding="utf-8") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(user_list):
    """
    write_json(user_list): Stores data into the datastore of the bot.
    """
    try:
        with open("expense_record.json", "w", encoding="utf-8") as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def fetchUserFromTelegram(chat_id):
    return mongoClient.fetch_user_from_telegram(chat_id)


def fetchLinkCodeFromTelegram(chat_id):
    return mongoClient.fetch_link_code_from_telegram(chat_id)


def linkDiscordToTelegram(chat_id, discord_id):
    return mongoClient.link_discord_to_telegram(chat_id, discord_id)


def fetchLinkCodeFromDiscord(discord_id):
    return mongoClient.fetch_link_code_from_discord(discord_id)


def createLinkCodeTelegram(chat_id, link_code):
    return mongoClient.create_link_code_from_telegram(chat_id, link_code)


def createLinkCodeDiscord(discord_id, link_code):
    return mongoClient.create_link_code_from_discord(discord_id, link_code)


def deleteLinkCode(link_code):
    return mongoClient.delete_link_code(link_code)


def fetchLinkCode(link_code):
    return mongoClient.fetch_link_code(link_code)


def generateRandomLinkCode():
    return str(random.randint(100000, 999999))


def read_category_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("categories.json"):
            with open("categories.json", "w", encoding="utf-8") as json_file:
                json_file.write(
                    '{ "categories" : "Food,Groceries,Utilities,Transport,Shopping,Miscellaneous" }'
                )
            return json.dumps('{ "categories" : "" }')
        elif os.stat("categories.json").st_size != 0:
            with open("categories.json", encoding="utf-8") as category_record:
                category_record_data = json.load(category_record)
            return category_record_data

    except FileNotFoundError:
        print("---------NO CATEGORIES FOUND---------")


def write_category_json(category_list):
    """
    write_json(category_list): Stores data into the datastore of the bot.
    """
    try:
        with open("categories.json", "w", encoding="utf-8") as json_file:
            json.dump(category_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def validate_entered_amount(amount_entered):
    """
    validate_entered_amount(amount_entered): Takes 1 argument, amount_entered.
    It validates this amount's format to see if it has been correctly entered by the user.
    """
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match(
        "^[1-9][0-9]{0,14}$", amount_entered
    ):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0


def validate_entered_duration(duration_entered):
    if duration_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}", duration_entered):
        duration = int(duration_entered)
        if duration > 0:
            return str(duration)
    return 0


def update_budget(chat_id: str = "", category: str = "", amount: float = 0):
    return mongoClient.update_budget_from_telegram(chat_id, category, amount)


def getUserHistory(chat_id):
    """
    getUserHistory(chat_id): Takes 1 argument chat_id and uses this to get the relevant user's historical data.
    """
    return mongoClient.fetch_spends_from_telegram(chat_id)


def updateUserSpend(spend_id, date=None, category=None, amount=None):
    if date:
        return mongoClient.update_spend_date_from_telegram(spend_id, date)
    elif category:
        return mongoClient.update_spend_category_from_telegram(spend_id, category)
    elif amount:
        return mongoClient.update_spend_amount_from_telegram(spend_id, amount)
    else:
        return False


def getUserHistoryByCategory(chat_id, category):
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if f",{category}," in record:
            previous_expenses.append(record)
    return previous_expenses


def getUserHistoryByDate(chat_id, date):
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if date == record["date"]:
            previous_expenses.append(record)
    return previous_expenses


def getUserHistoryDateExpense(chat_id):
    data = getUserHistory(chat_id)
    cat_spend_dict = {}
    for record in data:
        cat_spend_dict[record["date"]] = record["amount"]
    return cat_spend_dict


def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if str(chat_id) in user_list:
        return user_list[str(chat_id)]
    return None


def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, "Oh no! " + str(e))


def createNewUserRecord():
    return data_format


def getOverallBudget(chatId):
    data = mongoClient.fetch_budget_from_telegram(chatId)
    if data is None or data == {}:
        return 0

    overall = 0
    for cat in dict(data["category"]).keys():
        overall += int(data["category"][cat])

    return overall


def getCategoryBudget(chatId):
    data = mongoClient.fetch_budget_from_telegram(chatId)
    if data is None:
        return None
    return data["category"]


def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]


def resetBudget(chat_id):
    return mongoClient.reset_budget_from_telegram(chat_id)


def canAddBudget(chatId):
    overall_budget = getOverallBudget(chatId)
    category_budget = getCategoryBudget(chatId)
    return (overall_budget is None and overall_budget != "0") and (
        category_budget is None and category_budget != {}
    )


def getBudgetLimit(chatId):
    data = getUserData(chatId)
    if data is None or data == {}:
        return None
    return data["budget"]["limit"]


def isOverallBudgetAvailable(chatId):
    overall_budget = getOverallBudget(chatId)
    if overall_budget is not None and overall_budget != "0":
        return True
    return False


def isCategoryBudgetAvailable(chatId):
    category_budget = getCategoryBudget(chatId)
    if category_budget is not None and category_budget != {}:
        return True
    return False


def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None or data == {} or data == "0":
        return False
    return cat in data.keys()


def isCategoryBudgetByCategoryNotZero(chatId):
    for cat in spend_categories:
        if getCategoryBudgetByCategory(chatId, cat) == "0":
            return False
    return True


def isBudgetLimitAvailable(chatId):
    budget_limit = getBudgetLimit(chatId)
    if budget_limit is not None and budget_limit != "0":
        return True
    return False


def get_uncategorized_amount(chatId, amount):
    overall_budget = float(amount)
    category_budget_data = getCategoryBudget(chatId)
    if category_budget_data is None or category_budget_data == {}:
        return amount
    category_budget = 0
    for c in category_budget_data.values():
        category_budget += float(c)
    uncategorized_budget = overall_budget - category_budget
    return str(round(uncategorized_budget, 2))


def display_remaining_budget(message, bot):
    display_remaining_overall_budget(message, bot)


def display_remaining_overall_budget(message, bot):
    chat_id = message.chat.id
    budget, remaining_budget = calculateRemainingOverallBudget(chat_id)
    if budget == None or budget == 0:
        msg = "No budget set. Please set a budget if it is needed."
    else:
        budget_limit = float(80)
        if remaining_budget / budget > 1 - budget_limit / 100:
            msg = "The Overall Monthly Budget is ${:.2f}. \nRemaining Overall Monthly Budget is ${:.2f}".format(
                budget, remaining_budget
            )
        elif (
            remaining_budget / budget <= 1 - budget_limit / 100
        ) and budget_limit != 0:
            msg = "The Overall Monthly Budget is ${:.2f}. \nTotal spending has reached {:.2%} of the budget, exceeding the {:.2%} limit. Please monitor your spending.".format(
                budget, 1 - remaining_budget / budget, budget_limit / 100
            )
        else:
            msg = "The Overall Monthly Budget is ${}. \nBudget Exceded!\nExpenditure exceeds the budget by ${}".format(
                budget, str(remaining_budget)[1:]
            )
    bot.send_message(chat_id, msg)


def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime("%Y-%m")
    queryResult = [value for _, value in enumerate(history) if query in value["date"]]
    if budget == 0:
        return None, -calculate_total_spendings(queryResult)
    return float(budget), float(budget) - calculate_total_spendings(queryResult)


def calculate_total_spendings(queryResult):
    total = 0
    for row in queryResult:
        total = total + float(row["amount"])
    return total


def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)


def calculateRemainingCategoryBudgetPercent(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    if budget == "0":
        print("budget is zero")
        return None
    return (
        calculate_total_spendings_for_category(queryResult, cat) / float(budget)
    ) * 100


def calculate_total_spendings_for_category(queryResult, cat):
    total = 0
    for row in queryResult:
        s = row.split(",")
        if cat == s[1]:
            total = total + float(s[2])
    return total


def calculate_total_spendings_for_category_chat_id(chat_id, cat):
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    print(query)
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    return calculate_total_spendings_for_category(queryResult, cat)


def updateBudgetCategory(chatId, category):
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"][category] = str(0)
    write_json(user_list)


def deleteBudgetCategory(chatId, category):
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"].pop(category, None)
    write_json(user_list)


def getAvailableCategories(history):
    available_categories = set()
    for record in history:
        available_categories.add(record["category"])
    return available_categories


def getCategoryWiseSpendings(available_categories, history):
    category_wise_history = {}
    for cat in available_categories:
        for record in history:
            if cat == record["category"]:
                if cat in category_wise_history.keys():
                    category_wise_history[cat].append(record)
                else:
                    category_wise_history[cat] = [record]
    return category_wise_history


def erase_spend_history(chat_id: str = ""):
    return mongoClient.reset_spends_from_telegram(chat_id)


def delete_spend_history(chat_id: str = "", date: str = ""):
    return mongoClient.delete_spends_from_telegram(chat_id, date)


def getFormattedPredictions(category_predictions):
    category_budgets = ""
    for key, value in category_predictions.items():
        if type(value) == float:
            category_budgets += str(key) + ": $" + str(value) + "\n"
        else:
            category_budgets += str(key) + ": " + value + "\n"
    predicted_budget = "Here are your predicted budgets"
    predicted_budget += " for the next month \n"
    predicted_budget += category_budgets
    return predicted_budget


def getSpendCategories():
    """
    getSpendCategories(): This functions returns the spend categories used in the bot. These are defined the same file.
    """
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(",")
    spend_cat = [category.strip() for category in spend_cat if category.strip()]

    return spend_cat


def deleteSpendCategories(category):
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(",")
    spend_cat.remove(category)

    result = ",".join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)


def addSpendCategories(category):
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(",")
    spend_cat.append(category)
    spend_cat = [category.strip() for category in spend_cat if category.strip()]
    result = ",".join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)


def getSpendDisplayOptions():
    """
    getSpendDisplayOptions(): This functions returns the spend display options used in the bot. These are defined the same file.
    """
    return spend_display_option


def getSpendEstimateOptions():
    return spend_estimate_option


def getCommands():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return commands


def getDateFormat():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return dateFormat


def getTimeFormat():
    """
    def getTimeFormat(): This functions returns the time format used in the bot.
    """
    return timeFormat


def getMonthFormat():
    """
    def getMonthFormat(): This functions returns the month format used in the bot.
    """
    return monthFormat


def getChoices():
    return choices


def getBudgetOptions():
    return budget_options


def getBudgetTypes():
    return budget_types


def getBudgetLimitOptions():
    return budget_limit_options


def getUpdateOptions():
    return update_options


def getAnalyticsOptions():
    return analytics_options


# === Multi-Currency Support ===


def getCurrencies():
    """
    Retrieves a list of supported currencies from 'currencies.txt' for multi-currency expense tracking.
    """
    try:
        with open("currencies.txt", "r") as tf:
            currencies = tf.read().split(",")
        return [currency.strip() for currency in currencies if currency.strip()]
    except FileNotFoundError:
        print("Currency list file not found.")
        return []


def convert_currency(from_currency, to_currency, amount):
    """
    Convert amount from one currency to another using a currency conversion API.
    """
    if amount <= 0:
        return None

    import requests

    api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        rates = response.json().get("rates")
        rate = rates.get(to_currency)
        return round(amount * rate, 2) if rate else None
    except requests.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None


# === Data migration in json file ===
def migrate_users():
    user_list = read_json()  # Load existing user data

    for chat_id, user_data in user_list.items():
        # Remove 'account', 'balance', 'balance_data', and 'reminder' keys if they exist
        user_data.pop("account", None)
        user_data.pop("balance", None)
        user_data.pop("balance_data", None)
        user_data.pop("reminder", None)

        # Clean 'data' entries by removing records with "Checking Account" or "Saving Account"
        if "data" in user_data:
            user_data["data"] = [
                record
                for record in user_data["data"]
                if "Checking Account" not in record and "Saving Account" not in record
            ]

    write_json(user_list)  # Save the updated data


def migrate_data_entries():
    user_list = read_json()  # Load existing user data

    for chat_id, user_data in user_list.items():
        if "data" in user_data:
            updated_data = []
            for record in user_data["data"]:
                # Use regex to separate date, time, category, and amount
                match = re.match(
                    r"(\d{2}-\w{3}-\d{4})(?: \d{2}:\d{2})?,([A-Za-z]+),(\d+(\.\d+)?)",
                    record,
                )
                if match:
                    # Keep only date, category, and amount
                    date, category, amount = (
                        match.groups()[0],
                        match.groups()[1],
                        match.groups()[2],
                    )
                    updated_record = f"{date},{category},{amount}"
                    updated_data.append(updated_record)
                else:
                    updated_data.append(
                        record
                    )  # Leave as-is if the format is unrecognized

            user_data["data"] = updated_data  # Replace with updated data list

    write_json(user_list)  # Save the modified data
