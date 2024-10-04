# cogs/admin.py
import discord
from discord.ext import commands

from utils.config import DISCORD_CHANNEL

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 500, commands.BucketType.user)
    async def diamond(self, ctx):
        """Envía un mensaje informativo sobre el bot."""
        await ctx.send('Hola, soy un bot creado por ANGELUS con el propósito de cumplir las funciones básicas de información para los miembros del servidor. Pronto recibiré más actualizaciones con funciones útiles.')

    @diamond.error
    async def diamond_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tiempo_restante = round(error.retry_after)
            await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        contenido = message.content.lower()
        respuestas = {
            'hola': f'hola {message.author.name}',
            'buenas': f'hola {message.author.name}',
            'que': 'so',
            'rra': 'llado'
        }

        # Respuestas generales
        for clave, respuesta in respuestas.items():
            if clave in contenido:
                await message.channel.send(respuesta)
                break  # Evita múltiples respuestas

        # Respuestas específicas por ID de usuario
        respuestas_especificas = {
            967581989152653372: 'hola ANGELUS',
            671828689075437589: 'hola nigger',  # **⚠️ Importante: Este término es ofensivo y no debe usarse. Recomendación: eliminar o reemplazar.**
            580904606771445783: 'hola narizón',
            706673602950332439: 'hola tipito :3'
        }

        user_id = message.author.id
        if user_id in respuestas_especificas and 'hola' in contenido:
            await message.channel.send(respuestas_especificas[user_id])

def setup(bot):
    bot.add_cog(Admin(bot))
