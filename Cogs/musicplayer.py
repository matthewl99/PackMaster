import discord
from discord.ext import commands
import youtube_dl
from async_timeout import timeout
from collections import deque

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.music_queues = {}  # Add a queue for each guild

    async def play_next_song(self, ctx):
        """Plays the next song in the queue, if any."""
        if ctx.guild.id in self.music_queues and self.music_queues[ctx.guild.id]:
            source = self.music_queues[ctx.guild.id].popleft()
            self.voice_clients[ctx.guild.id].play(source, after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
        else:
            # Disconnect after the queue is empty, optional
            await self.leave(ctx)

    @commands.command()
    async def play(self, ctx, url):
        """Adds a song to the queue and plays it if no song is currently playing."""
        if ctx.guild.id not in self.voice_clients or not self.voice_clients[ctx.guild.id].is_connected():
            await ctx.invoke(self.join)
        
        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(URL, method='fallback')
            
        if ctx.guild.id not in self.music_queues:
            self.music_queues[ctx.guild.id] = deque()
        
        self.music_queues[ctx.guild.id].append(source)
        
        if not self.voice_clients[ctx.guild.id].is_playing():
            await self.play_next_song(ctx)

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song."""
        if ctx.guild.id in self.voice_clients and self.voice_clients[ctx.guild.id].is_playing():
            self.voice_clients[ctx.guild.id].stop()
            await self.play_next_song(ctx)

    # Include other commands (pause, resume, stop, leave) here as before

def setup(bot):
    bot.add_cog(MusicPlayer(bot))