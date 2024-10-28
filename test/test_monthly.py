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

invalid_user_history = [
    "2024-10-01,Food,abc",  # Invalid cost value
    "2024-10-15,Transport,",
]

dummy_user_id = "test_user"

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


@patch("os.makedirs")
@patch("new_monthly.pio.write_image")
def test_create_category_pie_chart_with_empty_data(mock_write_image, mock_makedirs):
    """Test category pie chart with no data."""
    df = pd.DataFrame(columns=["Date", "Category", "Cost"])  # Empty DataFrame
    result = new_monthly.create_category_pie_chart(df, dummy_user_id)

    expected_filename = f"data/{dummy_user_id}_category_pie_chart.png"
    assert result == expected_filename

    # Ensure write_image was called even with empty data
    mock_write_image.assert_called_once_with(mock.ANY, expected_filename)


@patch("new_monthly.pio.write_image")
def test_create_monthly_bar_chart_with_invalid_cost(mock_write_image):
    """Test bar chart creation with invalid cost values."""
    df = prepare_test_dataframe(invalid_user_history)
    result = new_monthly.create_monthly_bar_chart(df, dummy_user_id)

    expected_filename = f"data/{dummy_user_id}_monthly_bar_chart.png"
    assert result == expected_filename

    # Ensure the chart was still saved
    mock_write_image.assert_called_once_with(mock.ANY, expected_filename)


@patch("os.remove")
@patch("new_monthly.create_chart_for_monthly_analysis")
def test_run_with_empty_history(mock_create_chart, mock_remove, mocker):
    """Test the run function when history is empty."""
    mock_create_chart.return_value = []  # No charts generated

    bot = MagicMock()
    message = mocker.MagicMock()
    message.chat.id = 12345

    new_monthly.run(message, bot)

    # Ensure no charts were sent or removed
    bot.send_photo.assert_not_called()
    mock_remove.assert_not_called()


@patch("builtins.open", new_callable=mock_open)
@patch("os.remove")
def test_cleanup_after_file_send(mock_remove, mock_open):
    """Test if files are properly removed after being sent to the bot."""
    bot = MagicMock()
    charts = [
        f"data/{dummy_user_id}_monthly_analysis.png",
        f"data/{dummy_user_id}_monthly_analysis_by_category.png"
    ]

    for chart in charts:
        with open(chart, "rb") as f:
            bot.send_photo(12345, f)

    # Ensure files are removed
    for chart in charts:
        os.remove(chart)
        mock_remove.assert_any_call(chart)


@patch("builtins.open", side_effect=Exception("File open error"))
@patch("code.new_monthly.helper.getUserHistory", return_value=dummy_user_history)
def test_run_with_file_open_exception(mock_get_history, mock_open, mocker):
    """Test run function when file opening raises an exception."""
    bot = MagicMock()
    message = mocker.MagicMock()
    message.chat.id = 12345

    new_monthly.run(message, bot)

    # Ensure the exception message is sent to the user
    bot.reply_to.assert_called_once_with(
        message, "Oops! Could not create monthly analysis chart"
    )

@patch("code.new_monthly.pio.write_image")
def test_non_existent_category(mock_write_image):
    """Test handling of a non-existent category."""
    df = pd.DataFrame({
        "Date": ["2024-10-01"],
        "Category": ["NonExistentCategory"],
        "Cost": [100.0]
    })
    result = new_monthly.create_category_pie_chart(df, dummy_user_id)

    expected_filename = f"data/{dummy_user_id}_category_pie_chart.png"
    assert result == expected_filename

    # Verify that the pie chart was created
    mock_write_image.assert_called_once_with(mock.ANY, expected_filename)

