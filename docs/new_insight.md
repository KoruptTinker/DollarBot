# About MyDollarBot's new Spending Insights Feature
The Spending Insights feature provides users with personalized insights and trends based on their transaction history. It helps users better understand their spending patterns through comparisons, averages, and breakdowns by time and category. 

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/vegechick510/DollarBot/blob/main/code/insight.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function that gathers the user’s transaction history and sends a sorted summary to the chat. If the data contains at least two months of transactions, it generates personalized spending insights for the user.

2. generate_insights(monthly_spend, day_spend)
his function analyzes the transaction data to provide spending insights, including:
Weekend vs. Weekday Spending: Identifies whether the user spends more on weekends or weekdays.

Multi-Month Category Comparisons: Highlights percentage changes in spending across categories between consecutive months.

Monthly Average Spending: Displays the average monthly spending based on the user's data.

Category Breakdown for Recent Month: Provides a detailed breakdown of the most recent month’s spending by category.



# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /insight into the telegram bot
