# About DollarBot's /add new Currency Feature 
Track expenses in multiple currencies, with automatic conversion to primary currency(US dollars) for unified reporting.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/vegechick510/DollarBot/blob/main/code/add_currencies.py)

# Code Description
## Functions
1. run(message, bot):
This function initiates the expense tracking process by prompting the user to select a category.

2. post_category_selection(message, bot):
This function handles category selection by the user and prompts them to select a currency.

3. post_currency_selection(message, bot, selected_category):
This function processes the currency selection and asks the user to enter the amount spent.


4. post_amount_input(message, bot, selected_category, selected_currency):
Handles the amount input and performs currency conversion.

5. update_balance(message, amount, bot):
Converts an amount from one currency to another using the ExchangeRate API.

6. add_user_record(chat_id, record_to_be_added):
Updates the user’s account balance after recording an expense.

7. add_user_balance_record(chat_id, record_to_be_added):
Adds a new expense record to the user's data.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /add into the telegram bot, after you select the date, you will be asked to select the currency you want to add, select the currency, it will automatically transfered to US dollars.
