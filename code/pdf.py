"""
File: pdf.py
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

import helper
import logging
from matplotlib import pyplot as plt
from fpdf import FPDF
import graphing
import os

# === Documentation of pdf.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the pdf save feature.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        msg = "Alright. Creating a pdf of your expense history!"
        bot.send_message(chat_id, msg)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        top = 0.8
        if len(user_history) == 0:
            plt.text(
                0.1,
                top,
                "No record found!",
                horizontalalignment="left",
                verticalalignment="center",
                transform=ax.transAxes,
                fontsize=20,
            )

        if helper.isOverallBudgetAvailable(chat_id):
            category_budget = helper.getCategoryBudget(chat_id)
            graphing.overall_split(category_budget)

            category_spend = {}
            for spend in user_history:
                category_spend[spend["category"]] = (
                    category_spend.get(spend["category"], 0) + spend["amount"]
                )
            if category_spend != {}:
                graphing.spend_wise_split(category_spend)

            if user_history:
                cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)
                graphing.time_series(cat_spend_dict)

            list_of_images = ["overall_split.png", "spend_wise.png", "time_series.png"]
            pdf = FPDF()
            pdf.add_page()
            x_coord = 20
            y_coord = 30
            for image in list_of_images:
                pdf.image(image, x=x_coord, y=y_coord, w=70, h=50)
                x_coord += 80
                if x_coord > 100:
                    x_coord = 20
                    y_coord += 60
            pdf.output("expense_report.pdf", "F")
            bot.send_document(chat_id, open("expense_report.pdf", "rb"))
            for image in list_of_images:
                os.remove(image)
        else:
            bot.send_message(
                chat_id,
                "Oh no! Set your corresponding category wise budgets using the /budget command to generate the expense report",
            )

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))
