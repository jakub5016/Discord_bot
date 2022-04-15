# bot.py
import argparse
import os

import discord
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ext import commands,tasks
import urllib
import re
import os
import youtube_dl
import pafy
import requests


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

#Youtube settings 
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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
async def play(ctx, msg):
    if not ctx.message.author.voice:
        await ctx.send("Sorry but you're not connected to any channel")
        return
    else:
        if msg:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            
            server = ctx.message.guild
            voice_channel = server.voice_client


            song = pafy.new(msg)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source
            
            
            
            voice_channel.play(discord.FFmpegPCMAudio(source=audio.url, **FFMPEG_OPTIONS))  # play the source
            
            await ctx.send("Currently playing:")
            await ctx.send(msg)

bot.run(TOKEN) #join server as bot