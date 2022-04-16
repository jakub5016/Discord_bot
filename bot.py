# bot.py
import argparse
from glob import glob
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
queue_titles = []
wantToSkip = False


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
    queue_titles.clear()

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
            queue_titles.append(song.title)

            await ctx.send("Adding to queue:")
            await ctx.send(song.title)
            if not (ctx.voice_client.is_playing()):
                await play(ctx=ctx)


async def play(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    global queue
    global queue_time
    global queue_titles

    theteIsMore = True
    global wantToSkip
    i = 0 
    while theteIsMore and (not wantToSkip): #main loop while plaing
        
        while (ctx.voice_client.is_playing() and (not wantToSkip)):
            await asyncio.sleep(1)
        
        if i >= len(queue):
            theteIsMore = False
        
        if wantToSkip: #If you want to skip there is exception
            if i == len(queue): #If you are at the end, just clear queue
                queue.clear()
                queue_time.clear()
                queue_titles.clear()
            voice_channel.stop() #Stop music and go to next song
            wantToSkip = False
        
        try:
            source = discord.FFmpegPCMAudio(source=queue[i], **FFMPEG_OPTIONS)
            voice_channel.play(source=source, after=voice_channel.stop())
        except:
            queue.clear()
            queue_time.clear()
            queue_titles.clear()
        finally:
            i += 1
            time.sleep(2)
    

@bot.command(name='que', help='Showing a queue')
async def queue_check(ctx):
    for i in range(len(queue_titles)):
        await ctx.send(str(i+1) + ' ' + queue_titles[i])

@bot.command(name='skip', help='Adding song to queue')
async def skip_song(ctx):
    global wantToSkip
    wantToSkip= True
bot.run(TOKEN) #join server as bot