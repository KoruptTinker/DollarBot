# Customizable Budget Tracking and Alerts

## Feature Overview

The customizable budget tracking and alerts feature allows users to set specific budgets and receive alerts tailored to their spending patterns. Users can set overall and category-specific budgets, track spending progress, and receive notifications as they approach budget limits. This functionality is designed to help users maintain financial control by receiving real-time feedback on their expenses relative to set budgets.

---

## Goals

- **Customized Budgets:** Allow users to define budgets at various levels, including overall and category-specific (e.g., groceries, utilities).
- **Real-Time Alerts:** Notify users when they approach critical thresholds (80%, 90%, and 100%) of their budgets.
- **Insightful Analysis:** Provide visual breakdowns and detailed analysis of spending in each category, helping users adjust their financial goals.

---

## Implementation

### Key Components

- **Budget Tracking**: Implements budget settings for overall and specific categories.
- **Threshold Alerts**: Alerts users at customizable intervals to notify them of their budget usage.
- **Budget Analysis**: Offers insights into spending habits via visual summaries and recommendations.

### Files and Functions

#### 1. **`budget.py`**
   - **Description**: Main budget management functions for adding, updating, viewing, and deleting budgets.
   - **Primary Functions**:
     - `set_budget(amount, category=None)`: Sets a new budget amount for either the overall or specific category.
     - `get_budget(category=None)`: Retrieves the current budget for the specified category or the overall budget.
     - `delete_budget(category=None)`: Deletes a specified category budget or the overall budget.
  
#### 2. **`budget_update.py`**
   - **Description**: Handles updating existing budgets based on user input.
   - **Primary Functions**:
     - `update_budget(amount, category=None)`: Updates the budget to a new specified amount for the category or overall.

#### 3. **`budget_view.py`**
   - **Description**: Provides users with a view of their current budgets.
   - **Primary Functions**:
     - `display_budget(category=None)`: Shows the budget for a specified category or the overall budget.
     - `display_remaining_budget(category=None)`: Displays the remaining budget and percentage left for each category.

#### 4. **`budget_delete.py`**
   - **Description**: Enables budget deletion to start fresh or remove specific budgets.
   - **Primary Functions**:
     - `delete_category_budget(category)`: Deletes a specific category budget, clearing out the data.

#### 5. **`budget_limit.py`**
   - **Description**: Controls alert triggers and custom limits.
   - **Primary Functions**:
     - `check_limit(category=None)`: Checks the budget limit and notifies the user if 80%, 90%, or 100% of the budget has been reached.
     - `send_alert(category, threshold)`: Sends alerts based on defined threshold percentages.

---

### Workflow and Logic

1. **Setting Budgets**: 
   - Users can set budgets at the start, either for specific categories (e.g., groceries, transportation) or as an overall budget.

2. **Tracking and Notifications**:
   - Spending is tracked against each set budget, updating automatically with new transactions.
   - Threshold alerts are triggered as users approach their budget limits, with 80%, 90%, and 100% warnings.

3. **View and Analysis**:
   - Budgets and their remaining amounts are displayed through `budget_view.py`.
   - Spending trends and remaining budget per category are visually summarized, allowing users to adjust spending or reset budgets as needed.

---

### Example Usage

- **Set a Budget**: Users can set a monthly budget for food by calling `set_budget(500, category="food")`. 
- **Update Budget**: If a user wants to increase the food budget to $600, they can call `update_budget(600, category="food")`.
- **Delete Budget**: To remove the set budget for transportation, use `delete_category_budget("transportation")`.
- **Check Limits**: As users spend within a category, `check_limit()` automatically sends alerts if they hit specified thresholds.
  
---

## Conclusion

The Customizable Budget Tracking and Alerts feature provides users with flexible budget management and personalized alerts, supporting better financial management through real-time monitoring and visual insights. By implementing customizable alerts, users can manage their budgets effectively and make data-driven decisions for improved financial health.
