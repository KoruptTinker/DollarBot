# About DollarBot's budget_limit module
The budget_limit module contains all the functions required to implement the add/update/detele feature. In essence, all operations involved in addition/updating of a new budget limit for alert and deleting an existing budget limit are taken care of in this module and are implemented here. 

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/KoruptTinker/DollarBot/blob/main/code/budget_limit.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the budget limit features. It takes 2 arguments for processing - message which is the **message** from the user, and **bot** which is the telegram bot object from the main code.py function.



2. post_limit_option_selection(message, bot): 
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object. This function takes input from the user, making them choose which operation of budget limit they would like to do - add/update, delete the budget limit or exit the operation, and then calls the corresponding functions for further processing.

3. update_budget_limit(message, bot): 
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object. This function is called when the user wants to either create a new budget limit alert or update an existing one. It checks if there is an existing budget limit through the helper module's isBudgetLimitAvailable function and if so, displays this along with the prompt for the new (to be updated) budget limit, or just asks for the new budget limit. It passes control to the post_budget_limit_input function in the same file.
   
   
4. post_budget_limit_input(message, bot): It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object. This function is called when the user has entered the new budget limit alert value and write it into the json file.

5.delete_budget_limit(message, bot):
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object. It gets the user's chat ID from the message object, and reads all user data through the read_json method from the helper module. It then proceeds to empty the budget limit data for the particular user based on the user ID provided from the UI. It returns a simple message indicating that this operation has been done to the UI.
