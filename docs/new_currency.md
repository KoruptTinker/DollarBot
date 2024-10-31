# Multi-Currency Support

## Overview
The Multi-Currency Support feature in DollarBot allows users to log expenses in various currencies and automatically converts each expense to a primary currency, USD by default. This enables users to consolidate expenses from different currencies without needing to perform manual conversions, making DollarBot effective for users who travel or frequently transact in foreign currencies.

## Feature Details
### Supported Currencies
- Users can log expenses in the following currencies: **USD, CNY, GBP, EUR, CAD, and JPY**. These supported currencies are listed in `currencies.txt`, which makes it easy to add more currencies by adding additional currency codes to this file.

### Automatic Conversion
- DollarBot fetches real-time exchange rates through an external API, ensuring that each transaction reflects the most current market rates.
- Conversion to USD occurs at the time an expense is logged, making it seamless for the user while maintaining accurate tracking.
- The converted USD amount is saved along with the expense record, providing a single-currency view of spending across all transactions.

### User Interface Changes
- When logging an expense, users can now select the currency for that specific transaction.
- After selecting a currency and entering an amount, DollarBot handles the conversion in the background, showing the final transaction in USD to the user.

## Implementation
### Data Handling
- **helper.py**: This file contains key functions, such as `convert_currency()`, which validates currency input and performs the conversion to USD using the API’s exchange rates.
- **add.py**: Handles user interactions, prompting users to select a currency and amount. It then calls `convert_currency()` from `helper.py` to process the transaction and save it in USD.

### Currency Rates File
- **currencies.txt**: Lists all supported currencies (USD, CNY, GBP, EUR, CAD, and JPY). This file ensures valid currency entries, enabling the bot to recognize and process only supported currencies.

## Usage Example
1. The user selects an expense amount and currency, such as **50 GBP**.
2. DollarBot uses `convert_currency()` to retrieve the latest exchange rate for GBP to USD.
3. The transaction is converted and stored in USD, with a confirmation displaying both the original and converted amounts for transparency.

## Benefits
- **Simplified Tracking**: Users can manage multi-currency expenses without manual conversion, consolidating all expenses into a primary currency.
- **Real-Time Accuracy**: The use of live exchange rates ensures that all expenses are recorded accurately, reflecting currency market fluctuations.
- **User-Friendly**: DollarBot automatically converts expenses and provides a unified USD view, sparing users from managing complex conversions.

## Future Enhancements
- Additional currencies can easily be added to `currencies.txt`.
- Providing a configurable primary currency option so users can choose a currency other than USD as their default for expense tracking.
