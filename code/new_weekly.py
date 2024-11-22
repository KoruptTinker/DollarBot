import helper
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os

matplotlib.use("agg")  # Use 'agg' backend to avoid GUI issues.


def run(message, bot):
    """
    Displays Weekly user expenditure line charts and new bar and pie charts for more insights.
    """
    helper.read_json()
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)

    if user_history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        try:
            # Keep original charts and add new charts
            charts = create_chart_for_weekly_analysis(user_history, chat_id)

            # Send all generated charts to the user
            for chart in charts:
                with open(chart, "rb") as f:
                    bot.send_photo(chat_id, f)
        except Exception as e:
            print(f"Exception occurred: {e}")
            bot.reply_to(message, "Oops! Could not create weekly analysis chart")


def create_chart_for_weekly_analysis(user_history, userid):
    result = []

    # Parse user history into a DataFrame
    user_history_split = [
        [item["date"], item["category"], item["amount"]] for item in user_history
    ]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"])
    df.dropna(subset=["Cost"], inplace=True)

    df["Year"] = df["Date"].dt.year
    df["Week"] = df["Date"].dt.strftime("%U")

    # Keep your original charts
    result.append(create_original_line_chart(df, userid))
    result.append(create_category_line_chart(df, userid))

    # Add new bar chart and pie chart
    result.append(create_bar_chart(df, userid))
    result.append(create_pie_chart(df, userid))

    return result


# Your Original Line Chart (No Changes)
def create_original_line_chart(df, userid):
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(["Year", "Week"]).agg({"Cost": "sum"}).reset_index()
    plt.plot(grouped_data.index, grouped_data["Cost"], marker="o")
    plt.xticks(
        grouped_data.index,
        "Week: " + grouped_data["Week"],
        rotation=45,
    )
    plt.xlabel("Year-Week")
    plt.ylabel("Total Cost")
    plt.title("Total Expenses Over Time")
    plt.grid(True)
    fig_name = f"data/{userid}_weekly_line_chart.png"
    plt.savefig(fig_name, bbox_inches="tight")
    plt.close()
    return fig_name


# Your Original Category Line Chart (No Changes)
def create_category_line_chart(df, userid):
    plt.figure(figsize=(12, 6))
    grouped_data = (
        df.groupby(["Year", "Week", "Category"]).agg({"Cost": "sum"}).reset_index()
    )

    for category in df["Category"].unique():
        category_data = grouped_data[grouped_data["Category"] == category]
        plt.plot(category_data.index, category_data["Cost"], marker="o", label=category)

    plt.xticks(
        grouped_data.index,
        "Week: " + grouped_data["Week"],
        rotation=45,
    )
    plt.xlabel("Year-Week")
    plt.ylabel("Total Cost")
    plt.title("Expenses Over Time by Category")
    plt.legend()
    plt.grid(True)
    fig_name = f"data/{userid}_category_line_chart.png"
    plt.savefig(fig_name, bbox_inches="tight")
    plt.close()
    return fig_name


# New Bar Chart for Weekly Expenses
def create_bar_chart(df, userid):
    grouped_data = df.groupby(["Year", "Week"]).agg({"Cost": "sum"}).reset_index()
    fig = px.bar(
        grouped_data,
        x="Week",
        y="Cost",
        color="Year",
        barmode="group",
        title="Weekly Expenses - Bar Chart",
    )
    fig_name = f"data/{userid}_weekly_bar_chart.png"
    pio.write_image(fig, fig_name)
    return fig_name


# New Pie Chart for Category-wise Spending Distribution
def create_pie_chart(df, userid):
    category_data = df.groupby("Category").agg({"Cost": "sum"}).reset_index()
    fig = px.pie(
        category_data,
        names="Category",
        values="Cost",
        title="Category-wise Spending Distribution",
        hole=0.4,
    )
    fig_name = f"data/{userid}_category_pie_chart.png"
    pio.write_image(fig, fig_name)
    return fig_name
