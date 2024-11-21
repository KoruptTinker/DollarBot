"""
File: test_helper.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

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

from code import helper
from code.helper import isCategoryBudgetByCategoryAvailable, throw_exception
from mock import ANY
from telebot import types
from mock.mock import patch
import logging
import mock
import pytest
from code.helper import convert_currency, getCurrencies, validate_entered_amount


MOCK_CHAT_ID = 894127939
MOCK_USER_DATA = {
    str(MOCK_CHAT_ID): {
        "data": ["correct_mock_value"],
        "budget": {"overall": None, "category": None},
    },
    "102": {
        "data": ["wrong_mock_value"],
        "budget": {"overall": None, "category": None},
    },
}
MOCK_CATEGORY_DATA = {
    "categories": "Food,Groceries,Utilities,Transport,Shopping,Miscellaneous"
}


def test_validate_entered_amount_none():
    result = helper.validate_entered_amount(None)
    if result:
        assert False, "None is not a valid amount"
    else:
        assert True


def test_validate_entered_amount_int():
    val = "101"
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + " is valid amount"


def test_validate_entered_amount_int_max():
    val = "999999999999999"
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + " is valid amount"


def test_validate_entered_amount_int_outofbound():
    val = "9999999999999999"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount(out of bound)"
    else:
        assert True


def test_validate_entered_amount_float():
    val = "101.11"
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + " is valid amount"


def test_validate_entered_amount_float_max():
    val = "999999999999999.9999"
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + " is valid amount"


def test_validate_entered_amount_float_more_decimal():
    val = "9999999999.999999999"
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + " is valid amount"


def test_validate_entered_amount_float_outofbound():
    val = "9999999999999999.99"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount(out of bound)"
    else:
        assert True


def test_validate_entered_amount_string():
    val = "agagahaaaa"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount"
    else:
        assert True


def test_validate_entered_amount_string_with_dot():
    val = "agaga.aaa"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount"
    else:
        assert True


def test_validate_entered_amount_special_char():
    val = "$%@*@.@*"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount"
    else:
        assert True


def test_validate_entered_amount_alpha_num():
    val = "22e62a"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount"
    else:
        assert True


def test_validate_entered_amount_mixed():
    val = "a14&^%.hs827"
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + " is not a valid amount"
    else:
        assert True


def test_getUserHistory_without_data(mocker):
    mocker.patch.object(helper, "read_json")
    helper.read_json.return_value = {}
    result = helper.getUserHistory(MOCK_CHAT_ID)
    if len(result) == 0:
        assert True
    else:
        assert False, "Result is not None when user data does not exist"


def test_getUserHistory_with_data(mocker):
    mocker.patch.object(helper, "read_json")
    helper.read_json.return_value = MOCK_USER_DATA
    result = helper.getUserHistory(7687448400)
    if len(result) == 1:
        assert True
    else:
        assert False, "User data is available but not found"


def test_getSpendCategories(mocker):
    mocker.patch.object(helper, "read_category_json")
    helper.read_category_json.return_value = MOCK_CATEGORY_DATA
    result = helper.getSpendCategories()
    if result == MOCK_CATEGORY_DATA["categories"].split(","):
        assert True
    else:
        assert False, "expected spend categories are not returned"


def test_getSpendDisplayOptions():
    result = helper.getSpendDisplayOptions()
    if result == helper.spend_display_option:
        assert True
    else:
        assert False, "expected spend display options are not returned"


def test_getCommands():
    result = helper.getCommands()
    if result == helper.commands:
        assert True
    else:
        assert False, "expected commands are not returned"


def test_getDateFormat():
    result = helper.getDateFormat()
    if result == helper.dateFormat:
        assert True
    else:
        assert False, "expected date format are not returned"


def test_getTimeFormat():
    result = helper.getTimeFormat()
    if result == helper.timeFormat:
        assert True
    else:
        assert False, "expected time format are not returned"


def test_getMonthFormat():
    result = helper.getMonthFormat()
    if result == helper.monthFormat:
        assert True
    else:
        assert False, "expected month format are not returned"


def test_getChoices():
    result = helper.getChoices()
    if result == helper.choices:
        assert True
    else:
        assert False, "expected choices are not returned"


def test_write_json(mocker):
    mocker.patch.object(helper, "json")
    helper.json.dump.return_value = True
    user_list = ["hello"]
    helper.write_json(user_list)
    helper.json.dump.assert_called_with(user_list, ANY, ensure_ascii=ANY, indent=ANY)


@patch("telebot.telebot")
def test_throw_exception(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    message = create_message("message from testing")

    throw_exception("hello, exception from testing", message, mc, logging)
    mc.reply_to.assert_called_with(message, "Oh no! hello, exception from testing")


def test_createNewUserRecord():
    data_format_call = helper.createNewUserRecord()
    data_format = {"data": [], "budget": {"overall": None, "category": None}}
    assert sorted(data_format_call) == sorted(data_format)


def test_getOverallBudget_none_case():
    helper.getUserData.return_value = None
    overall_budget = helper.getOverallBudget(11)
    assert overall_budget is 0


def test_getOverallBudget_working_case():
    overall_budget = helper.getOverallBudget(7687448401)
    assert overall_budget == 0


def test_getCategoryBudget_working_case():
    cat_data = {"Food": 10.0, "Utilities": 20.0}
    overall_budget = helper.getCategoryBudget(7687448400)
    assert overall_budget.keys() == cat_data.keys()


def test_getCategoryBudgetByCategory_none_case():
    helper.isCategoryBudgetByCategoryAvailable = mock.Mock(return_value=False)
    testresult = helper.getCategoryBudgetByCategory(10, "Food")
    assert testresult is None


def test_getCategoryBudgetByCategory_normal_case():
    helper.isCategoryBudgetByCategoryAvailable = mock.Mock(return_value=True)
    helper.getCategoryBudget = mock.Mock(return_value={"Food": 10})
    testresult = helper.getCategoryBudgetByCategory(10, "Food")
    assert testresult is not None


def test_canAddBudget():
    helper.getOverallBudget = mock.Mock(return_value=None)
    helper.getCategoryBudget = mock.Mock(return_value=None)
    testresult = helper.canAddBudget(10)
    assert testresult


def test_canAddBudget():
    helper.getOverallBudget = mock.Mock(return_value=None)
    helper.getCategoryBudget = mock.Mock(return_value=None)
    testresult = helper.canAddBudget(10)
    assert testresult


def test_getBudgetLimit_no_data():
    helper.getUserData = mock.Mock(return_value={"budget": {"limit": None}})
    budget_limit = helper.getBudgetLimit(11)
    assert budget_limit is None


def test_getBudgetLimit():
    helper.getUserData = mock.Mock(return_value={"budget": {"limit": "10"}})
    budget_limit = helper.getBudgetLimit(11)
    assert budget_limit == "10"


def test_isOverallBudgetAvailable():
    helper.getOverallBudget = mock.Mock(return_value=True)
    testresult = helper.isOverallBudgetAvailable(10)
    assert testresult is True


def test_isCategoryBudgetAvailable():
    helper.getCategoryBudget = mock.Mock(return_value=True)
    testresult = helper.isCategoryBudgetAvailable(10)
    assert testresult is True


def test_isCategoryBudgetByCategoryAvailable_working():
    helper.getCategoryBudget = mock.Mock(return_value={"Food": 10})
    testresult = isCategoryBudgetByCategoryAvailable(10, "Food")
    assert testresult


def test_isCategoryBudgetByCategoryAvailable_none_case():
    helper.getCategoryBudget = mock.Mock(return_value=None)
    testresult = isCategoryBudgetByCategoryAvailable(10, "Food")
    assert testresult is False


def test_isBudgetLimitAvailable():
    helper.getBudgetLimit = mock.Mock(return_value=10)
    testresult = helper.isBudgetLimitAvailable(10)
    assert testresult is True


def test_isBudgetLimitAvailable_none():
    helper.getBudgetLimit = mock.Mock(return_value=None)
    testresult = helper.isBudgetLimitAvailable(10)
    assert testresult is False


def test_isBudgetLimitAvailable_zero():
    helper.getBudgetLimit = mock.Mock(return_value="0")
    testresult = helper.isBudgetLimitAvailable(10)
    assert testresult is False


def test_calculate_total_spendings():
    pass


def test_calculate_total_spendings_for_category():
    pass


def test_calculateRemainingOverallBudget():
    pass


@patch("telebot.telebot")
def test_display_remaining_overall_budget_not_set(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    helper.calculateRemainingOverallBudget = mock.Mock(return_value=(0, 0))
    message = create_message("hello from testing")
    helper.display_remaining_overall_budget(message, mc)

    mc.send_message.assert_called_with(
        11, "No budget set. Please set a budget if it is needed."
    )


def test_getBudgetTypes():
    testresult = helper.getBudgetTypes()
    localBudgetTypes = {
        "category": "Category-Wise Budget",
        "exit": "Exit",
    }
    assert sorted(testresult) == sorted(localBudgetTypes)


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")


# Mocked conversion data for tests
CURRENCY_TO_USD_DATA = [
    ("USD", "USD", 100, 100),  # Convert 100 USD to USD (should be the same)
    ("CNY", "USD", 100, 14.0),  # Example conversion of 100 CNY to USD
    ("GBP", "USD", 100, 130),  # Example conversion of 100 GBP to USD
    ("EUR", "USD", 100, 108),  # Example conversion of 100 EUR to USD
    ("CAD", "USD", 100, 71.9),  # Example conversion of 100 CAD to USD
    ("JPY", "USD", 1000, 6.52),  # Example conversion of 1000 JPY to USD
]


@pytest.mark.parametrize(
    "from_currency, to_currency, amount, expected", CURRENCY_TO_USD_DATA
)
def test_convert_currency_to_usd(from_currency, to_currency, amount, expected):
    """Test conversion from specified currencies to USD."""
    result = convert_currency(from_currency, to_currency, amount)
    assert result > expected * 0.5 and result < expected * 1.5


def test_getCurrencies():
    """Test that getCurrencies returns a list of available currencies including all specified ones."""
    currencies = getCurrencies()
    assert set(["USD", "CNY", "GBP", "EUR", "CAD", "JPY"]).issubset(currencies)


@pytest.mark.parametrize(
    "amount, currency, expected",
    [("100", "USD", "100.0"), ("200", "CNY", "200.0"), ("50", "GBP", "50.0")],
)
def test_valid_multi_currency_amount(amount, currency, expected):
    """Test various valid currency amounts with expected decimal formatting"""
    assert validate_entered_amount(amount) == expected


def test_valid_multi_currency_amount_values():
    assert helper.convert_currency("USD", "USD", 100) == 100
    assert round(helper.convert_currency("CNY", "USD", 200), 0) > 0


def test_invalid_currency_conversion():
    """Test conversion when invalid currency is provided"""
    result = convert_currency("INVALID", "USD", 100)
    assert result is None


@pytest.mark.parametrize(
    "from_currency, to_currency, amount",
    [
        ("USD", "USD", -50),  # Negative amount
        ("EUR", "USD", 0),  # Zero amount
    ],
)
def test_convert_currency_invalid_amounts(from_currency, to_currency, amount):
    """Test currency conversion with zero and negative amounts"""
    assert convert_currency(from_currency, to_currency, amount) is None


@pytest.mark.parametrize(
    "from_currency, to_currency, amount, expected",
    [
        ("CNY", "USD", 0.01, 0.00157),  # Tiny CNY amount to USD
        ("JPY", "USD", 500000, 3260.0),  # Large JPY amount to USD
        ("GBP", "USD", 10000.76, 13000.99),  # Large GBP with decimal
    ],
)
def test_edge_case_currency_conversion(from_currency, to_currency, amount, expected):
    """Test conversion with boundary and high-precision cases"""
    result = convert_currency(from_currency, to_currency, amount)
    if result == 0:
        assert result == round(expected, 2)
    else:
        assert result > round(expected, 2) * 0.5 and result < round(expected, 2) * 1.5
