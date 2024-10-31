![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/github/languages/top/vegechick510/DollarBot?color=red&label=Python&logo=Python&logoColor=yellow)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
[![DOI](https://zenodo.org/badge/875854476.svg)](https://doi.org/10.5281/zenodo.14018911)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/vegechick510/DollarBot/actions/workflows/black.yml)
[![Autopep8](https://github.com/vegechick510/DollarBot/actions/workflows/autopep8.yml/badge.svg)](https://github.com/vegechick510/DollarBot/actions/workflows/autopep8.yml)
![GitHub contributors](https://img.shields.io/github/contributors/vegechick510/DollarBot)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![codecov](https://codecov.io/gh/vegechick510/DollarBot/graph/badge.svg?token=uFIfOR9FTm)](https://codecov.io/gh/vegechick510/DollarBot)
![Lines of code](https://tokei.rs/b1/github/vegechick510/DollarBot)
![Version](https://img.shields.io/github/v/release/vegechick510/DollarBot?color=ff69b4&label=Version)
![GitHub issues](https://img.shields.io/github/issues-raw/vegechick510/DollarBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/vegechick510/DollarBot)

# 💰 Dollar Bot 💰

<hr>

# DollarBot - Because your financial future deserves the best!

You wake up, brew a fresh cup of coffee, and start your day. You're excited because today is the day you take control of your finances like never before. How? Say hello to DollarBot, your ultimate financial companion. With simple commands, it transforms your financial story into one of motivation, empowerment, and control. 

And the best part? DollarBot is your financial sidekick, available exclusively on Telegram. That means no matter where you are, it's there to assist you in recording your expenses seamlessly.

<p align="center">
  <img src="https://github.com/vegechick510/DollarBot/blob/main/docs/DALL%C2%B7E%202024-10-31%2001.51.11%20-%20A%20cartoon-style%20illustration%20of%20a%20friendly%20robot%20for%20a%20financial%20management%20project.%20The%20robot's%20features%20are%20represented%20by%20shapes%2C%20symbolizing%20funct.webp" alt="DollarBot Illustration" width="400"/>
</p>



## Demo Video

<a href="https://youtu.be/bAio20DZ_-I">https://youtu.be/bAio20DZ_-I</a>


## :money_with_wings: About DollarBot

DollarBot is a user-friendly Telegram bot designed to simplify your daily expense recording on a local system effortlessly.

With simple commands, this bot allows you to:

📝 **Add/Record a new spending:** As you sip that morning coffee, effortlessly log your expenses, no matter how small or significant. Every expense adds up, and DollarBot ensures you don't miss a thing.

💡 **Display your expenditure for the current day/month:** With DollarBot, you're never in the dark about your spending. Get real-time insights on your daily and monthly expenses, motivating you to stay on budget and crush your financial goals.

🔍 **Show your spending history:** Ever wondered where your money disappears to? DollarBot provides a detailed spending history that tells a story of your financial habits. It's a tale of lessons and opportunities for improvement.

🗑️ **Delete/Erase all your records:** Made an error or just want to start afresh? It's as simple as a command, a chance to correct your narrative without any hassle.

🔧 **Edit/Change any spending details:** Life is full of surprises, and sometimes expenses change. DollarBot adapts with you, offering easy editing options to keep your story accurate.

📊 Set Your Budget: Take full control of your finances by defining and tracking your budget with DollarBot. It's the proactive step that puts you firmly in the driver's seat of your financial journey.

📈 **Visualize your spending:** Numbers can be daunting, but DollarBot transforms them into a captivating visual experience. Use the '/chart' option to see your spending as graphs and pie charts. This punchline to your story helps you spot trends and make smarter financial choices.

📈 **Predict future expenses:** Predict your next month's budget based on your current expenditure

# :star: What's New?

- **Multi-Currency Support:** Track expenses in multiple currencies, with automatic conversion to primary currency(US dollars) for unified reporting.
- **Enhanced Budget Tracking and Alerts:** Set custom budget limits and receive alerts when you reach specific percent of your budget to avoid overspending.
- **Personalized Spending Insights:** Get actionable insights based on your spending patterns, such as “You spend more on weekends” or “Dining expenses increased by 20% this month.”
- **Enhanced Data Visualization:** Enjoy new chart types, including bar and pie charts, with filtering options by category and time to better analyze spending trends.
- **Debugging issues and Better documentation::** Improved code for easier debugging and enhanced documentation to help developers maintain the project efficiently.


Are you a developer? <a href="https://github.com/vegechick510/DollarBot/blob/main/README.md">Click here: For Developers and Future Contributors</a>

# :rocket: Installation and Setup

## Pre-requisite: The Telegram Desktop App

Since DollarBot is built on top of Telegram, you'll first need:
1. Download the Telegram Desktop Application <a href="https://desktop.telegram.org/">here.</a>
```https://desktop.telegram.org/```
2. Create a Telegram account or Sign in.

Open up your terminal and let's get started:

### MacOS / Ubuntu Users

1. Clone this repository to your local system. 
```
   git clone https://github.com/aditikilledar/dollar_bot_SE23/
```
2. Start a terminal session in the directory where the project has been cloned. Run the following commands and follow the instructions on-screen to complete the installation.
```
  chmod a+x setup.sh
  bash setup.sh
```
There, all done!

The installation is easy for MacOS or on UNIX terminals. 

### Windows

With Windows, you'll need to use a platform to execute UNIX-like commands in order to execute the setup.sh bash script. Once in the platform, use the steps in the MacOS/Unix Section above to setup DollarBot.

We've used <a href="https://www.cygwin.com/">Cygwin,</a> but there are more options like WSL that you can explore.

Additionally, find more hints on Cygwin installation <a href="https://stackoverflow.com/questions/6413377/is-there-a-way-to-run-bash-scripts-on-windows">here.</a>

## Running DollarBot:

Once you've executed setup.sh, and all dependencies have been installed, you can start running DollarBot by following these instructions.

1. Open the Telegram Desktop Application and sign in. Once inside Telegram, search for "BotFather". Click on "Start", and enter the following command:
```
  /newbot
```
2. Follow the instructions on screen and choose a name for your bot (e.g., `dollarbot`). After this, select a UNIQUE username for your bot that ends with "bot", for example: `dollarbot_<your_nickname>`.

3. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy and save this token for future use. Make sure you save this token– don't lose it!

4. In the repo directory (where you cloned it), run these commands.

(a) grant execution access to a bash script
  ```
  chmod a+x run.sh
  ```

(b) execute the run.sh bash script to start DollarBot
   
#### MacOS / Unix
```
   bash run.sh
```
#### Windows
```
   ./run.sh
```

```Note```: It will ask you to paste the API token you received from Telegram while creating your bot (Step 3), so keep that handy.
A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

5. In the Telegram app, search for your newly created bot by entering your UNIQUE username and open the bot you created.

6. Now, on Telegram, enter the "/start" or "menu" command, and you are all set to track your expenses!

### Run Automatically at Startup

To run the script automatically at startup / reboot, simply add the `.run_forever.sh` script to your `.bashrc` file, which executes whenever you reboot your system.
<a href="https://stackoverflow.com/questions/49083789/how-to-add-new-line-in-bashrc-file-in-ubuntu">Click here for help adding to .bashrc files.</a>

# :information_desk_person: Use Cases

Here's a quick overview of how each of the commands work. Simply enter /<command_name> into the Telegram chat and watch as the magic happens! 

### Menu
View all the commands Dollarbot offers to manage your expenses

[Click here to view the menu command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/menu_command.gif)

It can be invoked by using `/menu` command.

### Help
Display the list of commands.

[Click here to view the help command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/help_command.gif)
It can be invoked by using `/help` command.

### Pdf
Save history as PDF.

[Click here to view the pdf command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/pdf_command.gif)
It can be invoked by using `/pdf` command.

### Add
This option is for adding your expenses.

[Click here to view the add command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/add_command.gif)
1. It will give you the list of categories to choose from. <br> 
2. You will be prompted to enter the amount corresponding to your spending <br>      
3. The message will be prompted to notify the addition of your expense with the amount,date, time and category <br> 
4. It can be invoked by using `/add` command. 

### Analytics
This option gives user a graphical representation of their expenditures.

[Click here to view the Analytics command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/analytics.gif)
1. You will get an option to choose the type of data you want to see. <br> 
2. It can be invoked by using `/analytics` command.

### Predict
This option analyzes your recorded spendings and gives you a budget that will accommodate for them.

[Click here to view the Predict command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/predict_command.gif)
It can be invoked by using `/predict` command.

### History
This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spendings.
[Click here to view the History command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/history.gif)

It can be invoked by using `/history` command.

### Delete
This option is to Clear/Erase all your records.
[Click here to view the Delete command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/delete.gif)

It can be invoked by using `/delete` command.

### Edit
This option helps you to go back and correct/update the missing details    
[Click here to view the Edit command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/edit_command.gif)


1. It will give you the list of your expenses you wish to edit <br> 
2. It will let you change the specific field based on your requirements like amount/date/category <br> 
3. It can be invoked by using `/edit` command.

### Budget
This option is to set/update/delete the budget.     
[Click here to view the Budget command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/budget_command.gif)


1. The Add/update category is to set the new budget or update the existing budget <br>      
2. The view category gives the detail if budget is exceeding or in limit with the difference amount  <br>        
3. The delete category allows to delete the budget and start afresh! <br> 
4. It can be invoked by using `/budget` command.

### SendEmail
This option is to send you a email with you expenditures.
[Click here to view the SendEmail command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/send_mail.gif)


It can be invoked by using `/sendEmail` command.

### Add Recurring
This option is to add a recurring expense for future months.
[Click here to view the Add Recurring command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/add_recurring.gif)


It can be invoked by using `/add_recurring` command.

### Update Category
This option is to add/delete/edit the categories.         
[Click here to view the Update Category command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/update_category.gif)


1. The Add Category option is to add a new category which dosen't already exist  <br>       
2. The Delete Category option is to delete an existing category  <br> 
3. The Edit Category option is to edit an existing category. <br> 
4. It can be invoked by using `/updateCategory` command.

### Weekly
This option is to get the weekly analysis report of the expenditure.
[Click here to view the Weekly command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/weekly.gif)

It can be invoked by using `/weekly` command.


### Monthly
This option is to get the monthly analysis report of the expenditure
[Click here to view the Monthly command GIF](https://github.com/vegechick510/DollarBot/blob/main/docs/workflows/monthly.gif)

It can be invoked by using `/monthly` command.


### Insight
This option is to spending insights feature for users.         
<p align="center"><img width="700" src="./docs/workflows/insight.gif"></p>

It can be invoked by using `/insight` command.


### New Virtualization  
This option is to enhanced data visualization feature.         
<p align="center"><img width="700" src="./docs/workflows/monthly.gif"></p>

It can be invoked by using `/weekly` or `/monthly` command.


### Budget Limit
This option is to set/update/delete the budget limit for alert.     
<p align="center"><img width="700" src="./docs/workflows/budget_limit_add_upadte.gif"></p>
<p align="center"><img width="700" src="./docs/workflows/budget_limit_delete.gif"></p>

1. The Add/update category is to set the new budget limit or update the existing budget limit<br>      
2. The delete category allows to delete the budget limit! <br> 
3. It can be invoked by using `/budget` command.




### Currency
This option is to record expenses in multiple currencies, which are automatically converted to a primary currency (USD).         
<p align="center"><img width="700" src="./docs/workflows/currency.gif"></p>

It can be invoked by using `/add` command.



# :construction: What's Next

Some possible future enhancements are as follows:
1.	**Auto-Save to Google Drive:** Seamlessly back up your expenditure records to Google Drive. This feature lets you link your Google Drive account to DollarBot and automatically saves expense record
2.	**Smart Savings Goals:** Set personalized savings goals within DollarBot. As you record expenses, DollarBot will calculate your progress toward these goals, sending you reminders or encouraging messages to stay on track. Perfect for users saving for specific items, trips, or future plans.
3.	**Spending Challenges and Rewards:** Participate in spending challenges like “No-Spend Weekends” or “Save $50 a Week.” DollarBot tracks your progress, provides motivational updates, and rewards you with badges or points when you meet your goals. Great for those who need an extra push to stay financially disciplined!
4.	**Bill Reminder and Tracking:** Avoid late fees by setting up reminders for upcoming bills. DollarBot will remind you when due dates are near and can even record recurring bills for easy tracking.
5.	**Cash Flow Analysis:** Gain insight into your cash flow by categorizing income and expenses. DollarBot helps you identify trends in your spending and income, giving you a monthly or weekly overview of your cash flow status. 
6.	**Year-End Financial Summary:** Receive a detailed financial summary at the end of each year, which includes total income, expenses by category, savings achieved, and insights on how spending changed over the months.




:heart: Acknowledgements
---
We would like to thank Dr. Timothy Menzies for helping us understand the process of building a good Software Engineering project. We would also like to thank the teaching assistants for their support throughout the project.


:page_facing_up: License
---
This project is licensed under the terms of the MIT license. Please check [LICENSE](https://github.com/vegechick510/DollarBot/blob/main/LICENSE.md) for more details.

## Contributors
- [@Xianting Lu](https://github.com/xiantinglu)
- [@Xiang Lan](https://github.com/xianglan010)
- [@Xingyue Shi](https://github.com/AMShek)
# :calling: Support

For any support, email us at `xlan4@ncsu.edu`
