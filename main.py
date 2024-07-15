import discord
from discord.ext import commands
import json
import os
import asyncio

# Determine the path to the configuration file relative to the main.py script
base_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(base_directory, 'configuration.json')

# Print the current working directory
print(f"Current Working Directory: {os.getcwd()}")
print(f"Configuration file path: {config_file_path}")

# Load configuration
with open(config_file_path) as config_file:
    config = json.load(config_file)

token = config["token"]
prefix = config["prefix"]
owner_id = config["owner_id"]

# Initialize bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, owner_id=owner_id, intents=intents)

# Color scheme for embeds
COLOR_SCHEME = 0x1abc9c

# Function to create an embed template
def create_embed(title, description, color=COLOR_SCHEME):
    embed = discord.Embed(title=title, description=description, color=color)
    # Customize the embed further if needed
    return embed

@bot.event
async def on_ready():
    if bot.user:
        print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('Ready to serve!')

# Load cogs
initial_extensions = ['cogs.pack', 'cogs.collection', 'cogs.trading', 'cogs.showcase', 'cogs.events']

async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)

if __name__ == '__main__':
    asyncio.run(load_extensions())
    bot.run(token)
