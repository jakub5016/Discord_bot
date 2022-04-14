# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands,tasks
import os

load_dotenv() #load an env
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Sorry but you're not connected to any channel")
        return
    else:
         channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Tells the bot to leave the current voice channel')
async def leave(ctx):
    channel = ctx.guild.voice_client
    await channel.disconnect()
    await ctx.send('Bye bye :wave:')

@bot.command(name='play', help='Tells the bot to join the voice channel, and play music')
async def play(ctx, arg):
    if not ctx.message.author.voice:
        await ctx.send("Sorry but you're not connected to any channel")
        return
    else:
        if arg:
            channel = ctx.message.author.voice.channel
            await ctx.send("Currently playing:")
            await ctx.send(arg)
        else:
            await join()
            await ctx.send("What music you want me to play?")
    await channel.connect()

bot.run(TOKEN) #join server as bot