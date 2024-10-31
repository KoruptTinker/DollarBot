# Customizable Budget Tracking and Alerts

## Overview
The customizable budget tracking and alerts feature allows users to set specific budgets and receive alerts based on their spending patterns. With this feature, users can define overall and category-specific budgets, monitor spending progress, and receive notifications when they approach or exceed budget limits. This functionality is designed to promote financial control through real-time feedback on expenses.

## Feature Details
- **Customized Budgets**: Users can set budgets at both overall and category levels, such as groceries, utilities, or travel.
- **Real-Time Alerts**: Notifications are triggered as users approach 80%, 90%, or 100% of their set budgets.
- **Spending Analysis**: Detailed insights into each category's spending help users make informed financial adjustments.

## Benefits
- **Enhanced Financial Awareness**: Users gain insights into spending patterns, promoting mindful budgeting.
- **Prevent Overspending**: Real-time alerts help prevent unintentional overspending by providing timely reminders.
- **Customizable Tracking**: Flexible budget categories enable tailored tracking to suit individual spending habits.

## Usage Examples

1. **Set a Budget**  
   - Users can set a budget by entering: `/budget set <amount> <category>`
   - For example, to set a $500 budget for food, users would input: `/budget set 500 food`

2. **Update an Existing Budget**  
   - To modify a budget, users use the command: `/budget update <new_amount> <category>`
   - Example: To increase the food budget to $600: `/budget update 600 food`

3. **Delete a Budget**  
   - To delete a category budget: `/budget delete <category>`
   - Example: To remove the transportation budget: `/budget delete transportation`

4. **View Current Budget**  
   - Users can check their current budget status with: `/budget view <category>`
   - Example: To view the remaining budget for food: `/budget view food`

5. **Receive Alerts**  
   - Users receive notifications as they approach 80%, 90%, and 100% of their set budgets. Alerts are automatically sent through the bot.

6. **Check Remaining Budget**  
   - Users can view remaining balances in each category with: `/budget remaining <category>`
   - Example: `/budget remaining food` to check the balance left for food.

## Implementation

### Key Components and Functions

1. **`budget.py`**  
   - **Purpose**: Manages budget-related operations like adding, updating, and deleting budgets.
   - **Core Functions**:
     - `set_budget(amount, category=None)`: Sets a budget for a specific category or overall.
     - `get_budget(category=None)`: Retrieves the budget of a specified category or overall.
     - `delete_budget(category=None)`: Deletes the budget of a category or overall.

2. **`budget_update.py`**  
   - **Purpose**: Updates budget amounts based on user input.
   - **Core Function**:
     - `update_budget(amount, category=None)`: Adjusts the budget to the specified new amount.

3. **`budget_view.py`**  
   - **Purpose**: Displays current budgets and remaining amounts.
   - **Core Functions**:
     - `display_budget(category=None)`: Shows the current budget for the specified category or overall.
     - `display_remaining_budget(category=None)`: Indicates the remaining amount and percentage for each budget category.

4. **`budget_delete.py`**  
   - **Purpose**: Enables users to remove budgets.
   - **Core Function**:
     - `delete_category_budget(category)`: Clears the specified category budget.

5. **`budget_limit.py`**  
   - **Purpose**: Manages threshold alerts and custom limits.
   - **Core Functions**:
     - `check_limit(category=None)`: Notifies users when they reach 80%, 90%, or 100% of their budget.
     - `send_alert(category, threshold)`: Sends alerts based on the defined threshold percentages.

### Workflow and Logic
1. **Budget Setup**  
   - Users set their initial budgets for specific categories or overall spending limits.

2. **Ongoing Tracking and Notifications**  
   - All expenditures are monitored and matched against the set budgets, with automated alerts sent as thresholds are met.

3. **Real-Time Updates and Views**  
   - Budget progress is updated in real-time, allowing users to view remaining balances and adjust their spending accordingly.

## Future Enhancements
- **Multi-Currency Support**: Allow budgets in different currencies with automatic conversion to a primary currency.
- **Historical Budget Analysis**: Introduce detailed historical views of past budgets and spending patterns.
- **Custom Alert Frequencies**: Enable users to set alert thresholds that best match their preferences, like monthly or bi-weekly reminders.
- **Predictive Budget Recommendations**: Provide AI-driven insights to recommend budget adjustments based on past spending behavior.

