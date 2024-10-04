# cogs/youtube.py
import discord
from discord.ext import commands, tasks
import requests

from utils.config import (YOUTUBE_API_KEY, CHANNEL_ID, DISCORD_CHANNEL)
from utils.youtube_api import build_youtube_service  # Crearemos esta función en el siguiente paso

class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_video_id = None
        self.youtube = build_youtube_service(YOUTUBE_API_KEY)
        self.check_new_video.start()

    def cog_unload(self):
        self.check_new_video.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print('YouTube Cog está listo.')

    @tasks.loop(minutes=5)
    async def check_new_video(self):
        url = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1'
        response = requests.get(url)
        data = response.json()
        print(data)

        if data.get('items'):
            latest_video = data['items'][0]
            video_id = latest_video['id']['videoId']

            if video_id != self.last_video_id:
                self.last_video_id = video_id
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                channel = self.bot.get_channel(DISCORD_CHANNEL)
                if channel:
                    await channel.send(f'@everyone ANGELUS11💠 ha subido un nuevo video :D ve a verlo!\n{video_url}')
                else:
                    print(f'No se pudo encontrar el canal con el id {DISCORD_CHANNEL}')

    @check_new_video.before_loop
    async def before_check_new_video(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def yt(self, ctx, *, search_query):
        """Busca un video en YouTube y muestra detalles."""
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={YOUTUBE_API_KEY}&type=video&maxResults=1"
        search_response = requests.get(search_url).json()

        if search_response.get('items'):
            video = search_response['items'][0]
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            channel_name = video['snippet']['channelTitle']
            published_at = video['snippet']['publishedAt']

            video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={video_id}&key={YOUTUBE_API_KEY}'
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
            await ctx.send('No se encontraron videos.')

def setup(bot):
    bot.add_cog(YouTube(bot))
