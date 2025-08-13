import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import requests
import googleapiclient.discovery

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

class QueryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.search_api_key = os.getenv("SEARCH_API_KEY")
        self.cse_id = os.getenv("CSE_ID")

    @commands.command()
    async def yt(self, ctx, *, search_query=None):
        if not search_query:
            await ctx.send('Please enter a search term')
            return
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={self.youtube_api_key}&type=video&maxResults=1&safeSearch=strict"
        search_response = requests.get(search_url).json()

        if search_response['items']:
            video = search_response['items'][0]
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            channel_name = video['snippet']['channelTitle']
            published_at = video['snippet']['publishedAt']

            video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={video_id}&key={self.youtube_api_key}'
            video_details_response = requests.get(video_details_url).json()
            video_details = video_details_response['items'][0]

            duration = video_details['contentDetails']['duration']
            views = video_details['statistics']['viewCount']

            embed = discord.Embed(title=video_title, url=f'https://www.youtube.com/watch?v={video_id}', color=discord.Color.red())
            embed.add_field(name='Uploaded by', value=channel_name, inline=False)
            embed.add_field(name='Duration', value=duration, inline=False)
            embed.add_field(name='ID', value=video_id, inline=False)
            embed.add_field(name='Published', value=published_at, inline=False)
            embed.add_field(name='Views', value=f'{views} views', inline=False)
            embed.set_image(url=video['snippet']['thumbnails']['high']['url'])

            await ctx.send(embed=embed)

        else:
            await ctx.send('No se encontraron videos')

    @commands.command()
    async def img(self, ctx, *, query=None):
        if not query:
            await ctx.send('Please enter a search term')
            return
        try:
            service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=self.search_api_key)

            res = service.cse().list(
                q=query, cx=self.cse_id, searchType='image', num=1, safe='active'
            ) .execute()

            if 'items' in res:
                item = res['items'][0]
                title = item['title']
                link = item['link']
                url_page = item['image']['contextLink']

                embed = discord.Embed(title=title, url=url_page, description= f'Resultados para **{query}**', color=discord.Color.yellow())
                embed.set_image(url=link)
                embed.set_footer(text=f'{url_page}')

                await ctx.send(embed=embed)
            else:
                await ctx.send('No se encontaron resultados')
    
        except Exception as e:
            await ctx.send(f'Ha ocurrido un error al buscar la imagen {e}')

    @commands.command()
    async def google(self, ctx, *, query=None):
        if not query:
            await ctx.send('Please enter a search term')
            return
        try:
            service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=self.search_api_key)
            res = service.cse().list(
                q=query, cx=self.cse_id, num=3, safe='active'
            ) .execute()

            if 'items' in res:
                for item in res['items'][:3]:
                    title = item['title']
                    snippet = item['snippet']
                    link = item['link']

                    embed = discord.Embed(title=title, description=snippet, url=link, color=discord.Color.yellow())
                    await ctx.send(embed=embed)
            else:
                await ctx.send('No se encontraron resultados')
        except Exception as e:
            await ctx.send(f'Ocurrió un error al realizar la búsqueda: {e}')

async def setup(bot):
    await bot.add_cog(QueryCog(bot)) 
