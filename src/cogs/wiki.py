import discord
from discord.ext import commands
import wikipedia

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def search_wikipedia(self, query):
        try:
            wikipedia.set_lang('es')
            result = wikipedia.summary(query, sentences = 4)
            page = wikipedia.page(query)
            url = page.url
            content = f'{result}\n{url}'

            if len(content)> 2000:
                content = content[::1997] + '...\n' + url

            return content

        except wikipedia.exceptions.DisambiguationError as e:
            return f'la busqueda {query} es ambigua, por favor se más específico.'
        except wikipedia.exceptions.PageError as e:
            return f'No se encontró ningún articulo relacionado con su búsqueda {query}.'
        except Exception as e:
            print(e)

    @commands.command()
    async def wiki (self, ctx, *, query):
        try:
            resultado = self.search_wikipedia(query)
            await ctx.send(resultado)
        except Exception as e :
            await ctx.send(f'Error al realizar la busqueda en Wikipedia: {e}')

async def setup(bot):
    await bot.add_cog(WikiCog(bot))     
