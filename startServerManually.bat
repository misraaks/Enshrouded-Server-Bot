@echo off

cd C:\Enshrouded-Server-Bot

echo Checking for updates...
cd .\steamcmd\
steamcmd.exe +login anonymous +app_update 2278520 +quit

echo Launching server
cd .\steamapps\common\EnshroudedServer
start enshrouded_server.exe