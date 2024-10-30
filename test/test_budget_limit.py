"""
File: test_budget_limit.py
Author: Xianting Lu, Xiang Lan, Xingyue Shi
Date: October 28, 2024
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

import mock
from mock.mock import patch
from telebot import types
from code import budget_limit

def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from test run!")
    budget_limit.run(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_delete_budget_limit_user_not_in_list(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.read_json.return_value = {}

    message = create_message("hello from testing")
    
    budget_limit.delete_budget_limit(message, mc)

    mc.send_message.assert_called_with(11, "Chat ID not found in user list!")


@patch("telebot.telebot")
def test_delete_budget_limit_user_in_list(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.send_message.write_json = True

    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.read_json.return_value = {"11":{"budget": {"limit": "10"}}}

    message = create_message("hello from testing")
    
    budget_limit.delete_budget_limit(message, mc)

    mc.send_message.assert_called_with(11, "Budget Limit deleted!")


@patch("telebot.telebot")
def test_run_set_budget_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value

    # Mock helper function responses
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }
    
    message = create_message("Set Budget Limit")
    budget_limit.run(message, mc)

    assert mc.reply_to.called
    mc.reply_to.assert_called_with(message, "Set Budget Limit Alert", reply_markup=mock.ANY)


@patch("telebot.telebot")
def test_post_limit_option_selection_update_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }

    budget_limit.update_budget_limit = mock.Mock(return_value=True)
    message = create_message("Update Budget Limit")
    budget_limit.post_limit_option_selection(message, mc)

    assert budget_limit.update_budget_limit.called

@patch("telebot.telebot")
def test_post_limit_option_selection_delete_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }

    budget_limit.delete_budget_limit = mock.Mock(return_value=True)
    message = create_message("Delete Budget Limit")
    budget_limit.post_limit_option_selection(message, mc)

    assert budget_limit.delete_budget_limit.called

@patch("telebot.telebot")
def test_post_limit_option_selection_invalid_option(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }
    budget_limit.helper.throw_exception.return_value = True

    message = create_message("Invalid Option")
    budget_limit.post_limit_option_selection(message, mc)

    assert mc.send_message.called
    assert budget_limit.helper.throw_exception.called

@patch("telebot.telebot")
def test_post_budget_limit_input(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 15
    budget_limit.helper.read_json.return_value = {}
    budget_limit.helper.createNewUserRecord.return_value = {"budget": {"limit": 0}}
    budget_limit.helper.write_json = mock.Mock()

    message = create_message("15")
    user_list = budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.write_json.called
    assert user_list["11"]["budget"]["limit"] == 15
    mc.send_message.assert_called_with(11, "Budget Limit Alert Updated to 15%!")


@patch("telebot.telebot")
def test_post_limit_option_selection_exit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }

    message = create_message("Exit")
    result = budget_limit.post_limit_option_selection(message, mc)

    assert result is None
    assert not mc.send_message.called


@patch("telebot.telebot")
def test_update_budget_limit_with_existing_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.isBudgetLimitAvailable.return_value = True
    budget_limit.helper.getBudgetLimit.return_value = "20"

    budget_limit.update_budget_limit = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    budget_limit.run(message, mc)

    assert budget_limit.update_budget_limit


@patch("telebot.telebot")
def test_update_budget_limit_without_existing_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.isBudgetLimitAvailable.return_value = False
    
    mc.send_message = mock.Mock(return_value=True)

    message = create_message("hello from testing")
    budget_limit.run(message, mc)

    assert budget_limit.update_budget_limit


@patch("telebot.telebot")
def test_post_budget_limit_input_invalid_amount(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 0
    budget_limit.helper.throw_exception = mock.Mock()

    message = create_message("Invalid Amount")
    budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.throw_exception.called


@patch("telebot.telebot")
def test_post_budget_limit_input_new_user(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 10
    budget_limit.helper.read_json.return_value = {}
    budget_limit.helper.createNewUserRecord.return_value = {"budget": {"limit": 0}}
    budget_limit.helper.write_json = mock.Mock()

    message = create_message("10")
    user_list = budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.write_json.called
    assert user_list["11"]["budget"]["limit"] == 10
    mc.send_message.assert_called_with(11, "Budget Limit Alert Updated to 10%!")


@patch("telebot.telebot")
def test_post_budget_limit_input_exceeds_budget(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 120  # Set to exceed budget
    budget_limit.helper.read_json.return_value = {
        "11": {"budget": {"overall": "100", "limit": 0}}
    }
    budget_limit.helper.write_json = mock.Mock()

    message = create_message("120")
    budget_limit.post_budget_limit_input(message, mc)

    mc.send_message.assert_called_with(
        11,
        "Budget Limit Alert Updated to 120%!"
    )


@patch("telebot.telebot")
def test_post_budget_limit_input_non_numeric(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 0
    budget_limit.helper.throw_exception = mock.Mock()

    message = create_message("non-numeric")
    budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.throw_exception.called


@patch("telebot.telebot")
def test_post_budget_limit_input_zero_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 0
    budget_limit.helper.throw_exception = mock.Mock()

    message = create_message("0")
    budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.throw_exception.called


@patch("telebot.telebot")
def test_post_budget_limit_input_max_limit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.validate_entered_amount.return_value = 100
    budget_limit.helper.read_json.return_value = {}
    budget_limit.helper.createNewUserRecord.return_value = {"budget": {"limit": 0}}
    budget_limit.helper.write_json = mock.Mock()

    message = create_message("100")
    user_list = budget_limit.post_budget_limit_input(message, mc)

    assert budget_limit.helper.write_json.called
    assert user_list["11"]["budget"]["limit"] == 100
    mc.send_message.assert_called_with(11, "Budget Limit Alert Updated to 100%!")


@patch("telebot.telebot")
def test_run_multiple_options(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }

    message = create_message("Update Budget Limit, Delete Budget Limit")
    budget_limit.run(message, mc)

    assert mc.reply_to.called

@patch("telebot.telebot")
def test_cancel_operation_midway(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mocker.patch.object(budget_limit, "helper")
    budget_limit.helper.getBudgetLimitOptions.return_value = {
        "updatelim": "Update Budget Limit",
        "dellim": "Delete Budget Limit",
        "exit": "Exit",
    }

    message = create_message("Exit")
    result = budget_limit.post_limit_option_selection(message, mc)

    assert result is None
    assert not mc.send_message.called


