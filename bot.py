from datetime import datetime
import discord 
from discord.ext import commands, tasks
from config import *  
import datetime as dt
import time 

# Initiating bot with prefix '$'
client = commands.Bot(command_prefix='$')

# Initiating ban wave times
banStart = []
banEnd = []

# Initiating affected member list
members = []

main_channel = general_table

@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def setStart(ctx, *, time):
    global banStart
    time = dt.datetime.strptime(time, '%H:%M')
    banStart = [time.hour, time.minute]
    await ctx.send(f'Ban wave will now start at {banStart[0]}:{banStart[1]}')

@client.command()
async def setEnd(ctx, *, time):
    global banEnd
    time = dt.datetime.strptime(time, '%H:%M')
    banEnd = [time.hour, time.minute]
    await ctx.send(f'Ban wave will now end at {banEnd[0]}:{banEnd[1]}')

@client.command()
async def banUsers(ctx):
    for member in members:
        try: 
            await ctx.guild.ban(member)
            await ctx.send(f'Removed {member} until {banEnd[0]}:{banEnd[1]}')
        except: 
            await ctx.send(f'Failed to remove {member}')



@client.command()
async def unbanUsers(ctx):
    for member in members:
        try:
            await ctx.guild.unban(member)
            await ctx.invoke(client.get_command('inviteUser'), user=member)
            await ctx.send(f'Invited {member} until {banStart[0]}:{banStart[1]}')
        except:
            await ctx.send(f'Failed to unban/invite {member}')

@client.command()
async def addUser(ctx, *, user:discord.Member):
    members.append(user)
    await ctx.send(f'Added user {user}')

@client.command()
async def removeUser(ctx, *, user:discord.Member):
    members.remove(user)
    await ctx.send(f'Removed user {user}')

@client.command()
async def getUsers(ctx):
    for member in members:
        await ctx.send(member.name)

@client.command()
async def inviteUser(ctx, *, user: discord.Member):
    link = await ctx.channel.create_invite(max_use=1) # make this max_use = 1
    await user.send(str(link))

@client.command()
async def clear(ctx):
    await ctx.channel.purge()
    await ctx.send('Deleted last 100 messages')


@client.command()
async def init(ctx):
    print("Main loop has started!")
    print(members)
    print(banStart, banEnd)
    while(True):
        now = dt.datetime.now()
        now = [now.hour, now.minute]
        print(f"The time now: {now}\nThe time to ban: {banStart}\nThe time to unban: {banEnd}")
        if(now == banStart):
            await ctx.invoke(client.get_command('banUsers'))
            print(f"Banned at {now}")
        elif(now == banEnd):
            await ctx.invoke(client.get_command('unbanUsers'))
            print(f"Unbanned at {now}")

        time.sleep(30)



if __name__ == '__main__':
    client.run(token)
    
    
    