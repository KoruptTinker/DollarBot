[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/KoruptTinker/DollarBot/blob/main/LICENSE.md)
[![GitHub](https://img.shields.io/github/languages/top/KoruptTinker/DollarBot?color=green&label=Python&logo=Python&logoColor=green)]
[![DOI](https://zenodo.org/badge/875854476.svg)](https://doi.org/10.5281/zenodo.14018911)
[![Black](https://github.com/KoruptTinker/DollarBot/actions/workflows/black.yml/badge.svg)](https://github.com/KoruptTinker/DollarBot/actions/workflows/black.yml)
[![Autopep8](https://github.com/KoruptTinker/DollarBot/actions/workflows/autopep8.yml/badge.svg)](https://github.com/KoruptTinker/DollarBot/actions/workflows/autopep8.yml)
[![Pylint](https://github.com/KoruptTinker/DollarBot/actions/workflows/pylint.yml/badge.svg)](https://github.com/KoruptTinker/DollarBot/actions/workflows/pylint.yml)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
![Discord](https://img.shields.io/discord/1309342901108604968?style=flat&logo=discord&logoColor=green&label=Discord%20Server)
[![codecov](https://codecov.io/gh/KoruptTinker/DollarBot/graph/badge.svg?token=crodhCsUXz)](https://codecov.io/gh/KoruptTinker/DollarBot)
[![pytest](https://github.com/KoruptTinker/DollarBot/actions/workflows/pytest.yml/badge.svg)](https://github.com/KoruptTinker/DollarBot/actions/workflows/pytest.yml)
[![GitHub issues](https://img.shields.io/github/issues-raw/KoruptTinker/DollarBot)](https://github.com/KoruptTinker/DollarBot/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/KoruptTinker/DollarBot)](https://github.com/KoruptTinker/DollarBot/issues?q=is%3Aissue+is%3Aclosed)

# 💰 Dollar Bot 💰

<hr>

# DollarBot - Because your financial future deserves the best!

You wake up, brew a fresh cup of coffee, and start your day. You're excited because today is the day you take control of your finances like never before. How? Say hello to DollarBot, your ultimate financial companion. With simple commands, it transforms your financial story into one of motivation, empowerment, and control. 

And the best part? DollarBot is your financial sidekick, available exclusively on Telegram. That means no matter where you are, it's there to assist you in recording your expenses seamlessly.

<a href="https://dollarbotgroup28.my.canva.site/">Click here for a video overview!!</a>

<p align="center">
  <img src="https://github.com/KoruptTinker/DollarBot/blob/main/docs/DALL%C2%B7E%202024-10-31%2001.51.11%20-%20A%20cartoon-style%20illustration%20of%20a%20friendly%20robot%20for%20a%20financial%20management%20project.%20The%20robot's%20features%20are%20represented%20by%20shapes%2C%20symbolizing%20funct.webp" alt="DollarBot Illustration" width="400"/>
</p>



## Demo Video

<a href="https://www.youtube.com/watch?v=TtzeHElefbQ">https://www.youtube.com/watch?v=TtzeHElefbQ</a>


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

- **Discord Integration::** Integrated Discord to increase bot accessibility.
- **Better data storage::** Migrated from using a json file for storing data to MongoDB
- **Better secrets handling::** Removed all sensitive information like API Keys, Passwords, Connection URLs from the codebase to an env with a proper modular class to handle these secrets
- **Dockerization::** Dockerized the application to make deployments seamless.
- **Debugging issues and Better documentation::** Improved code for easier debugging and enhanced documentation to help developers maintain the project efficiently.

# :rocket: Installation and Setup

## Pre-requisite: An active Telegram account

Open up your terminal and let's get started:

### MacOS / Ubuntu Users

1. Clone this repository to your local system. 
```
   git clone https://github.com/KoruptTinker/DollarBot/
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

Once installed, run the following commands and follow the instructions on-screen to complete the installation.
```
  chmod a+x setup.sh
  bash setup.sh
```
There, all done!

## Getting Telegram BotToken:

Once you've executed setup.sh, and all dependencies have been installed, you can start running DollarBot by following these instructions.

1. Open the Telegram Desktop Application and sign in. Once inside Telegram, search for "BotFather". Click on "Start", and enter the following command:
```
  /newbot
```
2. Follow the instructions on screen and choose a name for your bot (e.g., `dollarbot`). After this, select a UNIQUE username for your bot that ends with "bot", for example: `dollarbot_<your_nickname>`.

3. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy and save this token for future use. Make sure you save this token– don't lose it!

4. In the repo directory (where you cloned it), run these commands.

## Obtaining Bot Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name your application[1]
3. Navigate to "Bot" section in left menu
4. Click "Add Bot"[4]
5. Click "Reset Token" then "Copy" to obtain your bot token[4]

> ⚠️ Never share your bot token with anyone!

### Inviting Bot to Server

1. Go to OAuth2 section in application settings
2. In OAuth2 URL Generator select:
   - `bot`
   - `applications.commands`[2]

3. Select required permissions for your bot

4. Use this invite link structure: 
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=0&scope=bot%20applications.commands

5. Replace `YOUR_CLIENT_ID` with your Application ID[3]
6. Open generated link in browser
7. Select target server (requires "Manage Server" permission)[2]
8. Click "Authorize"

Your bot should now appear in your server's member list!

### Required Intents

Enable these in Bot settings if needed:
- Server Members Intent
- Message Content Intent
- Presence Intent[1]


## Running DollarBot:

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

1. In the Telegram app, search for your newly created bot by entering your UNIQUE username and open the bot you created.

2. Now, on Telegram, enter the "/start" or "menu" command, and you are all set to track your expenses!

# :information_desk_person: Use Cases

Here's a quick overview of how each of the commands work. Simply enter /<command_name> into the Telegram chat and watch as the magic happens! 

### Menu
View all the commands Dollarbot offers to manage your expenses

[Click here to view the menu command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/menu_command.gif)

It can be invoked by using `/menu` command.

### Help
Display the list of commands.

[Click here to view the help command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/help_command.gif)
It can be invoked by using `/help` command.

### Pdf
Save history as PDF.

[Click here to view the pdf command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/pdf_command.gif)
It can be invoked by using `/pdf` command.

### Add
This option is for adding your expenses.

[Click here to view the add command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/add_command.gif)
1. It will give you the list of categories to choose from. <br> 
2. You will be prompted to enter the amount corresponding to your spending <br>      
3. The message will be prompted to notify the addition of your expense with the amount,date, time and category <br> 
4. It can be invoked by using `/add` command. 

### Analytics
This option gives user a graphical representation of their expenditures.

[Click here to view the Analytics command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/analytics.gif)
1. You will get an option to choose the type of data you want to see. <br> 
2. It can be invoked by using `/analytics` command.

### Predict
This option analyzes your recorded spendings and gives you a budget that will accommodate for them.

[Click here to view the Predict command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/predict_command.gif)
It can be invoked by using `/predict` command.

### History
This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spendings.
[Click here to view the History command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/history.gif)

It can be invoked by using `/history` command.

### Delete
This option is to Clear/Erase all your records.
[Click here to view the Delete command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/delete.gif)

It can be invoked by using `/delete` command.

### Edit
This option helps you to go back and correct/update the missing details    
[Click here to view the Edit command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/edit_command.gif)


1. It will give you the list of your expenses you wish to edit <br> 
2. It will let you change the specific field based on your requirements like amount/date/category <br> 
3. It can be invoked by using `/edit` command.

### Budget
This option is to set/update/delete the budget.     
[Click here to view the Budget command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/budget_command.gif)


1. The Add/update category is to set the new budget or update the existing budget <br>      
2. The view category gives the detail if budget is exceeding or in limit with the difference amount  <br>        
3. The delete category allows to delete the budget and start afresh! <br> 
4. It can be invoked by using `/budget` command.

### SendEmail
This option is to send you a email with you expenditures.
[Click here to view the SendEmail command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/send_mail.gif)


It can be invoked by using `/sendEmail` command.

### Weekly
This option is to get the weekly analysis report of the expenditure.
[Click here to view the Weekly command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/weekly.gif)

It can be invoked by using `/weekly` command.


### Monthly
This option is to get the monthly analysis report of the expenditure
[Click here to view the Monthly command GIF](https://github.com/KoruptTinker/DollarBot/blob/main/docs/workflows/monthly.gif)

It can be invoked by using `/monthly` command.


### Insight
This option is to spending insights feature for users.         
<p align="center"><img width="700" src="./docs/workflows/insight.gif"></p>

It can be invoked by using `/insight` command.


# :construction: What's Next

Some possible future enhancements are as follows:
1.	**Remove Dependency on Telegram:** Reshape the bot to be able to be used without having a telegram account. Allowing Discord users to access the functionality even when they don't have a Telegram account/
2.	**Smart Gamification:** Gamify spending and saving money by introducing smart challenges such as "No-Spend Weekends" or setting up saving goals and allowing users to achieve them on a weekly/monthly basis.
3.	**Cash Flow Analysis:** Gain insight into your cash flow by categorizing income and expenses. DollarBot helps you identify trends in your spending and income, giving you a monthly or weekly overview of your cash flow status. 
4.	**Year-End Financial Summary:** Receive a detailed financial summary at the end of each year, which includes total income, expenses by category, savings achieved, and insights on how spending changed over the months.
5.  **Multi-User spends:** Allow spends to be shared amongst users to allow proper splits and book-keeping of records.

:page_facing_up: License
---
This project is licensed under the terms of the MIT license. Please check [LICENSE](https://github.com/KoruptTinker/DollarBot/blob/main/LICENSE.md) for more details.

## Contributors
<table>
  <tr>
    <td align="center"><a href="https://github.com/KoruptTinker"><img src="./images/Brijesh.png" width="100px;" alt=""/><br /><sub><b>Brijesh Kumar Bhayana</b></sub></a></td>
    <td align="center"><a href="https://github.com/VidhishaKamat"><img src="https://avatars.githubusercontent.com/VidhishaKamat" width="100px;" alt=""/><br /><sub><b>Vidhisha Kamat</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/Abhi0010"><img src="./images/Abhishek.png" width="100px;" alt=""/><br /><sub><b>Abhishek Potdar</b></sub></a><br /></td>
  </tr>
</table>

For any support, email us at `dollarbot_ncsu@protonmail.com`
