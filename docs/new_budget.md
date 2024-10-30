# About DollarBot's new budget limit Feature
This feature enables users to set custom budget limits and receive alerts when they reach specific percentages (80%, 90%, or 100%) of their budget to avoid overspending.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/vegechick510/DollarBot/blob/main/code/budget_limit.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the budget feature. It pop ups a menu on the bot asking the user to choose to add, remove or display a budget, after which control is given to post_operation_selection(message, bot) for further proccessing. It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the main code.py function.

2. post_limit_option_selection(message, bot):
It takes 2 arguments for processing - message
    which is the message from the user, and bot which is the telegram bot object.
    This function takes input from the user, making them choose which operation of budget limit they
    would like to do - add/update, delete the budget limit or exit the operation, and then calls the corresponding functions for further processing.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /budget into the telegram bot, then type /Budget Limit to set your specific budget percent.
