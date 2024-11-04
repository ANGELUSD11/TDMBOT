#utils/wiki.py
import discord
from discord.ext import commands
import wikipedia

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='>', intents=intents)

class WikipediaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        wikipedia.set_lang('es')

    @bot.command()
    async def wiki(self, ctx, *, consulta):
        """Busca un artículo en Wikipedia y muestra un resumen."""
        try:
            resultado = self.buscar_wikipedia(consulta)
            await ctx.send(resultado)
        except Exception as e:
            await ctx.send(f'Error al realizar la búsqueda en Wikipedia: {e}')

    def buscar_wikipedia(self, consulta):
        try:
            resultado = wikipedia.summary(consulta, sentences=3)
            pagina = wikipedia.page(consulta)
            titulo = pagina.title
            url = pagina.url
            return f'**{titulo}**\n{resultado}\n{url}'
        except wikipedia.exceptions.DisambiguationError:
            return f'La búsqueda "{consulta}" es ambigua, por favor sé más específico.'
        except wikipedia.exceptions.PageError:
            return f'No se encontró ningún artículo relacionado con tu búsqueda "{consulta}".'

def setup(bot):
    bot.add_cog(WikipediaCog(bot))
