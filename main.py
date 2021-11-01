import mtoken
import requests
import json
import discord
from discord.ext import commands
import youtube_dl
import asyncio
client = commands.Bot(command_prefix="!")
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
}
Music_list={}
async def connect(ctx):
    global Music_list
    Voice_Chanels = ctx.guild.voice_channels
    for Voice_Chanel in Voice_Chanels:
        if ctx.author.id in Voice_Chanel.voice_states:
            current_Voice = Voice_Chanel
    if ctx.guild.id not in Music_list:
        print(ctx.guild.id)
        Music_list[ctx.guild.id] = []
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(current_Voice)
    await current_Voice.connect()

@client.command()
async def p(ctx, url : str, is_loop=False):
    global ydl_opts, Music_list
    await connect(ctx)

    ytdl = youtube_dl.YoutubeDL(ydl_opts)
    data = ytdl.extract_info(url, download=False)
    print(data['url'])
    Music_list[ctx.guild.id].append(data['url'])
    await ctx.send("Music add")
    while True:
        try:
            if ctx.voice_client.is_playing():
                await asyncio.sleep(2)
                continue
            else:
                try:
                    url = Music_list[ctx.guild.id].pop()
                    ctx.voice_client.play(discord.FFmpegPCMAudio(url),after=lambda e: print(f'Player error: {e}') if e else None)
                except IndexError:
                    break
        except AttributeError:
            break


@client.command()
async def next(ctx):
    if ctx.voice_client.is_playing():
        if len(Music_list[ctx.guild.id])>0:
            url = Music_list[ctx.guild.id].pop()
            ctx.voice_client.source = discord.FFmpegPCMAudio(url)


@client.command()
async def watch(ctx):
    data = {
        'max_age':6000,
        'max_uses':0,
        'target_application_id':755600276941176913,
        'target_type':2,
        'temporary':False,
        'validate':None
    }
    headers = {
        'Authorization':"Bot OTAzMTMwMDM5MTMzMDE2MDk1.YXofZA.9jf6lfVKrmFCv_DfFuyOxpDwV_s",
        'Content-type':"application/json"
    }
    if ctx.author.voice is not None:
        if ctx.author.voice.channel is not None:
            channel = ctx.author.voice.channel

    response = requests.post(f"https://discord.com/api/v8/channels/{channel.id}/invites", data=json.dumps(data),headers=headers)
    link = json.loads(response.content)
    print(link)
    await ctx.send(f"https://discord.com/invite/{link['code']}")


@client.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()
    else:
        await ctx.send("Bot not in voice channel")


client.run(mtoken.token)
