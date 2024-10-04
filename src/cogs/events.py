# cogs/events.py
import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        contenido = message.content.lower()

        # Respuestas generales
        if 'hola' in contenido:
            await message.channel.send(f'hola {message.author.name}')
        elif contenido == 'buenas':
            await message.channel.send(f'hola {message.author.name}')
        elif contenido == 'que':
            await message.channel.send('so')
        elif contenido == 'rra':
            await message.channel.send('llado')
        
        # Respuestas específicas por ID de usuario
        respuestas_especificas = {
            967581989152653372: 'hola ANGELUS',
            671828689075437589: 'hola nigger', 
            580904606771445783: 'hola narizón',
            706673602950332439: 'hola tipito :3'
        }

        user_id = message.author.id
        if user_id in respuestas_especificas and 'hola' in contenido:
            await message.channel.send(respuestas_especificas[user_id])

        # Procesar otros comandos
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))
