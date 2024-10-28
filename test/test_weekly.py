import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from code import weekly  # Adjust the import based on your project structure

# === Dummy Data for Testing ===
dummy_user_history = [
    "2024-10-01,Food,10.5",
    "2024-10-02,Transport,15.2",
    "2024-10-03,Groceries,35.0",
    "2024-10-04,Utilities,60.0",
    "2024-10-05,Food,20.0",
    "2024-10-06,Transport,30.0"
]

dummy_user_id = "test_user"

def prepare_test_dataframe(user_history):
    """Helper function to prepare a DataFrame for testing."""
    user_history_split = [item.split(",") for item in user_history]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])
    df['Cost'] = pd.to_numeric(df['Cost'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# === Test Cases ===

@patch("code.weekly.plt.savefig")
def test_create_chart_for_weekly_analysis(mock_savefig):
    """Test if weekly charts are created correctly."""
    df = prepare_test_dataframe(dummy_user_history)
    result = weekly.create_chart_for_weekly_analysis(dummy_user_history, dummy_user_id)

    # Ensure both charts were saved with correct filenames
    expected_filenames = [
        f"data/{dummy_user_id}_weekly_analysis.png",
        f"data/{dummy_user_id}_weekly_analysis_by_category.png"
    ]

    assert result == expected_filenames
    mock_savefig.assert_any_call(expected_filenames[0], bbox_inches="tight")
    mock_savefig.assert_any_call(expected_filenames[1], bbox_inches="tight")


@patch("code.weekly.helper.getUserHistory", return_value=None)
def test_run_no_history(mock_get_history):
    """Test the run function with no user history."""
    bot = MagicMock()
    message = MagicMock()
    message.chat.id = 12345

    weekly.run(message, bot)

    # Ensure the bot sends a message about no records
    bot.send_message.assert_called_once_with(
        12345, "Oops! Looks like you do not have any spending records!"
    )

