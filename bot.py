import asyncio
import re
import threading
import discord
import subprocess
import os

from discord.ext import commands

import requests
import shutil
from datetime import datetime

#==-----------------------------------------==#
# EDIT THE VALUES BELOW                       #
# See README.md for more information          #
#                                             #
# Your bot's token                            #
TOKEN = ''
#                                             #
# Server update script file                   #
SERVER_UPDATE_BIN = './steamcmd/steamcmd.exe'
SERVER_UPDATE_ARGUMENTS = '+login anonymous +app_update 2278520 +quit'
#                                             #
# Server start script file                    #
SERVER_START_BIN = './steamcmd/steamapps/common/EnshroudedServer/enshrouded_server.exe'
#                                             #
# Savegame file backup location               #  
SAVEGAME_BACKUP_PATH = ''
#                                             #
# The role allowed to start the server        #
BOT_MASTER = '@everyone'                      #
#                                             #
#==-----------------------------------------==#

SERVER_START_COMMAND = [SERVER_START_BIN]
SERVER_UPDATE_ARGUMENTS_LIST = SERVER_UPDATE_ARGUMENTS.split()
SERVER_UPDATE_COMMAND = [SERVER_UPDATE_BIN] + SERVER_UPDATE_ARGUMENTS_LIST

# Init Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Init server process and status
server_process = None
server_running = False
server_update_process = None
server_updating = False

# Prevent concurrent access to server_process
server_lock = threading.Lock()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

@bot.command()
async def startserver(ctx):
    global server_process, server_running, server_update_process, server_updating

    # Check if the user has the 'BOT_MASTER_ROLE_NAME' role
    bot_master_role = discord.utils.get(ctx.guild.roles, name=BOT_MASTER)
    if bot_master_role not in ctx.author.roles:
        await ctx.send("You don't have permission to start the server.")
        return

    # Check if the server is already running
    if server_updating:
        await ctx.send("The server is updating...please wait a few minutes and try again.")
        return
    
    # Check if the server is already running
    if server_running:
        await ctx.send("The server is already running.")
        return

    # Start the server and update asynchronously
    # await ctx.send("Updating and starting server...")
    try:
        # Create a backup of the savefile before starting the server
        await ctx.send("Creating savegame backup...")
        backup_filename = f"3ad85aea.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        backup_file = os.path.join(SAVEGAME_BACKUP_PATH, backup_filename)
        shutil.copy('./steamcmd/steamapps/common/EnshroudedServer/savegame/3ad85aea', backup_file)
        await ctx.send(f"Backup {backup_filename} complete!")

        # Update the server software
        await ctx.send("Updating server...")
        with server_lock:
            # Update server
            server_update_process = await asyncio.create_subprocess_exec(
                *SERVER_UPDATE_COMMAND,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(SERVER_UPDATE_BIN),
                universal_newlines=False,
            )
            server_updating = True

            # Wait for the update process to complete
            _, _ = await server_update_process.communicate()
            return_code = server_update_process.returncode
            server_updating = False

            if return_code != 0:
                await ctx.send(f"Server update failed with return code {return_code}.")
                return
            await ctx.send("Update complete!")
            
            # Start server
            await ctx.send("Starting server...")
            server_process = await asyncio.create_subprocess_exec(
                *SERVER_START_COMMAND,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(SERVER_START_BIN),
                universal_newlines=False,
            )

        server_running = True

        # Print server output to the console
        while server_running:
            stdout_line = await server_process.stdout.readline()
            if not stdout_line:
                break
            stdout_line = stdout_line.decode("utf-8").strip()
            print(stdout_line)

            # Check if the line matches the server startup completion pattern
            if re.search(r"HostOnline", stdout_line):
                public_ip = requests.get('https://api.ipify.org').text
                await ctx.send(f"Server is up and running at {public_ip}:15637")

        await ctx.send("Server has stopped.")
        server_running = False

    except Exception as e:
        await ctx.send(f"An error occurred while updating/starting the server: {e}")

@bot.command()
async def stopserver(ctx):
    global server_process, server_running

    # Check if the user has the 'BOT_MASTER_ROLE_NAME' role
    bot_master_role = discord.utils.get(ctx.guild.roles, name=BOT_MASTER)
    if bot_master_role not in ctx.author.roles:
        await ctx.send("You don't have permission to stop the server.")
        return

    # Check if the server is running
    if not server_running:
        await ctx.send("The server is not running.")
        return

    # Stop the server
    await ctx.send("Stopping server...")
    try:
        server_process.terminate()
        try:
            asyncio.wait_for(server_process.wait(), timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Server did not stop gracefully. Forcefully terminating.")
            server_process.kill()
        server_running = False

        # Create a backup of the savefile after stopping the server
        await ctx.send("Creating savegame backup...")
        backup_filename = f"3ad85aea.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        backup_file = os.path.join(SAVEGAME_BACKUP_PATH, backup_filename)
        shutil.copy('./steamcmd/steamapps/common/EnshroudedServer/savegame/3ad85aea', backup_file)
        await ctx.send(f"Backup {backup_filename} complete!")
        
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the server: {e}")

# Function to read console commands from the terminal
# (I didn't write this, and I don't think this does anything for Enshrouded)
# (but I'm keeping it here from the original Minecraft bot code code I stole....)
def read_console_input():
    global server_process, server_running
    while True:
        try:
            if server_running:
                command = input()
                with server_lock:
                    server_process.stdin.write((command + "\n").encode('utf-8'))
                    
        except KeyboardInterrupt:
            # Stop the server
            print("Stopping server...")
            server_process.terminate()
            try:
                asyncio.wait_for(server_process.wait(), timeout=30)
            except asyncio.TimeoutError:
                print("Server did not stop gracefully. Forcefully terminating.")
                server_process.kill()

if __name__ == "__main__":
    # Check if the server start script exists
    if not os.path.exists(SERVER_START_BIN):
        print(f"Server start binary not found.")
        sys.exit()

    # Check if the server update script exists
    if not os.path.exists(SERVER_UPDATE_BIN):
        print(f"Server update binary not found.")
        sys.exit()
    
    # Check if the savegame backup path exists
    if not os.path.exists(SAVEGAME_BACKUP_PATH):
        print(f"Savegame backup path not found.")
        sys.exit()

    # Start a thread to read console input
    console_input_thread = threading.Thread(target=read_console_input)
    console_input_thread.daemon = True
    console_input_thread.start()
    
    bot.run(TOKEN)
