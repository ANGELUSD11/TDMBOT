import os
import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
from discord import FFmpegPCMAudio

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx): #command to join a voice channel
        if ctx.author.voice: #verify if the user is in a VC
            channel = ctx.author.voice.channel #obtain the voice channel
            await channel.connect()
            await ctx.send("Connected to the voice channel.")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I am not connected to any voice channel.")

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))