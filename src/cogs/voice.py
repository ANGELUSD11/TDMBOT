import os
from discord.ext import commands

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client:
                await ctx.send("I am already connected to a voice channel.")
            else:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send("Connected to the voice channel.")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        if not voice_client:
            await ctx.send("I am not connected to any voice channel.")
            return

        if ctx.author.voice.channel != voice_client.channel:
            await ctx.send("You are not in the same voice channel as me.")
            return

        if voice_client.is_playing():
            voice_client.stop()

        # Borrar archivo de audio si está guardado
        audio_path = getattr(voice_client, "audio_path", None)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

        await voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        if not voice_client:
            await ctx.send("I am not connected to any voice channel.")
            return

        if ctx.author.voice.channel != voice_client.channel:
            await ctx.send("You are not in the same voice channel as me.")
            return

        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Stopped audio.")
        else:
            await ctx.send("No audio is currently playing.")

        audio_path = getattr(voice_client, "audio_path", None)   
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))
