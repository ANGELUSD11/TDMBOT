import os
import discord
from discord import FFmpegPCMAudio
from ..core.ttsengine import generate_speech
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ffmpeg_path = os.getenv("FFMPEG_PATH")
        bot.remove_command('help')

    @commands.command()
    @commands.cooldown(rate=1, per=12000, type=commands.BucketType.guild)
    async def help(self, ctx):
        embed = discord.Embed(
            title='**HOLA!**',
            description=(
                "Soy un bot en desarrollo (versión beta sujeta a cambios) creado por ANGELUS11, "
                "mi prefijo es `>` y lo puedes utilizar para diferentes comandos\n\n"
                ">img: Busca una imagen en Google\n\n"
                ">wiki: Buscar un artículo en Wikipedia\n\n"
                ">meme/shitpost: Mandar un meme random de Reddit\n\n"
                ">cat: Muestra una imagen random de gatitos :3\n\n"
                ">avatar: Mostrar el avatar de un usuario\n\n"
                ">spotify (username): Ver qué está escuchando tú o un miembro en Spotify\n\n"
                ">binary: Convierte un valor entero a binario\n\n"
                ">ocr(local): Extrae texto de imágenes en varios idiomas con Tesseract\n\n"
                ">dl(local): Descarga videos de varios sitios con YT-DLP\n\n"
                ">translate (idioma, texto): Traduce texto en distintos idiomas\n\n"
                ">ia: Pregúntale una consulta a la IA de Gémini, puedes adjuntar imágenes."
                ">madewith: Información técnica sobre el bot\n\n"
                "Redes de ANGELUS: [GitHub](https://angelusd11.github.io/)"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url='https://panels.twitch.tv/panel-792145813-image-ec083130-b0fd-42ab-a88d-250e6ebe5c80')
        embed.set_footer(text='Este comando tiene cooldown de 3 horas')
        await ctx.send(embed = embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after)
            await ctx.send(f'Debes esperar {remaining_time} segundos antes de usar el comando nuevamente.')

    @commands.command()
    @commands.cooldown(rate=1, per=12000, type=commands.BucketType.guild)
    async def madewith(self, ctx):
        embed = discord.Embed(title='**Created with Python3.12 by ANGELUS11**\n\ndiscord.py', description='You can find the source code in:\n https://github.com/ANGELUSD11/TDMBOT \nHosting:\n https://bot-hosting.net/ \nSupport:\n https://discord.gg/eTnPfUev3m', 
        color=discord.Color.dark_blue())
        embed.set_image(url='https://images.opencollective.com/discordpy/25fb26d/logo/256.png')
        embed.set_footer(text='Este comando tiene cooldown de 3 horas')
        await ctx.send(embed=embed)

    @madewith.error
    async def madewith_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after)
            await ctx.send(f'Debes esperar {remaining_time} segundos antes de usar el comando nuevamente.')

    @commands.command()
    async def chat(self, ctx, *, mensaje: str = None):
        if not mensaje:
            await ctx.send('Dí algo para que el bot lo replique.')
            return
        else:
            await ctx.send(mensaje)

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            audio_path = generate_speech(mensaje)
            voice_client.audio_path = audio_path 
            try:
                if not voice_client.is_playing():
                    voice_client.play(
                        FFmpegPCMAudio(audio_path, executable=self.ffmpeg_path),
                        after=lambda e: os.remove(audio_path) if os.path.exists(audio_path) else None
                    )
            finally:
                if os.path.exists(audio_path) and not voice_client.is_playing():
                    os.remove(audio_path)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'Avatar de {member.display_name}', color=discord.Color.blue())
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def binary(self, ctx, *, number: str):
        try:
            entero = int(number)
            binario = bin(entero)[2:]
            embed = discord.Embed(title='Conversión a binario', color=discord.Color.green())
            embed.add_field(name='Número entero', value=entero, inline=False)
            embed.add_field(name='Número binario', value=binario, inline=False)

            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(title=f'❌Error, {number}, no es un valor válido, por favor ingresa un número.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def spotify(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        print(member.activities)

        activity = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)

        if activity:
            embed = discord.Embed(title=f'{member.display_name} está escuchando {activity.title}', description=f'Artista: {activity.artist}\nÁlbum: {activity.album}', color=activity.colour)
            embed.set_thumbnail(url=activity.album_cover_url)
            embed.add_field(name='Duración: ', value=str(activity.duration), inline=True)
            embed.add_field(name='Escuchar en Spotify', value=f'[Link]({activity.track_url})', inline=True)

            await ctx.send(embed=embed)

        else:
            await ctx.send(f'{member.display_name} no está escuchando Spotify en este momento.')

async def setup(bot):
    await bot.add_cog(InfoCog(bot)) 
