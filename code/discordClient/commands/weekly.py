from discord import app_commands
import discord
import helper
import helper
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio


async def weekly(interaction: discord.Interaction):
    """Display weekly spending analysis with visualizations.

    This command generates and displays various charts analyzing the user's weekly spending patterns.
    It creates line charts, bar charts, and pie charts to visualize spending trends and category distributions.

    The function:
        1. Verifies user has a linked Telegram account
        2. Retrieves user's spending history
        3. Generates four visualization charts:
           - Weekly spending trend line chart
           - Category-wise weekly spending trend line chart
           - Weekly expenses bar chart
           - Category distribution pie chart
        4. Sends the charts as Discord attachments
    """
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
            charts = create_chart_for_weekly_analysis(
                user_history, user_details["telegram_chat_id"]
            )
            files = [discord.File(open(chart, "rb")) for chart in charts]
            await interaction.response.send_message(files=files)
        except Exception as e:
            print(f"Exception occurred: {e}")
            await interaction.response.send_message("Something went wrong")


def create_chart_for_weekly_analysis(user_history, userid):
    """Generate multiple visualization charts for weekly spending analysis.

    Creates four different types of charts to analyze spending patterns:
    - Total spending over time (line chart)
    - Category-wise spending over time (line chart) 
    - Weekly expenses comparison (bar chart)
    - Category distribution (pie chart)

    Returns:
        list: Paths to generated chart image files
    """
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


def create_original_line_chart(df, userid):
    """Create a line chart showing total weekly spending over time.

    Returns:
        str: Path to the generated chart image
    """
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
    """Create a line chart showing weekly spending trends by category.

    Returns:
        str: Path to the generated chart image
    """
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
    """Create a grouped bar chart comparing weekly expenses across years.

    Returns:
        str: Path to the generated chart image
    """
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
    """Create a donut chart showing distribution of spending across categories.

    Returns:
        str: Path to the generated chart image
    """
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


async def setup(tree: app_commands.CommandTree):
    tree.command(name="weekly", description="View weekly analysis")(weekly)
