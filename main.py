import os, platform
def clear():
    if platform.system().lower()=="windows":
        os.system('cls')
    else:
        os.system('clear')

if platform.system().lower()=="windows":
    ossys = "python.exe -m pip install"
else:
    ossys = "python3 -m pip install"

dir = os.path.dirname(os.path.realpath(__file__))
wdir = os.getcwd()
if dir != wdir:
    os.chdir(dir)

try:
    import discord, requests
except ImportError:
    os.system(f"{ossys} discord requests"), clear()
import requests
import discord
from discord.ext import tasks, commands
if str(os.path.exists("config.py")) == "False":
    print("config.py not detected! \n Creating config.py.")
    Token = input("Token: ")
    Channel = input("Channel: ")
    RoleID = input("(If empty will @everyone) RoleID: ")
    Seconds = input("(In seconds how often bot will check for updates) Seconds: ")
    Prefix = input("Prefix: ")
    with open("config.py", "w") as file:
        file.write(f'Token = "{Token}" \nChannel = "{Channel}" \nRoleID = "{RoleID}" \nSeconds = "{Seconds}" \nPrefix = "{Prefix}"')
    file.close
from config import Token, Channel, RoleID, Seconds, Prefix
intents = discord.Intents.all()
client = commands.Bot(command_prefix=str(Prefix),intents=intents)
Seconds = int(Seconds)

print("Original Code Created by: MirayXS/Shin#6327 Edited by Pakyu!#6228")
print("To change the config delete config.py or edit it!")

@client.event
async def on_ready():
    if Seconds < 60:
        await client.change_presence(activity=discord.Game(name=f"Checking for Roblox Updates {Seconds}sec Intervals"))
    else:
        min = (Seconds // 60)
        await client.change_presence(activity=discord.Game(name=f"Checking for Roblox Updates {min}min Intervals"))
    try:
        await client.tree.sync()
    except Exception as Error:
        print(Error)
    print('<----------- NEW SESSION ----------->')
    print('[SUCCESS] : Logged in as ' + format(client.user))
    print('<----------------------------------->\n\n')
    await robloxgameclient_loop.start()

# RobloxGameClient
@tasks.loop(seconds=Seconds)
async def robloxgameclient_loop():
    print(f"Checking for Roblox Update...")
    file = open("Version.txt", "r")
    fileread = file.readlines()
    oldData = "".join(str(x) for x in fileread)
    newData = requests.get('http://setup.roblox.com/version') # This is the endpoint where Roblox updates their version number. This is new data. 
    if oldData == "":
        print("[EMPTY] ( [X] ) Version.txt is Empty Will Set to the Latest Version.")
        with open("Version.txt", "w") as file:
                file.write(str(newData.text))
    elif str(newData.text) in str(oldData): # if the new data is the same as the old data...
        print("[CLEARED] ( [✓] ) No New RobloxGameClient Version!\n")
    elif str(newData.text) not in str(oldData): # if the new data is **not** the same as the old data...
        print("[FAILED] ( [X] ) New RobloxGameClient Version!\n")
        print("New RobloxGameClient Version: "+ newData.text)
        print("-------------------------------------")
        print("Old RobloxGameClient Version: "+ oldData)
        print("-------------------------------------")
        channel = client.get_channel(int(Channel))
        if RoleID == "":
            await channel.send(f"||<@everyone>|| \n```Roblox has been updated!!! \nPrevious Version: {oldData} \nUpdated Version: {newData.text}```")
        else:
            await channel.send(f"||<@{str(RoleID)}>|| \n```Roblox has been updated!!! \nPrevious Version: {oldData} \nUpdated Version: {newData.text}```")
        with open("Version.txt", "w") as file:
            file.write(str(newData.text))
    file.close

# Use this command to ping the bot, or to know if the bot crashed.  
@client.hybrid_command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.hybrid_command(pass_context=True)
async def version(ctx):
    newData = requests.get('http://setup.roblox.com/version')
    await ctx.send(f"Latest Version: {newData.text}")

# RobloxGameClient - before_loop
@robloxgameclient_loop.before_loop
async def before_some_task():
  await client.wait_until_ready()

client.run(Token)
