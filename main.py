import discord
from discord.ext import commands
import json
import os

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True  # Enable the member intents for tracking join/leave events
# The bot instance
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Color scheme for embeds
COLOR_SCHEME = 0x1abc9c

# Function to create an embed template
def create_embed(title, description, color=COLOR_SCHEME):
    embed = discord.Embed(title=title, description=description, color=color)
    # Customize the embed further if needed
    return embed

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

bot.run(token)