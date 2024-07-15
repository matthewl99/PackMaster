from discord.ext import commands
import discord
import sys
import os

# Adjust the import path to access main.py's create_embed function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import create_embed

class Collection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collections = {}  # This will hold user collections for simplicity; consider using a database

    @commands.command(name='viewcollection')
    async def view_collection(self, ctx):
        user = ctx.author
        if user.id in self.collections:
            collection = self.collections[user.id]
            description = '\n'.join(collection) if collection else 'Your collection is empty.'
        else:
            description = 'Your collection is empty.'
        embed = create_embed(title=f"{user.name}'s Collection", description=description)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))
