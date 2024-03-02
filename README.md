# Enshrouded-Server-Bot
A Discord bot that allows channel members to start and stop an Enshrouded server (running on the same PC as the bot.)

## Setup
1. Install Enshrouded server using steamcmd, as described [here](https://hub.tcno.co/games/enshrouded/dedicated_server/). 
2. Check the global variables in `bot.js` and edit them to your liking. I put the `steamcmd` folder in the same folder as `bot.js` itself. Even if you put `steamcmd` in the same folder, you still need to check and edit `backupDirectory` and `serverQueryPort` to match your server and preferences.
3. Setup your Discord bot (instructions copied from Stonley890's [mc-console-bot](https://github.com/Stonley890/mc-console-bot))
    1. Go to https://discord.com/developers/applications and create a new application. Give it any name, description, or icon.
    2. Go to the **Bot** tab and create a bot. Give it a name.
    3. Under the **OAuth2** tab, go to **URL Generator**. Check the _bot_ box. In the second table, check the _Read Messages/View Channels_ box.
    4. Scroll down and look for MESSAGE CONTENT INTENT under _Privileged Gateway Intents_. Enable the toggle.
    5. Copy the URL and open it. Invite the bot to your server. Go back to the **Bot** tab and find the _Bot Token_. Reset and copy it. We'll need it later.
4. Create a .env file that looks like this (no single or double quotes needed...but do remove the angle brackets):
```
BOT_TOKEN=<YOUR_TOKEN_HERE>
```
5. Add bot to your server using the previously noted URL.
6. Install node.js and the bot's dependencies:
```
npm install child_process
npm install discord.js
npm install dotenv
npm install fs
npm install node-fetch@2
```
7. Run the bot with `node .\bot.js` (TODO: Maybe make this a Windows service or put it in the startup folder, who knows)
8. Test your bot in Discord by sending `$ping` in a channel the bot is in. The bot will respond `pong!`
9. Start your Enshrouded server using `$startserver`. Stop it with `$stopserver`
