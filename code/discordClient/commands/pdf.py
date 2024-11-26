from discord import app_commands
import discord
import helper
import logging
from matplotlib import pyplot as plt
from fpdf import FPDF
import graphing
import os
import asyncio


async def pdf(interaction: discord.Interaction):
    # Defer the reply immediately to prevent timeout
    await interaction.response.defer()

    try:
        helper.read_json()

        user_details = helper.fetchUserFromDiscord(interaction.user.id)
        if user_details is None:
            interaction.response.send_message(
                "You don't have your discord account linked to an active telegram account. Use /link command on telegram to learn more"
            )
            return

        chat_id = helper.fetchUserFromDiscord(interaction.user.id)["telegram_chat_id"]
        user_history = helper.getUserHistory(user_details["telegram_chat_id"])

        if user_history is None or len(user_history) == 0:
            await interaction.response.send_message(
                "Sorry! No spending records found!", ephemeral=True
            )
            return

        # interaction.response.send_message(
        #         "Alright. Creating a pdf of your expense history!"
        #     )

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        top = 0.8
        if len(user_history) == 0:
            plt.text(
                0.1,
                top,
                "No record found!",
                horizontalalignment="left",
                verticalalignment="center",
                transform=ax.transAxes,
                fontsize=20,
            )

        if helper.isOverallBudgetAvailable(chat_id):
            category_budget = helper.getCategoryBudget(chat_id)
            graphing.overall_split(category_budget)

            category_spend = {}
            for spend in user_history:
                category_spend[spend["category"]] = (
                    category_spend.get(spend["category"], 0) + spend["amount"]
                )
            if category_spend != {}:
                graphing.spend_wise_split(category_spend)

            if user_history:
                cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)
                graphing.time_series(cat_spend_dict)

            list_of_images = ["overall_split.png", "spend_wise.png", "time_series.png"]
            pdf = FPDF()
            pdf.add_page()
            x_coord = 20
            y_coord = 30
            for image in list_of_images:
                pdf.image(image, x=x_coord, y=y_coord, w=70, h=50)
                x_coord += 80
                if x_coord > 100:
                    x_coord = 20
                    y_coord += 60
            pdf.output("expense_report.pdf", "F")
            with open("expense_report.pdf", "rb") as pdf_file:
                file = discord.File(pdf_file, filename="expense_report.pdf")
                await interaction.followup.send(
                    "Here's your expense report:", file=file, ephemeral=True
                )

            # Clean up files
            await asyncio.sleep(0.5)
            try:
                # Remove the PDF
                os.remove("expense_report.pdf")
                # Remove any generated images
                for image in list_of_images:
                    os.remove(image)
            except OSError:
                # If files are still locked, try again after a delay
                await asyncio.sleep(1)
                os.remove("expense_report.pdf")
                for image in list_of_images:
                    os.remove(image)

        else:
            await interaction.followup.send(
                "Oh no! Set your corresponding category wise budgets using the /budget command to generate the expense report",
            )

    except Exception as e:
        await interaction.followup.send("Oops!" + str(e))


async def setup(tree: app_commands.CommandTree):
    tree.command(name="pdf", description="View a detailed summary of expenditure")(pdf)
