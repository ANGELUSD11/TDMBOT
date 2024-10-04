import os
import random
import wikipedia
import praw
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from PIL import Image
import pytesseract
from io import BytesIO
import asyncio
import requests
from discord_easy_commands import EasyBot
from discord.gateway import EventListener
from discord import app_commands, Interaction
import googleapiclient.discovery
import datetime

#configuración inicial del bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix = '<>', intents = intents)

DISCORD_TOKEN = 'my discord token'
DISCORD_CHANNEL = int('my discord channel integer')
YOUTUBE_API_KEY = 'my api key'
#custom search engine ID
CSE_ID = 'my cse id'
CHANNEL_ID = 'my channel id'

#variable global para almacenar el último video encontrado
last_video_id = None

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = 'AIzaSyDhieh_xHzxX8pjn_joqDJpYs7NHGqnitU')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    activity = discord.Activity(type=discord.ActivityType.watching, name='ANGELUS11💠|<>')
    await bot.change_presence(activity=activity)
    check_new_video.start()

@tasks.loop(minutes=5)
async def check_new_video():
    global last_video_id
    url = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1'
    response = requests.get(url)
    data = response.json()
    print(data)

    if data['items']:
        latest_video = data['items'][0]
        #la variable video_id contiene el video actual
        video_id = latest_video['id']['videoId']
        #last_video_id contiene el último video encontrado mientras que video_id contiene el video actual
        if video_id != last_video_id:
            last_video_id = video_id
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            channel = bot.get_channel(DISCORD_CHANNEL)
            if channel is None:
                print(f'No se pudo encontrar el canal con el id {DISCORD_CHANNEL}')
            else:
                await channel.send(f'@everyowone ANGELUS11💠 ha subido un nuevo video :D ve a verlo!\n{video_url}')

@check_new_video.before_loop
async def before_check_new_video():
    await bot.wait_until_ready()

@bot.command()
async def yt(ctx, *, search_query):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={YOUTUBE_API_KEY}&type=video&maxResults=1"
    search_response = requests.get(search_url).json()

    if search_response['items']:
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
        await ctx.send('No se encontraron videos')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Responder a "hola"
    if 'hola' in message.content.lower():
        await message.channel.send(f'hola {message.author.name}')

    if message.content.lower() == 'buenas':
        await message.channel.send(f'hola {message.author.name}')
    
    # Responder a "que"
    if message.content.lower() == 'que':
        await message.channel.send('so')

    if message.content.lower() == 'rra':
        await message.channel.send('llado')

    if message.author.id == 967581989152653372 and 'hola' in message.content.lower():
        await message.channel.send('hola ANGELUS')
    
    if message.author.id == 671828689075437589 and 'hola' in message.content.lower():
        await message.channel.send('hola nigger')

    if message.author.id == 580904606771445783 and 'hola' in message.content.lower():
        await message.channel.send('hola narizón')

    if message.author.id == 706673602950332439 and 'hola' in message.content.lower():
        await message.channel.send('hola tipito :3')
    
    # Procesar otros comandos
    await bot.process_commands(message)

@bot.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def diamond (ctx):
    await ctx.send('Hola, soy un bot creado por ANGELUS con el propósito de cumplir las funciones basicas de información para los miembros del server, pronto recibiré más actualizaciones con funciones útiles')

@diamond.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

def buscar_wikipedia(consulta):
    try:
        wikipedia.set_lang('es')
        resultado = wikipedia.summary(consulta, sentences = 4)
        pagina = wikipedia.page(consulta)
        url = pagina.url
        return f'{resultado}\n{url}'
    except wikipedia.exceptions.DisambiguationError as e:
        return f'la busqueda {consulta} es ambigua, por favor se más específico.'
    except wikipedia.exceptions.PageError as e:
        return f'No se encontró ningún articulo relacionado con su búsqueda {consulta}.'
@bot.command()
async def wiki (ctx, *, consulta):
    try:
        resultado =  buscar_wikipedia(consulta)
        await ctx.send(resultado)
    except Exception as e :
        await ctx.send(f'Error al realizar la busqueda en Wikipedia: {e}')

@bot.command()
async def search(ctx, *, query):
    try:
        service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=SEARCH_API_KEY)

        res = service.cse().list(
            q=query, cx=CSE_ID, searchType='image', num=1, safe='active'
        ) .execute()

        if 'items' in res:
            item = res['items'][0]
            title = item['title']
            link = item['link']
            url_page = item['image']['contextLink']

            embed = discord.Embed(title=title, url=url_page, description= f'Resultados para **{query}**')
            embed.set_image(url=link)
            embed.set_footer(text=f'Página={url_page}')

            await ctx.send(embed=embed)
        else:
            await ctx.send('No se encontaron resultados')
    
    except Exception as e:
        await ctx.send(f'Ha ocurrido un error al buscar la imagen {e}')

reddit = praw.Reddit(
    client_id = '_bKAslb7CgqepTll5_y8-Q',
    client_secret = '7cKKUzZC_NuNG7SqfyYpDIvEVD74XA',
    user_agent = 'discord_bot:v1.0.0 (by u/ANGELUSR11)'
)

@bot.command()
async def meme(ctx):
    subreddit = reddit.subreddit("MemesESP")
    memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

    image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    if image_memes:
        meme = random.choice(image_memes)
        meme_title = meme.title
        meme_url = meme.url
        meme_post_link = f"https://reddit.com{meme.permalink}"

        embed = discord.Embed(title=meme_title, url=meme_post_link)
        embed.set_image(url=meme_url)
        embed.set_footer(text=f"Fuente: r/MemesESP")
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron memes de imágenes.")

@bot.command()
async def dankmeme(ctx):
    subreddit = reddit.subreddit("dankmemes")
    memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

    image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    if image_memes:
        meme = random.choice(image_memes)
        meme_title = meme.title
        meme_url = meme.url
        meme_post_link = f"https://reddit.com{meme.permalink}"

        embed = discord.Embed(title=meme_title, url=meme_post_link)
        embed.set_image(url=meme_url)
        embed.set_footer(text=f"Fuente: r/dankmemes")
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron memes de imágenes.")

@bot.command()
async def shitpost(ctx):
    subreddit = reddit.subreddit("shitposting")
    memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

    image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    if image_memes:
        meme = random.choice(image_memes)
        meme_title = meme.title
        meme_url = meme.url
        meme_post_link = f"https://reddit.com{meme.permalink}"

        embed = discord.Embed(title=meme_title, url=meme_post_link)
        embed.set_image(url=meme_url)
        embed.set_footer(text=f"Fuente: r/shitposting")
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron memes de imágenes.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f'Avatar de {member.display_name}', color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def givemebadge(ctx):
    await ctx.send('Espera 24 horas para reclamar la insignia\nPuedes reclamarla en https://discord.com/developers/active-developer')

@bot.command()
@commands.cooldown(1, 12000, commands.BucketType.user)
async def info(ctx):
  embed = discord.Embed(description = '**Hola!**\n\n Soy un bot en desarrollo creado por ANGELUS11, mi prefijo es <> y lo puedes utilizar para diferentes comandos\n\n<>search: Busca una imagen en Google\n\n<>yt: Buscar un video en YouTube\n\n<>wiki: Buscar un artículo en Wikipedia\n\n<>meme/dankmeme/shitpost: Mandar un meme random de Reddit\n\n<>avatar: Mostrar el avatar de un usuario\n\n<>madewith: Información técnica sobre el bot', 
  color=discord.Color.green())
  embed.set_image(url='https://panels.twitch.tv/panel-792145813-image-ec083130-b0fd-42ab-a88d-250e6ebe5c80')
  embed.set_footer(text='Este comando tiene cooldown de 3 horas')
  await ctx.send(embed = embed)

@info.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 12000, commands.BucketType.user)
async def madewith(ctx):
  embed = discord.Embed(description = '**Bot desarrollado con Python3.12**\n\nUsando la librería discord.py, puedes encontrar todo mi código fuente en el repositorio:\n https://github.com/ANGELUSD11/TDMBOT \nHosteado con:\n https://bot-hosting.net/ \nCanal de soporte:\n https://discord.gg/eTnPfUev3m', 
  color=discord.Color.dark_blue())
  embed.set_image(url='https://images.opencollective.com/discordpy/25fb26d/logo/256.png')
  embed.set_footer(text='Este comando tiene cooldown de 3 horas')
  await ctx.send(embed = embed)

@madewith.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def redes (ctx):
    embed = discord.Embed(description= '**REDES DE ANGELUS**\n YouTube: https://www.youtube.com/channel/UCFYLLqA03vesXUt-3eTP81A\n Twitch: https://www.twitch.tv/angelusd11', color = discord.Color.blue())
    embed.set_image(url= 'https://panels.twitch.tv/panel-792145813-image-5131cc5e-a31b-48bb-91bb-0133e967aa59')
    embed.set_image(url= 'https://media.discordapp.net/attachments/1015682580252729475/1146960229012086784/Screenshot_20230831-1909592.png?width=1007&height=701')
    await ctx.send(embed=embed)

@redes.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 10000, commands.BucketType.user)
async def youtube (ctx):
    embed = discord.Embed(description = "**CANAL DE YOUTUBE**\n\nhttps://www.youtube.com/channel/UCFYLLqA03vesXUt-3eTP81A", color=discord.Color.red())
    embed.set_image(url='https://panels.twitch.tv/panel-792145813-image-5131cc5e-a31b-48bb-91bb-0133e967aa59')
    await ctx.send(embed=embed)

@yt.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def twitch (ctx):
    embed = discord.Embed(description="**CANAL DE TWITCH**\n\nhttps://www.twitch.tv/angelus11t", color=discord.Color.purple())
    embed.set_image(url='https://cdn.discordapp.com/attachments/1015682580252729475/1146960229012086784/Screenshot_20230831-1909592.png')
    await ctx.send(embed=embed)

@twitch.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
async def binario(ctx, number: str):
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

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ocr(ctx):
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url

        try:
            if ctx.message.attachments[0].size > 5 * 1024 * 1024:
                await ctx.send('La imagen es demasiado grande, sube una imagen de menos de 5mb')
                return

            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            text = pytesseract.image_to_string(img)

            if text.strip():
                embed = discord.Embed(title='Texto extraido', description=text[:1024], color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                await ctx.send('❌Error, no se encontró texto en la imagen')
        except Exception as e:
            await ctx.send(f'Ocurrió un error al procesar la imagen: {str(e)}')

    else:
        await ctx.send('Por favor, adjunta una imagen para procesar.')

@ocr.error
async def ocr_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'❌Por favor espera {error.retry_after:.2f} segundos antes de usar el comando nuevamente.')

@bot.command()
async def spotify(ctx, member: discord.Member = None):
    member = member or ctx.author
    print(member.activities)
    activity = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)

    if activity:
        embed = discord.Embed(title=f'{member.name} está escuchando {activity.title}', description=f'Artista: {activity.artist}\nÁlbun: {activity.album}', color=activity.colour)
        embed.set_thumbnail(url=activity.album_cover_url)
        embed.add_field(name='Duración: ', value=str(activity.duration), inline=True)
        embed.add_field(name='Escuchar en Spotify', value=f'[Link]({activity.track_url})', inline=True)

        await ctx.send(embed=embed)

    else:
        await ctx.send('El usuario mencionado no está escuchando música en Spotify en este momento.')

bot.run(DISCORD_TOKEN)
