import requests
import discord
import os
from discord.ext import tasks, commands
import Config as con
intents = discord.Intents.all()
client = commands.Bot(command_prefix=";",intents=intents)

print("Original Code Created by: MirayXS/Shin#6327 Edited by Pakyu!#6228")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"Checking for Roblox Updates 10min Intervals"))
    try:
        await client.tree.sync()
    except Exception as Error:
        print(Error)
    print('<----------- NEW SESSION ----------->')
    print('[SUCCESS] : Logged in as ' + format(client.user))
    print('-------------------------------------\n\n')
    await robloxgameclient_loop.start()

# RobloxGameClient
@tasks.loop(seconds=int(con.Seconds))
async def robloxgameclient_loop():
    os.chdir("RoUpdates-Revamped")
    file = open("Version.txt", "r")
    fileread = file.readlines()
    oldData = "".join(str(x) for x in fileread)
    newData = requests.get('http://setup.roblox.com/version') # This is the endpoint where Roblox updates their version number. This is new data.
    print(f"Checking for Roblox Update...")
    if oldData == "":
        print("[EMPTY] ( [X] ) Version.txt is Empty Will Set to the Latest Version.")
        with open("Version.txt", "w") as file:
            file.write(str(newData.text))
    elif str(newData.text) in oldData: # if the new data is the same as the old data...
        print("[CLEARED] ( [✓] ) No New RobloxGameClient Version!")
    elif str(newData.text) not in oldData: # if the new data is **not** the same as the old data...
        print("[FAILED] ( [X] ) New RobloxGameClient Version!\n")
        print("New RobloxGameClient Version: "+newData.text)
        print("-------------------------------------")
        print("Old RobloxGameClient Version: "+oldData)
        print("-------------------------------------")
        channel = client.get_channel(int(con.Channel))
        if con.RoleID == "":
            await channel.send(f"||<@&@everyone>|| \n```Roblox has been updated!!! \nPrevious Version: {oldData} \nUpdated Version: {newData.text}```")
        elif con.RoleID == "PASTE HERE":
            await channel.send(f"||<@&@everyone>|| \n```Roblox has been updated!!! \nPrevious Version: {oldData} \nUpdated Version: {newData.text}```")
        else:
            await channel.send(f"||<@&{str(con.RoleID)}>|| \n```Roblox has been updated!!! \nPrevious Version: {oldData} \nUpdated Version: {newData.text}```")
        with open("Version.txt", "w") as file:
             file.write(str(newData.text))
    file.close

# Use this command to ping the bot, or to know if the bot crashed.  
@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.command(pass_context=True)
async def version(ctx):
    newData = requests.get('http://setup.roblox.com/version')
    await ctx.send(f"Latest Version: {newData.text}")

@client.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.tree.command(name="version")
async def ping(interaction: discord.Interaction):
    newData = requests.get('http://setup.roblox.com/version')
    await interaction.response.send_message(f"Latest Version: {newData.text}")

# RobloxGameClient - before_loop
@robloxgameclient_loop.before_loop
async def before_some_task():
  await client.wait_until_ready()

client.run(con.Token)
