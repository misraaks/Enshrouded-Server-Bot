# Enshrouded-Server-Bot
A Discord bot that allows channel members to start and stop an Enshrouded server (running on the same PC as the bot.)

I made both Python and JavaScript implementations...although the JavaScript implementation needs work. There are intermittent connection issues when the server is started by the JavaScript bot.

## Python Bot Setup
1. Install Enshrouded server using steamcmd, as described [here](https://hub.tcno.co/games/enshrouded/dedicated_server/). 
2. Check the global variables in `bot.py` and edit them to your liking. Also edit the path to your server savegame file in the `shutil.copy` line (around line 84.)
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
6. Install python and the bot's dependencies (run from a command prompt in the project directory):
```
pip install discord.py requests python-dotenv
```
7. Again, from a command prompt in this directory, run the bot with `python3 .\bot.py`.
8. Start your Enshrouded server in Discord using `$startserver`. Stop it with `$stopserver`.

## JavaScript Bot Setup
1. Install Enshrouded server using steamcmd, as described [here](https://hub.tcno.co/games/enshrouded/dedicated_server/). 
2. Check the global variables in `bot.js` and edit them to your liking.
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

### Installing the JavaScript bot as a Windows Service (Optional)
1. In this directory, run `npm install node-windows`.
2. Edit `installWindowsService.js` to your liking. The service name and description are purely cosmetic.
3. In this directory, run `node installWindowsService.js install`.
4. Now your Discord bot will run in the background whenever you first log into Windows.
5. The service can be restarted or stopped from the Windows `services.msc` menu.
6. To remove the service, run `node uninstallWindowsService.js uninstall`. 
7. I don't know if `node-windows` will automatically update the service whenever you make changes to your `bot.js` file, so I'd uninstall and reinstall the service whenever I make changes.

## Troubleshooting
1. Be sure to run `EnshroudedServer.exe` manually at least once once you decide on its filepath. This will cause Windows Firewall to prompt you to allow the inbound connections. You will need to do this again if you ever relocate the executable.
2. Try double clicking `startServerManually.bat` to update and start your server manually, then see if you can connect.