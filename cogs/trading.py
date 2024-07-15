from discord.ext import commands
import discord
import sys
import os

# Adjust the import path to access main.py's create_embed function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import create_embed

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trade_proposals = {}  # This will hold trade proposals; consider using a database

    @commands.command(name='proposetrade')
    async def propose_trade(self, ctx, user: discord.User, my_card: str, their_card: str):
        proposer = ctx.author
        self.trade_proposals[(proposer.id, user.id)] = (my_card, their_card)
        embed = create_embed(title="Trade Proposal", description=f'{proposer.mention} proposed a trade to {user.mention}: {my_card} for {their_card}')
        await ctx.send(embed=embed)

    @commands.command(name='accepttrade')
    async def accept_trade(self, ctx, user: discord.User):
        accepter = ctx.author
        if (user.id, accepter.id) in self.trade_proposals:
            my_card, their_card = self.trade_proposals.pop((user.id, accepter.id))
            # Logic to swap the cards
            embed = create_embed(title="Trade Accepted", description=f'{accepter.mention} accepted the trade from {user.mention}: {my_card} for {their_card}')
            await ctx.send(embed=embed)
        else:
            embed = create_embed(title="Error", description="No trade proposal found from this user.", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(Trading(bot))
