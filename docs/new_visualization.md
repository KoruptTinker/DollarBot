# About DollarBot's new Visualization Feature
Improve the basic graphing features by adding more types of charts (like bar charts or pie charts) and allowing users to filter data by category or time.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/vegechick510/DollarBot/blob/main/code/new_monthly.py) also [here](https://github.com/vegechick510/DollarBot/blob/main/code/new_weekly.py)

# Code Description
## Functions

1. run(message, bot):
   Initiates the monthly analysis feature by retrieving user data and generating charts.
2. create_chart_for_monthly_analysis(user_history, userid):
   Generates all monthly charts based on user transaction history.
3. create_original_monthly_chart(df, userid):
   Generates a line chart of total monthly expenses over time.
4. create_category_monthly_chart(df, userid)
   Creates a line chart of monthly expenses by category.
5. create_monthly_bar_chart(df, userid)
   Generates a bar chart for monthly expenses, grouped by year.
6.create_category_pie_chart(df, userid)
   Creates a pie chart to visualize the spending distribution by category.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), you can use /weekly, /monthly to get more visualizaiton graphs compared with previous version.
