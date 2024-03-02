const { Client, GatewayIntentBits } = require('discord.js');
const { spawn, spawnSync } = require('child_process');
require('dotenv').config();
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');

// Change these with relative paths to your files
const updateBin = './steamcmd/steamcmd.exe'
const serverBin = './steamcmd/steamapps/common/EnshroudedServer/enshrouded_server.exe'
const fileToBackup = './steamcmd/steamapps/common/EnshroudedServer/savegame/3ad85aea'
const backupDirectory = 'D:/OneDrive/Documents/EnshroudedServerSaves/'
const serverQueryPort = 15637

// Other Globals
const prefix = '$';
let updateProcess = null;
let serverProcess = null;

// ### FUNCTION DEFINITIONS ###
async function getPublicIP() {
  try {
    response = await fetch('https://api.ipify.org?format=json');
    data = await response.json();
    return data.ip;
  } catch (error) {
    console.error(`Error fetching public IP: ${error.message}`);
    return null;
  }
}

async function sendPublicIPMessage(message) {
  publicIP = await getPublicIP();
  if (publicIP) {
    message.channel.send(`Server is up and running at ${publicIP}:${serverQueryPort}`);
  } else {
    message.channel.send('Error retrieving public IP. Server started without IP information.');
  }
}

function updateServer(message) {
  return new Promise((resolve, reject) => {
    message.channel.send("Updating server...").then(() => {
      updateProcess = 1;
      updateResult = spawnSync(updateBin, ['+login', 'anonymous', '+app_update', '2278520', '+quit']);
      if (updateResult.status === 0) {
        updateProcess = null;
        message.channel.send("Update complete!").then(resolve);
      } else {
        updateProcess = null;
        errorMessage = `Update process failed with code ${updateResult.status}`;
        console.error(errorMessage);
        message.channel.send('Update process failed.').then(reject);
      }
    });
  });
}

async function updateAndStartServer(message) {
  try {
    await updateServer(message);
    message.channel.send("Starting server...").then(() => {
      serverProcess = spawn(serverBin);
      serverProcess.on('close', (code) => {
        console.log(`Server process exited with code ${code}`);
      });
      sendPublicIPMessage(message);
    });
  } catch (error) {
    console.error(`Error during update and server start: ${error.message}`);
    message.channel.send('Server not started due to an error.');
  }
}

function backupFile(filePath, backupDir, message) {
  const fileName = path.basename(filePath);
  timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);;
  backupPath = path.join(backupDir, `${timestamp}_${fileName}.bak`);

  try {
    message.channel.send("Creating savegame backup...");
    fs.copyFileSync(filePath, backupPath);
    console.log(`File backed up to ${backupPath}`);
    message.channel.send("Backup complete!");
  } catch (error) {
    console.error(`Error backing up file: ${error.message}`);
    message.channel.send("Error backing up savegame.");
  }
}
// ### END FUNCTION DEFINITIONS ###

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
      ],
});

client.once('ready', () => {
  console.log('Bot is ready!');
});

client.on('messageCreate', (message) => {
  if (!message.content.startsWith(prefix) || message.author.bot) return;

  // Ping Pong
  if (message.content.startsWith(`${prefix}ping`)) {
    message.channel.send('pong!');
  }

  // $startserver
  else if (message.content.startsWith(`${prefix}startserver`)) {
    if (updateProcess) {
      message.channel.send('The server is updating...please wait a few minutes and try again.');
      return;
    } else
    if (serverProcess) {
      message.channel.send('The server is already running.');
      return;
    }
    
    // Backup the save file before starting the server 
    backupFile(fileToBackup, backupDirectory, message);

    // Call the async update and start server function
    updateAndStartServer(message);
  }
  
  // $stopserver
  else if (message.content.startsWith(`${prefix}stopserver`)) {
    if (serverProcess) {
      serverProcess.kill();
      serverProcess = null;
      message.channel.send('The server has stopped.');
    } else {
      message.channel.send('The server is not running.');
    }
  }
});

// Make sure you have an .env file with BOT_TOKEN=<yourBotToken>
client.login(process.env.BOT_TOKEN);
