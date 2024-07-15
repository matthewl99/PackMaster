from discord.ext import commands
import discord
import sys
import os

# Adjust the import path to access main.py's create_embed function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import create_embed

class Showcase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.showcases = {}  # This will hold user showcases; consider using a database

    @commands.command(name='showcase')
    async def showcase(self, ctx):
        user = ctx.author
        if user.id in self.showcases:
            showcase = self.showcases[user.id]
            description = '\n'.join(showcase) if showcase else 'Your showcase is empty.'
        else:
            description = 'Your showcase is empty.'
        embed = create_embed(title=f"{user.name}'s Showcase", description=description)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Showcase(bot))
