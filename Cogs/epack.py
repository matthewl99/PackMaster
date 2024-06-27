import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import create_embed

class EpackUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.check_epack_updates, 'interval', hours=1)
        self.scheduler.start()

@commands.command()
async def starttrade(self, ctx, member: discord.Member, *, card_name):
    """Initiates a trade discussion with another user."""
    designated_channel = discord.utils.get(ctx.guild.channels, name="trade-discussions")
    if designated_channel:
        await designated_channel.send(f"{ctx.author.mention} wants to trade **{card_name}** with {member.mention}.")
    else:
        await ctx.send("The designated channel for trade discussions does not exist.")

@commands.command()
async def sharepull(self, ctx, *, card_name):
    """Allows users to share their card pull in a designated channel."""
    designated_channel = discord.utils.get(ctx.guild.channels, name="🌐│・global-gatherings")
    if designated_channel:
        embed = create_embed("Card Pull", f"{ctx.author.display_name} pulled a **{card_name}**!", 0x3498db)
        await designated_channel.send(embed=embed)
    else:
        await ctx.send("The designated channel for card pulls does not exist.")
    async def check_epack_updates(self):
        url = "https://www.upperdeckepack.com/news"  # Replace with the actual URL of the ePack updates page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example parsing logic (this will need to be customized)
        # new_updates = soup.find_all("div", class_="update-class")
        new_updates = False  # Placeholder, replace with actual parsing logic

        if new_updates:
            channel = self.bot.get_channel(1254530289158590464)  # Replace with your channel ID
            await channel.send("New updates found on ePack: ...")  # Customize your message
            

def setup(bot):
    bot.add_cog(EpackUpdates(bot))