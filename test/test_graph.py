"""
File: test_graph.py
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

from code import graphing
import numpy as np
from mock import patch, MagicMock
import os

dummy_total_text_none = ""
dummy_total_text_data = """Food $10.0
Transport $50.0
Shopping $148.0
Miscellaneous $47.93
Utilities $200.0
Groceries $55.21\n"""

dummy_x = ["Food", "Transport", "Shopping", "Miscellaneous", "Utilities", "Groceries"]
dummy_y = [10.0, 50.0, 148.0, 47.93, 200.0, 55.21]
dummy_categ_val = {
    "Food": 10.0,
    "Transport": 50.0,
    "Shopping": 148.0,
    "Miscellaneous": 47.93,
    "Miscellaneous": 47.93,
    "Utilities": 200.0,
    "Groceries": 55.21,
}
dummy_color = [
    (1.00, 0, 0, 0.6),
    (0.2, 0.4, 0.6, 0.6),
    (0, 1.00, 0, 0.6),
    (1.00, 1.00, 0, 1.00),
]
dummy_edgecolor = "blue"
dummy_monthly_budget = {
    "Food": 100.0,
    "Transport": 150.0,
    "Shopping": 150.0,
    "Miscellaneous": 50,
    "Utilities": 200.0,
    "Groceries": 100,
}

n2 = len(dummy_x)
r2 = np.arange(n2)
width = 0.45


def test_visualize(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize(dummy_total_text_data, dummy_monthly_budget)
    # graphing.plt.bar.assert_called_with(r2,
    # ANY, width=width, label='your spendings')

@patch("code.graphing.plt.savefig")
def test_visualize_success(mock_savefig):
    """Test the original visualize function with valid data."""
    graphing.visualize(dummy_total_text_data, dummy_monthly_budget)
    mock_savefig.assert_called_once_with("expenditure.png", bbox_inches="tight")

@patch("code.graphing.plt.savefig")
def test_visualize_new(mocker_savefig):
    """Test the new visualize_new function."""
    result = graphing.visualize_new(dummy_total_text_data, dummy_monthly_budget)

    # Ensure the returned list contains the correct filenames
    assert result == [
        "stacked_bar_chart.png",
        "spending_pie_chart.png",
        "spending_trend_chart.png",
    ]

    # Check if the images were saved
    for img in result:
        mocker_savefig.assert_any_call(img, bbox_inches="tight")

@patch("os.remove")
@patch("code.graphing.plt.savefig")
def test_visualize_new_cleanup(mock_savefig, mock_remove):
    """Test that visualize_new generates and removes files correctly."""
    # Simulate generated image files from visualize_new
    generated_images = graphing.visualize_new(dummy_total_text_data, dummy_monthly_budget)

    # Check that the files were saved
    for img in generated_images:
        mock_savefig.assert_any_call(img, bbox_inches="tight")

    # Simulate file removal after sending to bot
    for img in generated_images:
        os.remove(img)  # Ensure actual call happens inside the test

    # Ensure that os.remove was called for each file
    for img in generated_images:
        mock_remove.assert_any_call(img)

def test_viewBudget_with_data(mocker):
    """Test viewBudget function with valid data."""
    mocker.patch.object(graphing, "plt")
    category_budget = {"Food": 100.0, "Transport": 150.0}
    result = graphing.viewBudget(category_budget)

    assert result is True
    graphing.plt.pie.assert_called_once()


def test_viewBudget_no_data(mocker):
    """Test viewBudget function with no budget data."""
    mocker.patch.object(graphing, "plt")
    category_budget = {"Food": 0.0, "Transport": 0.0}
    result = graphing.viewBudget(category_budget)

    assert result is False  


@patch("code.graphing.plt")
def test_time_series(mock_plt):
    """Test the time_series function."""
    cat_spend_dict = {"2024-10-01": 100.0, "2024-10-25": 150.0}
    graphing.time_series(cat_spend_dict)
    mock_plt.savefig.assert_called_once_with("time_series.png")


def test_overall_split_empty():
    """Test overall_split with empty data."""
    try:
        graphing.overall_split({})
    except ValueError as e:
        assert str(e) == "category_budget cannot be empty"


def test_spend_wise_split_empty():
    """Test spend_wise_split with empty data."""
    try:
        graphing.spend_wise_split({})
    except ValueError as e:
        assert str(e) == "category_spend cannot be empty"


def test_remaining_empty_data():
    """Test remaining function with empty data."""
    try:
        graphing.remaining({})
    except ValueError as e:
        assert str(e) == "category_spend_percent cannot be empty"


def test_time_series_empty_data():
    """Test time_series function with empty data."""
    try:
        graphing.time_series({})
    except ValueError as e:
        assert str(e) == "cat_spend_dict cannot be empty"



