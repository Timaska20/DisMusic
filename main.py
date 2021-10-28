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
    if ctx.author.id not in Music_list:
        Music_list[ctx.author.id] = []
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(current_Voice)
    await current_Voice.connect()

@client.command()
async def p(ctx, url : str, is_loop=False):
    global ydl_opts, Music_list
    await connect(ctx)
    if not is_loop:
        ytdl = youtube_dl.YoutubeDL(ydl_opts)
        data = ytdl.extract_info(url, download=False)
        print(data['url'])
        Music_list[ctx.author.id].append(data['url'])
        await ctx.send("Music add")
    else:
        Music_list[ctx.author.id].append(Music_list[ctx.author.id])
        await ctx.send("Music looped")
    while True:
        if ctx.voice_client.is_playing():
            await asyncio.sleep(2)
            continue
        else:
            try:
                url = Music_list[ctx.author.id].pop()
                ctx.voice_client.play(discord.FFmpegPCMAudio(url),after=lambda e: print(f'Player error: {e}') if e else None)
            except IndexError:
                break

@client.command()
async def loop(ctx):
    await p(ctx, "LOOP",True)
@client.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()
    else:
        await ctx.send("Bot not in voice channel")


client.run("ODkxMzU0NTk0NTM2NDgwNzc4.YU9Ipw.E9zxebd2oBDCv-zOa7oLXP06ZeE")
