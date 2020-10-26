import discord 
from discord.ext import commands
from config import *  
import datetime as dt

# Initiating bot with prefix '$'
client = commands.Bot(command_prefix='$')

# Initiating ban wave times
banStart = (dt.datetime.now().hour, dt.datetime.now().minute) 
banEnd = (dt.datetime.now().hour, dt.datetime.now().minute)

# Initiating affected member list
memebers = []

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def setStart(ctx, *, time):
    time = dt.datetime.strptime(time, '%H:%M')
    banStart = (time.hour, time.minute)
    await ctx.send(f'Ban wave will now start at {banStart[0]}:{banStart[1]}')

@client.command()
async def setEnd(ctx, *, time):
    time = dt.datetime.strptime(time, '%H:%M')
    banEnd = (time.hour, time.minute)
    await ctx.send(f'Ban wave will now start at {banEnd[0]}:{banEnd[1]}')




if __name__ == '__main__':
    client.run(token)