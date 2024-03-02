# Enshrouded-Server-Bot
A Discord bot that allows channel members to start and stop an Enshrouded server (running on the same PC as the bot.)


## Setup
1. Install Enshrouded server using steamcmd, as described [here](https://hub.tcno.co/games/enshrouded/dedicated_server/). 
2. Check the global variables in `bot.js` and edit them to your liking. I put the `steamcmd` folder in the same folder as `bot.js` itself. Even if you put `steamcmd` in the same folder, you still need to check and edit `backupDirectory` and `serverQueryPort` to match your server and preferences.
2. Follow instructions [here](https://github.com/Stonley890/mc-console-bot) to setup a Discord bot with message read permissions. Make note of your Discord bot token and URL.
3. Create a .env file that looks like this:
```
BOT_TOKEN=<YOUR_TOKEN_HERE>
```
4. Add bot to your server using the previously noted URL. I didn't bother putting any permissions in the bot code for who in the Discord server can start and stop the server...you can look at Stonely890's Minecraft bot for inspiration on restricting bot access by Discord server roles.
5. Install node.js and the bot's dependencies:
```
npm install child_process
npm install discord.js
npm install dotenv
npm install fs
npm install node-fetch@2
```
6. Run the bot with `node .\bot.js` (TODO: Maybe make this a Windows service or put it in the startup folder, who knows)
7. Test your bot in Discord by sending `$ping` in a channel the bot is in. The bot will respond `pong!`
8. Start your Enshrouded server using `$startserver`. Stop it with `$stopserver`
