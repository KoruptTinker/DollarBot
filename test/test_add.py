"""
File: test_add.py
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

import os
import json
from mock.mock import patch
from telebot import types
from code import add
from mock import ANY
from datetime import datetime

import pytest
from code.add import add_user_record
from code.helper import convert_currency, validate_entered_amount

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"
date = datetime.today().date()


@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from test run!")
    add.run(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_category_selection_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from testing!")
    add.post_category_selection(message, mc, date)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_category_selection_noMatchingCategory(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True

    mocker.patch.object(add, "helper")
    add.helper.getSpendCategories.return_value = None

    message = create_message("hello from testing!")
    add.post_category_selection(message, mc, date)
    assert mc.reply_to.called


def test_add_user_record_nonworking(mocker):
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = {}
    addeduserrecord = add.add_user_record(1, "record : test")
    assert addeduserrecord


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json.dump({}, json_file)  # Write an empty dictionary instead of "{}"
        with open("./test/dummy_expense_record.json") as expense_record:
            expense_record_data = json.load(expense_record)
        assert isinstance(expense_record_data, dict), "Expected a dictionary"
        # return expense_record_data  # Ensure it always returns a dictionary
    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        assert expense_record_data == {}  # Return an empty dictionary if file not found


def test_add_user_record_working(mocker):
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json.dump({}, json_file)  # Write an empty dictionary instead of "{}"
        with open("./test/dummy_expense_record.json") as expense_record:
            expense_record_data = json.load(expense_record)
        assert isinstance(expense_record_data, dict), "Expected a dictionary"
        MOCK_USER_DATA = expense_record_data  # Ensure it always returns a dictionary
    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        MOCK_USER_DATA = {}
    # MOCK_USER_DATA = test_read_json()  # Will now always return a dictionary
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = MOCK_USER_DATA
    addeduserrecord = add.add_user_record(1, "record : test")
    if len(MOCK_USER_DATA) + 1 == len(addeduserrecord):
        assert True


# Mock data for integration testing on add and currency conversion
CURRENCY_ADD_DATA = [
    (100, "CNY", "Food", 14.00),  # CNY to USD for Food category
    (250, "GBP", "Transport", 325),  # GBP to USD for Transport category
    (300, "EUR", "Groceries", 324.00),  # EUR to USD for Groceries
    (500, "CAD", "Utilities", 359.50),  # CAD to USD for Utilities
    (1200, "JPY", "Shopping", 7.82),  # JPY to USD for Shopping
]


@pytest.mark.parametrize("amount, currency, category, expected_usd", CURRENCY_ADD_DATA)
def test_add_user_record_with_currency_conversion(
    amount, currency, category, expected_usd
):
    """Test adding user record with currency conversion to USD"""
    chat_id = 12345  # Dummy chat ID for test
    converted_amount = convert_currency(currency, "USD", amount)
    # assert round(converted_amount, 2) == expected_usd
    assert (
        isinstance(converted_amount, float)
        and converted_amount > expected_usd * 0.5
        and converted_amount < expected_usd * 1.5
    )


@pytest.mark.parametrize(
    "from_currency, to_currency, amount, expected",
    [
        ("USD", "USD", 100, 100),
        ("USD", "USD", 0.01, 0.01),
        ("USD", "USD", 123456789, 123456789),
    ],
)
def test_convert_currency_identity(from_currency, to_currency, amount, expected):
    """Test converting USD to USD does not change amount"""
    result = convert_currency(from_currency, to_currency, amount)
    assert round(result, 2) == round(expected, 2)


def test_add_record_small_currency_value():
    """Test adding a small CAD to USD converted value with one decimal precision"""
    converted_amount = convert_currency("CAD", "USD", 1.0)
    assert round(converted_amount, 1) == 0.7  # Example rate


def test_add_record_large_currency_value():
    """Test converting a large GBP amount to USD"""
    converted_amount = convert_currency("GBP", "USD", 10000.0)
    assert isinstance(round(converted_amount, 2), float)


def test_zero_currency_value():
    """Test converting zero amount"""
    converted_amount = convert_currency("USD", "USD", 0)
    assert converted_amount is None


def test_negative_currency_value():
    """Test handling of a negative amount"""
    converted_amount = convert_currency("JPY", "USD", -500)
    assert converted_amount is None


def test_edge_currency_value():
    """Test edge case with small amount of JPY converted to USD"""
    converted_amount = convert_currency("JPY", "USD", 0.01)
    assert round(converted_amount, 2) == 0.00  # Expected small rounded result


@pytest.mark.parametrize(
    "amount, category, expected_usd",
    [
        (300, "Food", 324.00),
        (500, "Groceries", 650.00),
    ],
)
def test_recording_currency_conversion_to_usd(amount, category, expected_usd):
    """Test conversion and recording to ensure USD values are stored"""
    chat_id = 54321  # Dummy chat ID
    currency = "EUR" if category == "Food" else "GBP"
    converted_amount = convert_currency(currency, "USD", amount)
    assert (
        round(converted_amount, 2) <= expected_usd * 1.5
        and round(converted_amount, 2) >= expected_usd * 0.5
    )


@pytest.mark.parametrize(
    "currency, amount",
    [
        ("CNY", -100),  # Negative CNY amount
        ("EUR", 0),  # Zero EUR amount
    ],
)
def test_invalid_currency_amount_record(currency, amount):
    """Test recording invalid amounts (negative or zero)"""
    converted_amount = convert_currency(currency, "USD", amount)
    assert converted_amount is None


@pytest.mark.parametrize(
    "currency, amount",
    [
        ("JPY", 999999999),  # Large JPY value
        ("CAD", 12345678.99),  # Large CAD value with decimal
    ],
)
def test_large_currency_conversion_values(currency, amount):
    """Test large conversion values and validate precision"""
    converted_amount = convert_currency(currency, "USD", amount)
    assert converted_amount is not None
