import os
import pandas as pd
from unittest.mock import patch, MagicMock
from code import new_monthly
import mock
from mock import mock_open

# === Dummy Data for Testing ===
dummy_user_history = [
    "2024-10-01,Food,10.5",
    "2024-10-01,Transport,15.2",
    "2024-10-15,Groceries,35.0",
    "2024-11-05,Utilities,60.0",
]

dummy_user_id = "test_user"

# === Test Cases ===

@patch("code.new_monthly.plt.savefig")
def test_create_original_monthly_chart(mock_savefig):
    """Test the original monthly chart creation."""
    df = prepare_test_dataframe(dummy_user_history)
    result = new_monthly.create_original_monthly_chart(df, dummy_user_id)

    # Ensure the file was saved with the correct filename
    expected_filename = f"data/{dummy_user_id}_monthly_analysis.png"
    assert result == expected_filename
    mock_savefig.assert_called_once_with(expected_filename, bbox_inches="tight")

@patch("code.new_monthly.plt.savefig")
def test_create_category_monthly_chart(mock_savefig):
    """Test the category-wise monthly chart creation."""
    df = prepare_test_dataframe(dummy_user_history)
    result = new_monthly.create_category_monthly_chart(df, dummy_user_id)

    # Ensure the file was saved with the correct filename
    expected_filename = f"data/{dummy_user_id}_monthly_analysis_by_category.png"
    assert result == expected_filename
    mock_savefig.assert_called_once_with(expected_filename, bbox_inches="tight")

@patch("code.new_monthly.pio.write_image")
def test_create_monthly_bar_chart(mock_write_image):
    """Test the monthly bar chart creation with Plotly."""
    # Prepare the DataFrame
    df = prepare_test_dataframe(dummy_user_history)

    # Call the function to test
    result = new_monthly.create_monthly_bar_chart(df, dummy_user_id)

    # Check the expected filename
    expected_filename = f"data/{dummy_user_id}_monthly_bar_chart.png"
    assert result == expected_filename

    # Verify that write_image was called with the correct arguments
    mock_write_image.assert_called_once_with(mock.ANY, expected_filename)

@patch("code.new_monthly.pio.write_image")
def test_create_category_pie_chart(mock_write_image):
    """Test the category-wise pie chart creation."""
    df = prepare_test_dataframe(dummy_user_history)
    result = new_monthly.create_category_pie_chart(df, dummy_user_id)

    # Ensure the file was saved with the correct filename
    expected_filename = f"data/{dummy_user_id}_category_pie_chart.png"
    assert result == expected_filename

    # Verify that write_image was called with the correct arguments
    mock_write_image.assert_called_once_with(mock.ANY, expected_filename)


@patch("code.new_monthly.helper.getUserHistory", return_value=None)
@patch("code.new_monthly.helper.read_json")
def test_run_no_history(mock_read_json, mock_get_history, mocker):
    """Test the run function when no user history is available."""
    # Mock bot and message objects
    bot = MagicMock()
    message = mocker.MagicMock()
    message.chat.id = 12345

    # Call the function
    new_monthly.run(message, bot)

    # Ensure send_message() was called with the correct message
    bot.send_message.assert_called_once_with(
        12345, "Oops! Looks like you do not have any spending records!"
    )


# === Helper Function ===
def prepare_test_dataframe(user_history):
    """Helper function to prepare a DataFrame for testing."""
    user_history_split = [item.split(",") for item in user_history]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(subset=['Cost'], inplace=True)
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    return df
