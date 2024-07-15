from discord.ext import commands
import discord
import sys
import os
import json
import asyncio

# Adjust the import path to access main.py's create_embed function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import create_embed

class Pack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.packs = {}  # This will hold user packs for simplicity; consider using a database
        self.pack_data = self.load_pack_data()

    def load_pack_data(self):
        pack_file_path = os.path.join(os.path.dirname(__file__), '..', 'packs', 'pack_2023_24_series_two.json')
        with open(pack_file_path) as f:
            return json.load(f)

    @commands.command(name='earnpack')
    async def earn_pack(self, ctx):
        user = ctx.author
        if user.id not in self.packs:
            self.packs[user.id] = []
        # Add a copy of the pack data to the user's collection
        self.packs[user.id].append(self.pack_data.copy())
        embed = create_embed(title="Pack Earned!", description=f'{user.mention} earned a new pack!')
        await ctx.send(embed=embed)

    @commands.command(name='openpack')
    async def open_pack(self, ctx):
        user = ctx.author
        if user.id in self.packs and self.packs[user.id]:
            pack = self.packs[user.id].pop(0)  # Remove the first pack from the user's collection
            cards = sorted(pack["cards"], key=lambda x: x.get("rarity", "common"))  # Sort cards by rarity
            pack_image_path = pack.get("image", "default_pack_image_url")  # Use a default image if not found
            animation_path = pack.get("animation", None)  # Get the GIF animation path

            class PackView(discord.ui.View):
                def __init__(self, cards, pack_image_path, animation_path):
                    super().__init__()
                    self.cards = cards
                    self.pack_image_path = pack_image_path
                    self.animation_path = animation_path
                    self.current_card_index = 0
                    self.show_front = True
                    self.message = None

                async def start(self, ctx):
                    embed = discord.Embed(title="Opening Pack", description="Click the button below to open the pack.")
                    embed.set_image(url=f"attachment://{os.path.basename(self.pack_image_path)}")
                    self.message = await ctx.send(embed=embed, view=self, file=discord.File(self.pack_image_path))

                @discord.ui.button(label="Open", style=discord.ButtonStyle.primary)
                async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await interaction.response.defer()
                    await self.open_pack(interaction)
                    self.clear_items()  # Remove all buttons
                    self.add_item(PackView.Flip())  # Add the Flip button
                    self.add_item(PackView.Next())  # Add the Next button
                    await self.message.edit(view=self)

                async def open_pack(self, interaction: discord.Interaction):
                    if self.animation_path:
                        await self.tearing_animation(interaction)
                    await self.show_next_card(interaction)

                async def tearing_animation(self, interaction: discord.Interaction):
                    # Display the tearing animation GIF
                    embed = discord.Embed(title="Opening Pack", description="Tearing pack...")
                    embed.set_image(url=f"attachment://{os.path.basename(self.animation_path)}")
                    await self.message.edit(embed=embed, attachments=[discord.File(self.animation_path)])
                    await asyncio.sleep(2)  # Adjust the delay to match the length of your GIF animation

                async def show_next_card(self, interaction: discord.Interaction):
                    if self.current_card_index < len(self.cards):
                        card = self.cards[self.current_card_index]
                        description = f'{card["player_name"]} - {card["card_set"]} (#{card["card_number"]})'
                        embed = create_embed(title="Pack Opened", description=description)
                        # Attach the card front image
                        card_front_file = discord.File(card["front_image"], filename=f"front_{self.current_card_index}.png")
                        embed.set_image(url=f"attachment://front_{self.current_card_index}.png")
                        embed.set_footer(text="Card Front")
                        self.show_front = True
                        self.current_card_index += 1
                        await self.message.edit(embed=embed, view=self, attachments=[card_front_file])
                        await asyncio.sleep(1)  # Add a delay to make the transition smoother
                    else:
                        embed = create_embed(title="Pack Opened", description="No more cards left in the pack.")
                        await self.message.edit(embed=embed, view=None)

                class Flip(discord.ui.Button):
                    def __init__(self):
                        super().__init__(label="Flip", style=discord.ButtonStyle.primary)

                    async def callback(self, interaction: discord.Interaction):
                        view = self.view
                        if isinstance(view, PackView):
                            if view.current_card_index <= len(view.cards):
                                card = view.cards[view.current_card_index - 1]
                                description = f'{card["player_name"]} - {card["card_set"]} (#{card["card_number"]})'
                                if view.show_front:
                                    embed = create_embed(title="Pack Opened", description=description)
                                    # Attach the card back image
                                    card_back_file = discord.File(card["back_image"], filename=f"back_{view.current_card_index}.png")
                                    embed.set_image(url=f"attachment://back_{view.current_card_index}.png")
                                    embed.set_footer(text="Card Back")
                                    await view.message.edit(embed=embed, attachments=[card_back_file])
                                else:
                                    embed = create_embed(title="Pack Opened", description=description)
                                    card_front_file = discord.File(card["front_image"], filename=f"front_{view.current_card_index}.png")
                                    embed.set_image(url=f"attachment://front_{view.current_card_index}.png")
                                    embed.set_footer(text="Card Front")
                                    await view.message.edit(embed=embed, attachments=[card_front_file])
                                view.show_front = not view.show_front
                        await interaction.response.defer()

                class Next(discord.ui.Button):
                    def __init__(self):
                        super().__init__(label="Next", style=discord.ButtonStyle.secondary)

                    async def callback(self, interaction: discord.Interaction):
                        view = self.view
                        if isinstance(view, PackView):
                            await view.show_next_card(interaction)
                        await interaction.response.defer()

            view = PackView(cards, pack_image_path, animation_path)
            await view.start(ctx)

        else:
            embed = create_embed(title="Error", description="You don't have any packs to open.", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Pack(bot))
