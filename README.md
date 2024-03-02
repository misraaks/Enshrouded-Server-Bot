# Enshrouded-Server-Bot
A Discord bot that allows channel members to start and stop an Enshrouded server (running on the same PC as the bot.)

## Setup
1. Install Enshrouded server using steamcmd, as described [here](https://hub.tcno.co/games/enshrouded/dedicated_server/). 
2. Check the global variables in `bot.js` and edit them to your liking. The paths can (and probably should) be relative to the `bot.js` script itself. For my setup, I put my `steamcmd` folder containing the Enshrouded install in this project directory. Even if you also put your `steamcmd` folder in this folder, you still need to edit `backupDirectory` and `serverQueryPort` to match your preferences and server settings.
3. Setup your Discord bot (instructions copied from Stonley890's [mc-console-bot](https://github.com/Stonley890/mc-console-bot))
    1. Go to https://discord.com/developers/applications and create a new application. Give it any name, description, or icon.
    2. Go to the **Bot** tab and create a bot. Give it a name.
    3. Under the **OAuth2** tab, go to **URL Generator**. Check the _bot_ box. In the second table, check the _Read Messages/View Channels_ box.
    4. Scroll down and look for MESSAGE CONTENT INTENT under _Privileged Gateway Intents_. Enable the toggle.
    5. Copy the URL and open it. Invite the bot to your server. Go back to the **Bot** tab and find the _Bot Token_. Reset and copy it. We'll need it later.
4. Create a file named `.env` in this project directory that looks like this (no single or double quotes needed around your token...but do remove the angle brackets):
```
BOT_TOKEN=<YOUR_TOKEN_HERE>
```
5. Add your bot to your Discord server using the previously noted URL.
6. Install node.js and the bot's dependencies (run from a command prompt in the project directory):
```
npm install child_process
npm install discord.js
npm install dotenv
npm install fs
npm install node-fetch@2
```
7. Again, from a command prompt in this directory, run the bot with `node .\bot.js`.
8. Test your bot in Discord by sending `$ping` in a channel the bot is in. The bot will respond `pong!`.
9. Start your Enshrouded server in Discord using `$startserver`. Stop it with `$stopserver`.

## Installing as a service (optional)
1. In this directory, run `npm install node-windows`.
2. Edit `installWindowsService.js` to your liking. The service name and description are cosmetic, but the script path needs to match where you set up your project folder. I don't know if this path can be relative to `installWindowsService.js` itself, so I'm using the absolute path.
3. In this directory, run `node installWindowsService.js install`
4. Now your Discord bot will run in the background whenever you first log into Windows.
5. The service can be restarted or disabled from the Windows `services.msc` menu.
6. I don't fully understand how to use `node-windows` to uninstall the service, so I'll just use `sc.exe delete <Service_Name>` if I ever want to remove the Windows service, and then just delete the `daemon` directory that gets created in this directory.
