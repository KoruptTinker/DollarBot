"""
File: insight.py
Author: Xiang Lan, Xingyue Shi, Xianting Lu
Date: October 20, 2024
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2024

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
from tabulate import tabulate
from datetime import datetime, timedelta
from collections import defaultdict


def run(message, bot):
    """
    Implements both transaction history and spending insights feature with time-sorted history and enhanced insights.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        table = [["Date", "Category", "Amount"]]

        if user_history is None or len(user_history) == 0:
            raise Exception("Sorry! No spending records found!")

        # Store spending data for analysis
        monthly_spend = defaultdict(
            lambda: defaultdict(float)
        )  # Stores spend per month per category
        day_spend = defaultdict(float)  # Stores total spend per day of the week
        transaction_data = []

        for rec in user_history:
            date_str = rec["date"]
            category = rec["category"]
            amount = rec["amount"]
            amount = float(amount)

            # Parse the date
            date_time = datetime.strptime(date_str, "%Y-%m-%d")
            transaction_data.append((date_time, date_str, category, amount))

            # Calculate month for comparison
            month_year = date_time.strftime("%b-%Y")
            monthly_spend[month_year][category] += amount

            # Calculate day of the week (0=Monday, 6=Sunday)
            day_of_week = date_time.weekday()
            day_spend[day_of_week] += amount

        # Sort transaction data by date
        transaction_data.sort(key=lambda x: x[0])

        # Prepare table of sorted transactions
        for date_time, date_str, category, amount in transaction_data:
            table.append([date_str, category, "$ " + str(amount)])

        # Send sorted transaction history
        spend_total_str = "<pre>" + tabulate(table, headers="firstrow") + "</pre>"
        bot.send_message(chat_id, spend_total_str, parse_mode="HTML")

        # Check if there are at least two months of data
        if len(monthly_spend) < 2:
            raise Exception(
                "Not enough data to generate spending insights! At least two months of data are required."
            )

        # Provide enhanced spending insights if there is enough data
        insights = generate_insights(monthly_spend, day_spend)
        bot.send_message(chat_id, insights, parse_mode="HTML")

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))


def generate_insights(monthly_spend, day_spend):
    """
    Generates enhanced spending insights based on the user's transaction data, including multi-month trends and averages.
    """
    insights = "<b>Personalized Spending Insights</b>\n\n"

    # 1. Check weekend vs weekday spending
    weekend_spend = day_spend[5] + day_spend[6]  # Saturday and Sunday
    weekday_spend = sum(day_spend[i] for i in range(5))  # Monday to Friday

    if weekend_spend > weekday_spend:
        insights += f"🔸 You tend to spend more on weekends. Weekend spending: ${weekend_spend:.2f}\n"
    else:
        insights += (
            f"🔸 You spend more on weekdays. Weekday spending: ${weekday_spend:.2f}\n"
        )

    # 2. Multi-month comparison for each category
    months = sorted(monthly_spend.keys(), key=lambda x: datetime.strptime(x, "%b-%Y"))

    # Iterate through the last few months (if available)
    for i in range(1, len(months)):
        current_month = months[i]
        previous_month = months[i - 1]

        insights += (
            f"\n<b>Comparison between {current_month} and {previous_month}:</b>\n"
        )

        for category in monthly_spend[current_month]:
            current_month_spend = monthly_spend[current_month].get(category, 0)
            previous_month_spend = monthly_spend[previous_month].get(category, 0)

            if previous_month_spend > 0:
                percentage_change = (
                    (current_month_spend - previous_month_spend) / previous_month_spend
                ) * 100
                if percentage_change > 0:
                    insights += f"🔸 You spent {percentage_change:.2f}% more on {category} in {current_month} compared to {previous_month}.\n"
                else:
                    insights += f"🔸 You spent {abs(percentage_change):.2f}% less on {category} in {current_month} compared to {previous_month}.\n"

    # 3. Monthly average spending
    total_spend_per_month = {
        month: sum(monthly_spend[month].values()) for month in monthly_spend
    }
    avg_monthly_spend = sum(total_spend_per_month.values()) / len(total_spend_per_month)

    insights += f"\n🔸 Your average monthly spending is ${avg_monthly_spend:.2f}.\n"

    # 4. Category-wise analysis for the most recent month
    most_recent_month = months[-1]
    total_spent_recent = total_spend_per_month[most_recent_month]

    insights += f"\n<b>Spending in {most_recent_month} by category:</b>\n"
    for category, amount in monthly_spend[most_recent_month].items():
        percentage_of_total = (amount / total_spent_recent) * 100
        insights += f"🔸 {category}: ${amount:.2f} ({percentage_of_total:.2f}% of total spending)\n"

    return insights
