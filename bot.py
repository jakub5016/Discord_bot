# bot.py
import argparse
import os
from socket import timeout
from termios import CLNEXT
import time
from waiting import wait, TimeoutExpired
import asyncio

import discord
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ext import commands,tasks
import urllib
import re
import youtube_dl
import pafy
import requests

queue = []
queue_time = []

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
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)#set format options


load_dotenv() #load an env
TOKEN = os.getenv('DISCORD_TOKEN')#get token

bot = commands.Bot(command_prefix='!')#set prefix

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
    queue.clear()
    queue_time.clear()

@bot.command(name='add', help='Adding song to queue')
async def add(ctx, msg):
    if not ctx.message.author.voice:
        await ctx.send("Sorry but you're not connected to any channel")
        return
    else:
        try:
            await join(ctx=ctx)
        finally:

            server = ctx.message.guild
            voice_channel = server.voice_client


            song = pafy.new(msg)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source

            queue.append(audio.url)
            queue_time.append(song.length)

            await ctx.send("Adding to queue:")
            await ctx.send(song.title)

@bot.command(name='play', help='Adding song to queue')
async def play(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    i = 0
    while i <= (len(queue) - 1):
        if not ctx.voice_client.is_playing():
            await ctx.send("On a headphones right now: " + queue[1])
            voice_channel.stop()
            voice_channel.play(discord.FFmpegPCMAudio(source=queue[i], **FFMPEG_OPTIONS))
        else:
            await ctx.send(i)
            while ctx.voice_client.is_playing():
                time.sleep(5)

            voice_channel.play(discord.FFmpegPCMAudio(source=queue[i], **FFMPEG_OPTIONS))
        await ctx.send(i)
        i += 1

bot.run(TOKEN) #join server as bot