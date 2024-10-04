import discord
from discord.ext import commands
import googleapiclient.discovery

from utils.config import (SEARCH_API_KEY, CSE_ID)

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=SEARCH_API_KEY)

    def buscar_imagen(self, query):
        try:
            res = self.search_service.cse().list(
                q=query,
                cx=CSE_ID,
                searchType='image',
                num=1,
                safe='active'
            ).execute()

            if 'items' in res:
                return res['items'][0]  # Retornar el primer resultado de imagen
            return None
        except Exception as e:
            print(f'Error al buscar imagen: {e}')
            return None

    @commands.command()
    async def search(self, ctx, *, query):
        """Buscar imágenes en Google."""
        image_result = self.buscar_imagen(query)

        if image_result:
            title = image_result['title']
            link = image_result['link']
            url_page = image_result['image']['contextLink']

            embed = discord.Embed(
                title=title,
                url=url_page,
                description=f'Resultados para **{query}**'
            )
            embed.set_image(url=link)
            embed.set_footer(text=f'Página: {url_page}')

            await ctx.send(embed=embed)
        else:
            await ctx.send('No se encontraron resultados de imágenes')

# Función para añadir el cog al bot
async def setup(bot):
    await bot.add_cog(SearchCog(bot))
