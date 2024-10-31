import unittest
from collections import defaultdict
from code import insight


# === Helper Functions for Test Data ===
def prepare_monthly_spend():
    """Prepares dummy monthly spend data for testing."""
    return {
        "Oct-2024": {"Food": 10.5, "Transport": 15.2, "Groceries": 35.0},
        "Nov-2024": {"Utilities": 60.0, "Food": 20.0, "Transport": 30.0},
    }


def prepare_day_spend():
    """Prepares dummy day-wise spend data for testing."""
    return {
        0: 0.0,  # Monday
        1: 0.0,  # Tuesday
        2: 10.5,  # Wednesday (Food)
        3: 15.2,  # Thursday (Transport)
        4: 0.0,  # Friday
        5: 20.0,  # Saturday (Food)
        6: 30.0,  # Sunday (Transport)
    }


def prepare_single_day_spend():
    """Prepares data for a single-day transaction."""
    return {"Oct-2024": {"Food": 100.0}}


def prepare_spending_spike():
    """Prepares data with a spending spike in one month."""
    return {"Oct-2024": {"Food": 50.0}, "Nov-2024": {"Food": 200.0, "Groceries": 100.0}}


def prepare_no_weekend_spending():
    """Prepares data with no weekend spending."""
    return {
        0: 10.0,  # Monday
        1: 20.0,  # Tuesday
        2: 15.0,  # Wednesday
        3: 30.0,  # Thursday
        4: 25.0,  # Friday
        5: 0.0,  # Saturday
        6: 0.0,  # Sunday
    }


def prepare_missing_category_data():
    """Prepares data with a missing category in one month."""
    return {
        "Oct-2024": {"Food": 50.0, "Transport": 100.0},
        "Nov-2024": {"Groceries": 200.0},
    }


def prepare_large_spending():
    """Prepares data with large spending values."""
    return {
        "Oct-2024": {"Food": 1_000_000.0, "Transport": 500_000.0},
        "Nov-2024": {"Utilities": 2_000_000.0},
    }


def prepare_sample_day_spend():
    """Prepares sample day-wise spend data for testing."""
    return {
        0: 0.0,  # Monday
        1: 15.0,  # Tuesday
        2: 20.0,  # Wednesday
        3: 10.0,  # Thursday
        4: 5.0,  # Friday
        5: 0.0,  # Saturday
        6: 0.0,  # Sunday
    }


def prepare_sample_monthly_spend():
    """Prepares minimal sample monthly spending data for testing."""
    return {
        "Oct-2024": {"Food": 50.0, "Transport": 20.0},
        "Nov-2024": {"Food": 70.0, "Transport": 10.0},
    }


# === Test Suite ===
class TestInsights(unittest.TestCase):

    def test_generate_valid_insights(self):
        """Test insights generation with valid data."""
        monthly_spend = prepare_monthly_spend()
        day_spend = prepare_day_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("You tend to spend more on weekends", insights)
        self.assertIn("Comparison between Nov-2024 and Oct-2024", insights)
        self.assertIn("Your average monthly spending is", insights)
        self.assertIn("Spending in Nov-2024 by category", insights)

    def test_weekend_vs_weekday_spending(self):
        """Test weekend vs weekday spending insight."""
        monthly_spend = prepare_monthly_spend()
        day_spend = prepare_day_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("You tend to spend more on weekends", insights)

    def test_equal_weekend_weekday_spending(self):
        """Test insight when weekend and weekday spending are equal."""
        day_spend = prepare_day_spend()
        day_spend[0] = 30.0  # Make Monday spending equal to Sunday

        monthly_spend = prepare_monthly_spend()
        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("You spend more on weekdays", insights)

    def test_month_over_month_comparison(self):
        """Test month-over-month comparison in insights."""
        monthly_spend = prepare_spending_spike()
        day_spend = prepare_day_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("Comparison between Nov-2024 and Oct-2024", insights)
        self.assertIn("You spent 300.00% more on Food", insights)

    def test_category_wise_breakdown(self):
        """Test category-wise spending breakdown for the most recent month."""
        monthly_spend = prepare_monthly_spend()
        day_spend = prepare_day_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("Spending in Nov-2024 by category", insights)
        self.assertIn("Food: $20.00", insights)
        self.assertIn("Utilities: $60.00", insights)

    def test_insufficient_data(self):
        """Test behavior with insufficient data for insights."""
        monthly_spend = {"Oct-2024": {"Food": 10.5}, "Nov-2024": {"Transport": 20.0}}
        day_spend = prepare_day_spend()
        insights = insight.generate_insights(monthly_spend, day_spend)
        self.assertIn("Comparison between Nov-2024 and Oct-2024", insights)

    def test_zero_spending_in_month(self):
        """Test insights when a month has zero spending."""
        monthly_spend = {"Oct-2024": {}, "Nov-2024": {"Food": 20.0}}
        day_spend = prepare_day_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("Spending in Nov-2024 by category", insights)
        self.assertIn("Food: $20.00", insights)

    def test_weekday_vs_weekend_spending(self):
        """Test calculation of weekday vs weekend spending."""
        day_spend = prepare_sample_day_spend()
        monthly_spend = prepare_sample_monthly_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("You spend more on weekdays", insights)

    def test_percentage_change_in_spending(self):
        """Test correct percentage change calculation between months."""
        monthly_spend = prepare_sample_monthly_spend()
        day_spend = defaultdict(float)  # Empty day spend for this test

        insights = insight.generate_insights(monthly_spend, day_spend)

        # Verifying percentage increase from Oct to Nov for Food
        self.assertIn("You spent 40.00% more on Food", insights)

    def test_handle_missing_category_in_month_comparison(self):
        """Test month-over-month comparison with missing category."""
        monthly_spend = {"Oct-2024": {"Food": 50.0}, "Nov-2024": {"Transport": 30.0}}
        day_spend = defaultdict(float)  # No day spend needed for this test

        insights = insight.generate_insights(monthly_spend, day_spend)

        # Check if comparison is generated even when categories differ
        self.assertIn("Comparison between Nov-2024 and Oct-2024", insights)

    def test_zero_spending_in_weekday_vs_weekend(self):
        """Test weekday vs weekend insight when there is no weekend spending."""
        day_spend = {
            0: 30.0,  # Monday
            1: 20.0,  # Tuesday
            2: 15.0,
            3: 10.0,
            4: 5.0,
            5: 0.0,
            6: 0.0,
        }
        monthly_spend = prepare_sample_monthly_spend()

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("You spend more on weekdays", insights)

    def test_calculate_average_monthly_spending(self):
        """Test calculation of the average monthly spending."""
        monthly_spend = prepare_sample_monthly_spend()
        day_spend = defaultdict(float)  # No day spend needed for this test

        insights = insight.generate_insights(monthly_spend, day_spend)

        self.assertIn("Your average monthly spending is $75.00", insights)


# === Run Tests ===
if __name__ == "__main__":
    unittest.main()
