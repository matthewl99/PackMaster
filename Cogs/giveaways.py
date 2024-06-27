import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import pytz  # For timezone handling, if needed
import random

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = {}  # Dictionary to track active giveaways
        self.scheduled_announcements = []  # List to track scheduled announcements

    @commands.command(name='startgiveaway', help='Starts a giveaway')
    async def start_giveaway(self, ctx, duration: int, *, prize: str):
        """Starts a giveaway."""
        await ctx.send(f"Giveaway for {prize} started and will last {duration} seconds! React with 🎉 to enter!")
        giveaway_message = await ctx.send(embed=create_embed("Giveaway!", f"Prize: {prize}"))
        await giveaway_message.add_reaction("🎉")
        self.giveaways[giveaway_message.id] = (ctx.channel.id, prize)

        await asyncio.sleep(duration)

        # Conclude the giveaway
        new_msg = await ctx.fetch_message(giveaway_message.id)
        users = await new_msg.reactions[0].users().flatten()
        users.remove(self.bot.user)  # Remove the bot from the participants

        if users:
            winner = random.choice(users)
            await ctx.send(f"Congratulations {winner.mention}! You won {prize}!")
        else:
            await ctx.send("No participants, giveaway cancelled.")
        del self.giveaways[giveaway_message.id]

    @commands.command(name='scheduleannouncement', help='Schedules an announcement')
    async def schedule_announcement(self, ctx, time: str, *, message: str, recurring: str = None):
        """Schedules an announcement. Optional: Recurring (daily, weekly)."""
        scheduled_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        delay = (scheduled_time - now).total_seconds()

        if delay < 0:
            await ctx.send("Cannot schedule an announcement in the past.")
            return

        announcement_id = len(self.scheduled_announcements)  # Simple ID based on list length
        self.scheduled_announcements.append((announcement_id, scheduled_time, message, ctx.channel.id, recurring))

        task = self.bot.loop.create_task(self.send_scheduled_announcement(delay, announcement_id))
        self.announcement_tasks[announcement_id] = task

        await ctx.send(f"Announcement {announcement_id} scheduled for {time}")

    async def send_scheduled_announcement(self, delay, announcement_id):
        """Sends the scheduled announcement after the delay."""
        await asyncio.sleep(delay)
        announcement = next((a for a in self.scheduled_announcements if a[0] == announcement_id), None)
        if announcement:
            _, _, message, channel_id, recurring = announcement
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
            if recurring:
                # Reschedule based on recurrence, e.g., add 1 day for daily
                # This is a simplified example; adjust timing and recurrence handling as needed
                new_time = datetime.now() + timedelta(days=1 if recurring == 'daily' else 7)  # daily or weekly
                new_delay = (new_time - datetime.now()).total_seconds()
                self.bot.loop.create_task(self.send_scheduled_announcement(new_delay, announcement_id))

    @commands.command(name='listannouncements', help='Lists all scheduled announcements')
    async def list_announcements(self, ctx):
        if not self.scheduled_announcements:
            await ctx.send("No scheduled announcements.")
            return
        for id, time, message, _, recurring in self.scheduled_announcements:
            await ctx.send(f"ID: {id} | Time: {time} | Recurring: {recurring or 'No'} | Message: {message}")

    @commands.command(name='cancelannouncement', help='Cancels a scheduled announcement by ID')
    async def cancel_announcement(self, ctx, announcement_id: int):
        announcement = next((a for a in self.scheduled_announcements if a[0] == announcement_id), None)
        if announcement:
            self.scheduled_announcements.remove(announcement)
            task = self.announcement_tasks.pop(announcement_id, None)
            if task and not task.done():
                task.cancel()
            await ctx.send(f"Announcement {announcement_id} canceled.")
        else:
            await ctx.send("Announcement not found.")

def setup(bot):
    bot.add_cog(Giveaways(bot))