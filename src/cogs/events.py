import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
import datetime
import logging

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.general_channel_id = int(os.getenv("GENERAL_CHANNEL"))

        self.BIRTH_DAY = 15
        self.BIRTH_MONTH = 7
        self.BIRTH_HOUR = 15
        self.BIRTH_MINUTE = 30

        self.birthday_reminder.start()

    @tasks.loop(minutes=1)
    async def birthday_reminder(self):
        now = datetime.datetime.now()
        if (now.day == self.BIRTH_DAY and
            now.month == self.BIRTH_MONTH and
            now.hour == self.BIRTH_HOUR and
            now.minute == self.BIRTH_MINUTE):
            channel = self.bot.get_channel(int(self.general_channel_id))
            if channel:
                age = now.year - 2005
                await channel.send(f"¡Hoy es el cumpleaños de Angelus, felicítenlo por sus {age} años! 🎉")
                self.birthday_reminder.stop()

    @birthday_reminder.before_loop
    async def before_birthday_reminder(self):
        await self.bot.wait_until_ready()
        logging.info("Birthday reminder is ready.")

async def setup(bot):
    await bot.add_cog(EventsCog(bot)) 