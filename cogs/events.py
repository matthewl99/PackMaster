from discord.ext import commands
import discord
import sys
import os

# Adjust the import path to access main.py's create_embed function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import create_embed

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joinevent')
    async def join_event(self, ctx, event_name: str):
        user = ctx.author
        # Logic to join the event
        embed = create_embed(title="Event Joined", description=f'{user.mention} joined the event: {event_name}')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
