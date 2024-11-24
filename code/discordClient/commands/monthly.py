from discord import app_commands
import discord
import helper
import helper
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio


async def monthly(interaction: discord.Interaction):
    user_details = helper.fetchUserFromDiscord(interaction.user.id)
    if user_details is None:
        interaction.response.send_message(
            "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
        )
        return

    user_history = helper.getUserHistory(user_details["telegram_chat_id"])

    if user_history is None or len(user_history) == 0:
        await interaction.response.send_message(
            "Sorry! No spending records found!", ephemeral=True
        )
        return
    else:
        try:
            # Keep original charts and add new charts
            charts = create_chart_for_monthly_analysis(
                user_history, user_details["telegram_chat_id"]
            )
            files = [discord.File(open(chart, "rb")) for chart in charts]
            await interaction.response.send_message(files=files)
        except Exception as e:
            print(f"Exception occurred: {e}")
            await interaction.response.send_message("Something went wrong")

def create_chart_for_monthly_analysis(user_history, userid):
    """
    Generates monthly analysis charts: original line charts and new bar/pie charts.
    """
    result = []

    # Parse user history into a DataFrame
    user_history_split = [
        [item["date"], item["category"], item["amount"]] for item in user_history
    ]
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

async def setup(tree: app_commands.CommandTree):
    tree.command(name="monthly", description="View monthly analysis")(monthly)