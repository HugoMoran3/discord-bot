import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from asyncio import sleep
import  time
import os



TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = "!",)

channel_id = 862961024931725314

# get localtime, create
curr_time = time.localtime()
curr_clock = time.strftime("The time is %H:%M:%S", curr_time)
trigger = curr_time.tm_min == 00
print(trigger)
print(curr_clock)

@client.event
async def on_ready():
    channelGot = client.get_channel(channel_id)
    @tasks.loop(seconds=3.0)
    async def joiner():
        print("joiner")
        voice = await channelGot.connect()
        source = FFmpegPCMAudio('bigben.mp3')
        player = voice.play(source)
    joiner.start()




@client.command()
async def channels(ctx):
    voice_channel_list = ctx.guild.voice_channels
    print(voice_channel_list[0])
    channelname = voice_channel_list[0]
    print(voice_channel_list)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )



@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('bigben.mp3')
        player = voice.play(source)
        while voice.is_playing():
            await sleep(1)
        await voice.disconnect()
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")



@client.command(pass_context = True)
async def leave(ctx): 
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

def timetracker():  
    if trigger == True:
        alarm()
    else:
        print("It's not time for big ben")

@tasks.loop(seconds=1)
async def alarm():
    print("Joined channel")
    channel = client.get_channel(channel_id)
    join()
    print("Joined channel")



client.run(TOKEN)


