# Installation and Setup
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

```Note```: It will ask you to paste the API token you received from Telegram while creating your bot (Step 3), so keep that handy.
A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

5. In the Telegram app, search for your newly created bot by entering your UNIQUE username and open the bot you created.

6. Now, on Telegram, enter the "/start" or "menu" command, and you are all set to track your expenses!