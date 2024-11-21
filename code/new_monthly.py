import helper
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os

matplotlib.use("agg")


def run(message, bot):
    """
    Displays Monthly user expenditure charts, with new bar and pie charts for additional insights.
    """
    helper.read_json()
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)

    if user_history is None or len(user_history) == 0:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        try:
            charts = create_chart_for_monthly_analysis(user_history, chat_id)
            for chart in charts:
                with open(chart, "rb") as f:
                    bot.send_photo(chat_id, f)
        except Exception as e:
            print(f"Exception occurred: {e}")
            bot.reply_to(message, "Oops! Could not create monthly analysis chart")


def create_chart_for_monthly_analysis(user_history, userid):
    """
    Generates monthly analysis charts: original line charts and new bar/pie charts.
    """
    result = []

    # Parse user history into a DataFrame
    user_history_split = [[item["date"], item["category"], item["amount"]] for item in user_history]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])

    # Data Preprocessing
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"])
    df.dropna(subset=["Cost"], inplace=True)

    df["Month"] = df["Date"].dt.month_name()
    df["Year"] = df["Date"].dt.year

    # Keep your original two charts
    result.append(create_original_monthly_chart(df, userid))
    result.append(create_category_monthly_chart(df, userid))

    # Add new bar chart and pie chart
    result.append(create_monthly_bar_chart(df, userid))
    result.append(create_category_pie_chart(df, userid))

    return result


# Your Original Line Chart (No Changes)
def create_original_monthly_chart(df, userid):
    plt.figure(figsize=(10, 6))
    grouped_data = df.groupby(["Year", "Month"]).agg({"Cost": "sum"}).reset_index()
    plt.plot(grouped_data.index, grouped_data["Cost"], marker="o")
    plt.xticks(
        grouped_data.index,
        grouped_data["Year"].astype(str) + "-" + grouped_data["Month"],
        rotation=45,
    )
    plt.xlabel("Year-Month")
    plt.ylabel("Total Cost")
    plt.title("Total Cost Over Time")
    plt.grid(True)
    fig_name = f"data/{userid}_monthly_analysis.png"
    plt.savefig(fig_name, bbox_inches="tight")
    plt.close()
    return fig_name


# Your Original Category Line Chart (No Changes)
def create_category_monthly_chart(df, userid):
    plt.figure(figsize=(12, 6))
    grouped_data = (
        df.groupby(["Year", "Month", "Category"]).agg({"Cost": "sum"}).reset_index()
    )

    for category in df["Category"].unique():
        category_data = grouped_data[grouped_data["Category"] == category]
        plt.plot(category_data.index, category_data["Cost"], marker="o", label=category)

    plt.xticks(
        grouped_data.index,
        grouped_data["Year"].astype(str) + "-" + grouped_data["Month"],
        rotation=45,
    )
    plt.xlabel("Year-Month")
    plt.ylabel("Total Cost")
    plt.title("Total Cost Over Time by Category")
    plt.legend()
    plt.grid(True)
    fig_name = f"data/{userid}_monthly_analysis_by_category.png"
    plt.savefig(fig_name, bbox_inches="tight")
    plt.close()
    return fig_name


# New: Monthly Bar Chart
def create_monthly_bar_chart(df, userid):
    grouped_data = df.groupby(["Year", "Month"]).agg({"Cost": "sum"}).reset_index()
    fig = px.bar(
        grouped_data,
        x="Month",
        y="Cost",
        color="Year",
        barmode="group",
        title="Monthly Expenses - Bar Chart",
    )
    fig_name = f"data/{userid}_monthly_bar_chart.png"
    print(f"Saving bar chart to: {fig_name}")
    pio.write_image(fig, fig_name)
    return fig_name


# New: Category-wise Spending Pie Chart
def create_category_pie_chart(df, userid):
    category_data = df.groupby("Category").agg({"Cost": "sum"}).reset_index()
    fig = px.pie(
        category_data,
        names="Category",
        values="Cost",
        title="Category-wise Spending Distribution (Monthly)",
        hole=0.4,
    )
    fig_name = f"data/{userid}_category_pie_chart.png"
    pio.write_image(fig, fig_name)
    return fig_name
