# Multi-Currency Support

## Overview
The Multi-Currency Support feature allows users to record expenses in multiple currencies, which are automatically converted to a primary currency (USD). This functionality is useful for users who spend in different currencies and want a unified view of their spending in a single currency.

## Feature Details
- **Currency Selection**: Users can choose a currency (e.g., CNY, GBP, EUR, CAD, JPY, USD) when adding an expense.
- **Automatic Conversion**: Each transaction amount is converted to USD, providing a unified spending view.
- **API Integration**: Real-time exchange rates are fetched from an exchange rate API, ensuring up-to-date currency conversion.

## Benefits
- **Accurate Spending Overview**: Users get a consolidated view of their expenses in USD, regardless of the original currency.
- **Convenient for International Spending**: Ideal for users who travel or shop internationally, simplifying budget tracking across currencies.
- **Automatic Updates**: Exchange rates are refreshed with each transaction, offering precise conversions based on current rates.

## Usage Examples
To use Multi-Currency Support in the bot, users can enter commands as follows:

### Adding an Expense in a Specific Currency
Users can add expenses in any supported currency, and they’ll automatically convert to USD.

#### Example: `/add 100 CNY food` `/add 50 GBP travel` `/add 20 EUR groceries` `/add 100 JPY entertainment` 

Each command records the amount in the specified currency and stores the converted amount in USD.

## Implementation
The Multi-Currency Support feature is implemented in `helper.py` and `add.py`. 

### Key Components and Functions

- **Currency Conversion Logic**: The `convert_currency(from_currency, to_currency, amount)` function in `helper.py` interacts with an exchange rate API to convert amounts from any supported currency to USD.
  
- **Expense Entry**: In `add.py`, the `run(message, bot)` and `post_currency_selection()` functions are modified to prompt users for a currency choice and convert the entered amount to USD before saving.

- **Currencies List**: A list of supported currencies is defined in `currencies.txt`, ensuring that the bot only accepts valid currencies.

### Workflow and Logic

1. **Selecting a Currency**:
   - When users add an expense, they’re prompted to choose a currency from the supported list (USD, CNY, GBP, EUR, CAD, JPY).
   
2. **Converting and Recording**:
   - The amount is converted to USD using the real-time rate fetched from the exchange rate API and then saved in USD for unified tracking.

3. **Viewing Converted Amounts**:
   - All expenses are recorded in USD, allowing users to view their spending in a consistent currency format.

## Future Enhancements
- **Customizable Primary Currency**: Allow users to set a primary currency other than USD.
- **Historical Exchange Rates**: Use historical rates for transactions added retroactively, offering a more accurate representation of past spending.
- **Multi-Currency Budgeting**: Enable users to set budgets in different currencies and view conversion-adjusted spending limits.

