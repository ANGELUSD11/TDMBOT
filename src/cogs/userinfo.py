import os
import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True
SERVER_ID = int(os.getenv("SERVER_ID", 0))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == SERVER_ID:
            channel = member.guild.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f'{member.mention}, bienvenido al servidor!/ welcome to the server! :D')
            else:
                print('No se encontró el canal indicado.')
        else:
            print('No se encontró el servidor indicado.')

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))