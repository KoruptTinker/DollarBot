


# from discord import app_commands
# import discord
# import helper
# import graphing
# from datetime import datetime
# from tabulate import tabulate
# import os
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# async def display(interaction: discord.Interaction):
#     """
#     Display command handler for Discord bot.
#     Shows spending statistics for current day and month.
#     """
#     try:
#         # Verify user and get details
#         user_details = helper.fetchUserFromDiscord(interaction.user.id)
#         # logger.debug(f"User details: {user_details}")
        
# async def display(interaction: discord.Interaction):
#     try:
#         user_details = helper.fetchUserFromDiscord(interaction.user.id)
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
#         if user_details is None:
#             await interaction.response.send_message(
#                 "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
#             )
#             return

#         chat_id = user_details["telegram_chat_id"]
#         history = helper.getUserHistory(chat_id)
# <<<<<<< HEAD
#         logger.debug(f"User history: {history}")
        
#         if history is None or not history:
#             await interaction.response.send_message(
#                 "No spending records found!"
#             )
#             return

#         # Convert MongoDB documents to string format
#         formatted_history = []
#         for record in history:
#             formatted_record = f"{record['date']},{record['category']},{record['amount']}"
#             formatted_history.append(formatted_record)
#         logger.debug(f"Formatted history: {formatted_history}")

#         # Get current date in YYYY-MM-DD format
#         current_date = datetime.now()
#         day_query = current_date.strftime("%Y-%m-%d")
#         month_query = current_date.strftime("%Y-%m")
        
#         logger.debug(f"Day query: {day_query}")
#         logger.debug(f"Month query: {month_query}")

#         # Filter records for day and month
#         day_records = [value for index, value in enumerate(formatted_history) if str(day_query) in value]
#         month_records = [value for index, value in enumerate(formatted_history) if str(month_query) in value]
        
#         logger.debug(f"Day records: {day_records}")
#         logger.debug(f"Month records: {month_records}")

#         # Calculate spending totals
#         day_total_text, day_total_dict = calculate_spendings(day_records)
#         month_total_text, month_total_dict = calculate_spendings(month_records)
        
#         # logger.debug(f"Day totals: {day_total_dict}")
#         # logger.debug(f"Month totals: {month_total_dict}")
# =======
        
#         if history is None:
#             await interaction.response.send_message(
#                 "Oops! Looks like you do not have any spending records!"
#             )
#             return

#         # Get current day and month data
#         current_date = datetime.now()
#         day_query = current_date.strftime(helper.getDateFormat())
#         month_query = current_date.strftime(helper.getMonthFormat())

#         # Query for daily records
#         day_records = [value for value in history if str(day_query) in value]
#         # Query for monthly records
#         month_records = [value for value in history if str(month_query) in value]

#         # Calculate daily and monthly totals
#         day_total_text, day_total_dict = calculate_spendings(day_records)
#         month_total_text, month_total_dict = calculate_spendings(month_records)
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959

#         # Format response message
#         response = []
        
# <<<<<<< HEAD
#         # Format daily spending table
# =======
#         # Daily spending table
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
#         if day_total_dict:
#             day_table = [["Category", "Amount"]]
#             for category, amount in day_total_dict.items():
#                 day_table.append([str(category), f"$ {amount}"])
#             day_formatted = "**Daily Spending:**\n```\n" + tabulate(day_table, headers="firstrow", tablefmt="grid") + "\n```"
#             response.append(day_formatted)

# <<<<<<< HEAD
#         # Format monthly spending table
# =======
#         # Monthly spending table
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
#         if month_total_dict:
#             month_table = [["Category", "Amount"]]
#             for category, amount in month_total_dict.items():
#                 month_table.append([str(category), f"$ {amount}"])
#             month_formatted = "**Monthly Spending:**\n```\n" + tabulate(month_table, headers="firstrow", tablefmt="grid") + "\n```"
#             response.append(month_formatted)

#         if not response:
# <<<<<<< HEAD
#             await interaction.response.send_message(
#                 "No spending records found for today or this month!"
#             )
# =======
#             await interaction.response.send_message("You have no spending records!")
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
#             return

#         # Send text response
#         await interaction.response.send_message("\n".join(response))

# <<<<<<< HEAD
#         # Generate and send graphs if monthly data exists
#         if month_total_dict:
#             monthly_budget = helper.getCategoryBudget(chat_id)
#             logger.debug(f"Monthly budget: {monthly_budget}")
            
#             photo_paths = graphing.visualize_new(month_total_text, monthly_budget)
#             logger.debug(f"Generated photo paths: {photo_paths}")
            
# =======
#         # Generate and send graphs
#         monthly_budget = helper.getCategoryBudget(chat_id)
#         if month_total_text:
#             photo_paths = graphing.visualize_new(month_total_text, monthly_budget)
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
#             for photo_path in photo_paths:
#                 with open(photo_path, "rb") as photo:
#                     await interaction.followup.send(file=discord.File(photo))
#                 os.remove(photo_path)

#     except Exception as e:
# <<<<<<< HEAD
#         logger.error(f"Error in display command: {str(e)}", exc_info=True)
#         await interaction.response.send_message(f"An error occurred: {str(e)}")

# def calculate_spendings(queryResult):
#     """
#     Calculate total spending amounts by category from query results.
#     Returns formatted text and dictionary of totals.
#     """
#     try:
#         total_dict = {}
        
#         for row in queryResult:
#             s = row.split(",")
#             cat = s[1]
#             if cat in total_dict:
#                 total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
#             else:
#                 total_dict[cat] = float(s[2])
                
#         total_text = ""
#         for key, value in total_dict.items():
#             total_text += f"{key} ${value}\n"
            
#         logger.debug(f"Calculated totals - text: {total_text}, dict: {total_dict}")
#         return total_text, total_dict
        
#     except Exception as e:
#         logger.error(f"Error in calculate_spendings: {str(e)}", exc_info=True)
#         raise

# async def setup(tree: app_commands.CommandTree):
#     """
#     Register the display command with the Discord bot's command tree.
#     """
#     tree.command(name="display", description="View spending statistics for today and this month")(
#         display
#     )
# # """
# # File: display.py
# # Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
# # Date: October 01, 2023
# # Description: File contains Telegram bot message handlers and their associated functions.

# # Copyright (c) 2023

# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:

# # The above copyright notice and this permission notice shall be included in all
# # copies or substantial portions of the Software.

# # THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# # SOFTWARE.
# # """
# # from discord import app_commands
# # import logging
# # import discord
# # import time
# # from tabulate import tabulate
# # import helper
# # import graphing
# # import logging
# # from telebot import types
# # from datetime import datetime
# # import os
# # # === Documentation of display.py ===

# # async def display(interaction: discord.Interaction):
# #     """
# #     Display command handler for Discord bot.
# #     Shows spending statistics for current day and month.
# #     """
# #     try:
# #         # Verify user and get details
# #         user_details = helper.fetchUserFromDiscord(interaction.user.id)
# #         # logger.debug(f"User details: {user_details}")
        
# #         if user_details is None:
# #             await interaction.response.send_message(
# #                 "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
# #             )
# #             return
# #         chat_id = user_details["telegram_chat_id"]
# #         history = helper.getUserHistory(chat_id)
        
# #         if history is None or not history:
# #             await interaction.response.send_message(
# #                 "No spending records found!"
# #             )
# #             return


# # async def run(interaction: discord.Interaction):
# #     """
# #     run(message, bot): This is the main function used to implement the delete feature.
# #     It takes 2 arguments for processing - message which is the message from the user, and bot
# #     which is the telegram bot object from the main code.py function.
# #     """
# #     helper.read_json()
# #     chat_id = user_details["telegram_chat_id"]
# #     history = helper.getUserHistory(chat_id)
# #     if history is None:
# #         await interaction.response.send_message(
# #              "Oops! Looks like you do not have any spending records!"
# #         )
# #     else:
# #         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
# #         markup.row_width = 2
# #         for mode in helper.getSpendDisplayOptions():
# #             markup.add(mode)
# #         msg = bot.reply_to(
# #             message,
# #             "Please select a category to see the total expense",
# #             reply_markup=markup,
# #         )
# #         bot.register_next_step_handler(msg, display_total, bot)

# # async def display_total(message, bot):
# #     """
# #     display_total(message, bot): It takes 2 arguments for processing - message which is
# #     the message from the user, and bot which is the telegram bot object from the
# #     run(message, bot): function in the same file. This function loads the user's data using
# #     the helper file's getUserHistory(chat_id) method. After this, depending on the option user
# #     has chosen on the UI, it calls the calculate_spendings(queryResult): to process the queried
# #     data to return to the user after which it finally passes the data to the UI for the user to view.
# #     """
# #     try:
# #         chat_id = message.chat.id
# #         DayWeekMonth = message.text

# #         if DayWeekMonth not in helper.getSpendDisplayOptions():
# #             raise Exception(
# #                 'Sorry I can\'t show spendings for "{}"!'.format(DayWeekMonth)
# #             )

# #         history = helper.getUserHistory(chat_id)
# #         if history is None:
# #             raise Exception("Oops! Looks like you do not have any spending records!")

# #         await interaction.send_message(chat_id, "Hold on! Calculating...")
# #         # show the bot "typing" (max. 5 secs)
# #         bot.send_chat_action(chat_id, "typing")
# #         time.sleep(0.5)

# #         total_text = ""
# #         if DayWeekMonth == "Day":
# #             query = datetime.now().today().strftime(helper.getDateFormat())
# #             # query all that contains today's date
# #             queryResult = [
# #                 value for index, value in enumerate(history) if str(query) in value
# #             ]
# #         elif DayWeekMonth == "Month":
# #             query = datetime.now().today().strftime(helper.getMonthFormat())
# #             # query all that contains today's date
# #             queryResult = [
# #                 value for index, value in enumerate(history) if str(query) in value
# #             ]
# #         print("this is queryResult: "+queryResult)
# #         total_text, total_dict = calculate_spendings(queryResult)
# #         monthly_budget = helper.getCategoryBudget(chat_id)
# #         print("Print Total Spending", total_text)
# #         print("Print monthly budget", monthly_budget)

# #         spending_text = ""
# #         if len(total_text) == 0:
# #             spending_text = "You have no spendings for {}!".format(DayWeekMonth)
# #             await interaction.response.send_message(chat_id, spending_text)
# #         else:
# #             table = [["Category", "Amount"]]
# #             spending_text = "Here are your total spendings {}".format(
# #                 DayWeekMonth.lower()
# #             )
# #             for category, amount in total_dict.items():
# #                 table.append([str(category), "$ " + str(amount)])
# #             spend_total_str = "<pre>" + tabulate(table, headers="firstrow") + "</pre>"
# #             await interaction.response.send_message(chat_id, spending_text)
# #             bot.send_message(chat_id, spend_total_str, parse_mode="HTML")
# #             photo_paths = graphing.visualize_new(total_text, monthly_budget)
# #             # bot.send_photo(chat_id, photo=open("expenditure.png", "rb"))
# #             for photo_path in photo_paths:
# #                 with open(photo_path, "rb") as photo:
# #                     bot.send_photo(chat_id, photo)
# #                 os.remove(photo_path)
# #     except Exception as e:
# #         logging.exception(str(e))
# #         bot.reply_to(message, str(e))


# # async def calculate_spendings(queryResult):
# #     """
# #     calculate_spendings(queryResult): Takes 1 argument for processing - queryResult
# #     which is the query result from the display total function in the same file.
# #     It parses the query result and turns it into a form suitable for display on the UI by the user.
# #     """
# #     total_dict = {}

# #     for row in queryResult:
# #         # date,cat,money
# #         s = row.split(",")
# #         # cat
# #         cat = s[1]
# #         if cat in total_dict:
# #             # round up to 2 decimal
# #             total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
# #         else:
# #             total_dict[cat] = float(s[2])
# #     total_text = ""
# #     for key, value in total_dict.items():
# #         total_text += str(key) + " $" + str(value) + "\n"
# #     return total_text, total_dict
# =======
#         await interaction.response.send_message(f"Oops! {str(e)}")

# def calculate_spendings(queryResult):
#     total_dict = {}
    
#     for row in queryResult:
#         s = row.split(",")
#         cat = s[1]
#         if cat in total_dict:
#             total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
#         else:
#             total_dict[cat] = float(s[2])
            
#     total_text = ""
#     for key, value in total_dict.items():
#         total_text += f"{key} ${value}\n"
#     return total_text, total_dict

# async def setup(tree: app_commands.CommandTree):
#     tree.command(name="display", description="View spending statistics for today and this month")(
#         display
#     )
# >>>>>>> 8b53a9be140afd57462674dd81775a18df2f6959
