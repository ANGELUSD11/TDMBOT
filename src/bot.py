import os
import random
import time
import sys
import discord
import discord.ext.commands
import wikipedia
import praw
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
import yt_dlp
import logging
from deep_translator import GoogleTranslator
import subprocess2
import datetime

import discord.ext

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True
bot = commands.Bot(command_prefix = '>', intents = intents)

DISCORD_TOKEN = ''
DISCORD_CHANNEL = 
GENERAL_CHANNEL = 
YOUTUBE_API_KEY = ''
SEARCH_API_KEY = ''
CSE_ID = ''
SERVER_ID = ''
CHANNEL_ID = ''

#user ids in strings

allowed_users = ['', '']

#variable global para almacenar el último video encontrado /global variable
last_video_id = None
#variable global para almacenar el último stream envontrado /global variable
last_live_id = None

pytesseract.pytesseract.tesseract_cmd = r'/home/container/Tesseract-OCR/tesseract.exe'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = '')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    channel_ids = [982093327799312404, 747832973214351382]
    start_message = 'Bot started!'
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        #if the bot find channel
        if channel:
            await channel.send(start_message)
        else:
            print(f'No se pudo encontrar el canal: {channel_id}')

    activity = discord.Activity(type=discord.ActivityType.watching, name='ANGELUS11💠|>')
    await bot.change_presence(activity=activity)
    check_new_video.start()
    check_live_stream.start()

@bot.event
async def on_member_join(member):
    if member.guild.id == SERVER_ID:
        channel = member.guild.get_channel(GENERAL_CHANNEL) #obtiene el canal en base a la variable GENERAL_CHANNEL
        #comprueba la existencia de un canal determinado
        if channel:
            await channel.send(f'{member.mention}, bienvenido al servidor!')
        else:
            print('No se encontró el canal indicado.')
    else:
        print('No se encontró el servidor indicado.')

bot.event
async def on_disconnect():
    channel_ids = [982093327799312404, 747832973214351382]
    maintenance_message = 'El bot está por desconectarse debido a mantenimiento, volverá más tarde :)'
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(maintenance_message)
        else:
            print(f'No se pudo encontrar el canal: {channel_id}')

#verify and notify latest video in the channel 
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


#verify and notify latest livestream in the channel 
@tasks.loop(minutes=5)
async def check_live_stream():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&type=video&eventType=live&key={YOUTUBE_API_KEY}"
    global last_live_id
    response = requests.get(url)
    data = response.json()
    print(data)

    if data['items']:
        latest_live = data['items'][0]
        live_id = latest_live['id']['videoId']

        # Verifica si hay una nueva transmisión en vivo
        if live_id != last_live_id:
            last_live_id = live_id
            live_url = f'https://www.youtube.com/watch?v={live_id}'
            channel = bot.get_channel(GENERAL_CHANNEL)
            if channel is None:
                print(f'No se pudo encontrar el canal con el id {GENERAL_CHANNEL}')
            else:
                await channel.send(f'@everyowone ¡ANGELUS11💠 ha comenzado una transmisión en vivo!\n{live_url}')

@check_live_stream.before_loop
async def before_check_live_stream():
    await bot.wait_until_ready()

@bot.command()
async def yt(ctx, *, search_query):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={YOUTUBE_API_KEY}&type=video&maxResults=1&safeSearch=strict"
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

    if message.content.lower() == 'hola':
        await message.channel.send(f'hola {message.author.name}')
    
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
    if str(ctx.author.id) in allowed_users:
        await ctx.send('Hola, soy un bot creado por ANGELUS con el propósito de cumplir las funciones basicas de información para los miembros del server, pronto recibiré más actualizaciones con funciones útiles')
    else:
        await ctx.send('No tienes permiso para ejecutar este comando.')

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
        contenido = f'{resultado}\n{url}'

        if len(contenido)> 2000:
            contenido = contenido[::1997] + '...\n' + url

        return contenido

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
async def img(ctx, *, query):
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

            embed = discord.Embed(title=title, url=url_page, description= f'Resultados para **{query}**', color=discord.Color.yellow())
            embed.set_image(url=link)
            embed.set_footer(text=f'{url_page}')

            await ctx.send(embed=embed)
        else:
            await ctx.send('No se encontaron resultados')
    
    except Exception as e:
        await ctx.send(f'Ha ocurrido un error al buscar la imagen {e}')

@bot.command()
async def google(ctx, *, query):
    try:
        service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=SEARCH_API_KEY)
        res = service.cse().list(
            q=query, cx=CSE_ID, num=3, safe='active'
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

reddit = praw.Reddit(
    client_id = '',
    client_secret = '',
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

        embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
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

        embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
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

        embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
        embed.set_image(url=meme_url)
        embed.set_footer(text=f"Fuente: r/shitposting")
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron memes.")

@bot.command()
async def cat(ctx):
    subreddit = reddit.subreddit("cats")
    cat_post = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

    cat_images = [post for post in cat_post if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    if cat_images:
        cat_post = random.choice(cat_images)
        cat_title = cat_post.title
        cat_url = cat_post.url
        cat_post_link = f"https://reddit.com{cat_post.permalink}"

        embed = discord.Embed(title=cat_title, url=cat_post_link, color=discord.Color.orange())
        embed.set_image(url=cat_url)
        embed.set_footer(text=f"Fuente: r/cats")
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se encontraron memes.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f'Avatar de {member.display_name}', color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

bot.remove_command('help')
@bot.command()
@commands.cooldown(rate=1, per=12000, type=commands.BucketType.guild)
async def help(ctx):
  embed = discord.Embed(title='**HOLA!**', description = 'Soy un bot en desarrollo(versión beta sujeta a cambios) creado por ANGELUS11, mi prefijo es > y lo puedes utilizar para diferentes comandos\n\n>diamond: ¿Quién soy?\n\n>img: Busca una imagen en Google\n\n>google: Hace una búsqueda simple en Google\n\n>yt: Buscar un video en YouTube\n\n>wiki: Buscar un artículo en Wikipedia\n\n>meme/dankmeme/shitpost: Mandar un meme random de Reddit\n\n>cat:Muestra una imagen random de gatitos :3\n\n>avatar: Mostrar el avatar de un usuario\n\n>spotify (username): Ver que está escuchando tú o un miembro en Spotify\n\n>binary: Convierte un valor entero a binario (no se para que quieras esto pero ahi está)\n\n>ocr(local): Extrae texto de imágenes en varios idiomas con el motor Tesseract https://github.com/tesseract-ocr/tesseract \n\n>dl(local): Descarga videos de varios sitios web para enviarlos a discord, usa YT_DLP en local, una herramienta de código abierto utilizada para descargar videos en múltiples sitios web https://github.com/yt-dlp/yt-dlp \n\n>translate(prefijo de idioma, texto), traduce texto en distintos idiomas\n\n>madewith: Información técnica sobre el bot\n\nRedes de ANGELUS: https://angelusd11.github.io/', 
  color=discord.Color.green())
  embed.set_image(url='https://panels.twitch.tv/panel-792145813-image-ec083130-b0fd-42ab-a88d-250e6ebe5c80')
  embed.set_footer(text='Este comando tiene cooldown de 3 horas')
  await ctx.send(embed = embed)

@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(rate=1, per=12000, type=commands.BucketType.guild)
async def madewith(ctx):
  embed = discord.Embed(title='**Created with Python3.12 by ANGELUS11**\n\ndiscord.py', description='You can find the source code in:\n https://github.com/ANGELUSD11/TDMBOT \nHosting:\n https://bot-hosting.net/ \nSupport:\n https://discord.gg/eTnPfUev3m', 
  color=discord.Color.dark_blue())
  embed.set_image(url='https://images.opencollective.com/discordpy/25fb26d/logo/256.png')
  embed.set_footer(text='Este comando tiene cooldown de 3 horas')
  await ctx.send(embed=embed)

@madewith.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(rate=1, per=12000, type=commands.BucketType.guild)
async def redes (ctx):
    if str(ctx.author.id) in allowed_users:
        embed = discord.Embed(description= '**REDES DE ANGELUS**\n YouTube: https://www.youtube.com/channel/UCFYLLqA03vesXUt-3eTP81A\n Twitch: https://www.twitch.tv/angelusd11', color = discord.Color.blue())
        embed.set_image(url= 'https://panels.twitch.tv/panel-792145813-image-5131cc5e-a31b-48bb-91bb-0133e967aa59')
        embed.set_image(url= 'https://media.discordapp.net/attachments/1015682580252729475/1146960229012086784/Screenshot_20230831-1909592.png?width=1007&height=701')
        await ctx.send(embed=embed)
    else:
        await ctx.send('No tienes permiso para ejecutar este comando')

@redes.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 10000, commands.BucketType.user)
async def ytchannel (ctx):
    if str(ctx.author.id) in allowed_users:
        embed = discord.Embed(description = "**CANAL DE YOUTUBE**\n\nhttps://www.youtube.com/channel/UCFYLLqA03vesXUt-3eTP81A", color=discord.Color.red())
        embed.set_image(url='https://panels.twitch.tv/panel-792145813-image-5131cc5e-a31b-48bb-91bb-0133e967aa59')
        await ctx.send(embed=embed)
    else:
        await ctx.send('No tienes permiso para ejecutar este comando')

@yt.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
@commands.cooldown(1, 10000, commands.BucketType.user)
async def twitch (ctx):
    if str(ctx.author.id) in allowed_users:
        embed = discord.Embed(description="**CANAL DE TWITCH**\n\nhttps://www.twitch.tv/angelus11t", color=discord.Color.purple())
        embed.set_image(url='https://cdn.discordapp.com/attachments/1015682580252729475/1146960229012086784/Screenshot_20230831-1909592.png')
        await ctx.send(embed=embed)
    else:
        await ctx.send('No tienes permiso para ejecutar este comando.')

@twitch.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
async def binary(ctx, number: str):
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
    frames = [
        "[          ] 0%",
        "[=         ] 10%",
        "[==        ] 20%",
        "[===       ] 30%",
        "[====      ] 40%",
        "[=====     ] 50%",
        "[======    ] 60%",
        "[=======   ] 70%",
        "[========  ] 80%",
        "[========= ] 90%",
        "[==========] 100%"
    ]

    loading_message = await ctx.send('Thinking...')
    
    for frame in frames:
        await loading_message.edit(content=f'Downloading image... {frame}')
        await asyncio.sleep(0.3)
    await loading_message.edit(content='Processing image...')

    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url

        try:
            if ctx.message.attachments[0].size > 5 * 1024 * 1024:
                await ctx.send('La imagen es demasiado grande, sube una imagen de menos de 5mb')
                return

            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            text = pytesseract.image_to_string(img, lang='eng+rus+ara+afr+amh+asm+aze_cyrl+bel+bod+bos+bre+bul+cat+ceb+ces+chi_sim+chi_sim_vert+chr+cos+cym+dan+dan_frak+deu+deu_frak+deu_latf+div+dzo+ell+enm+epo+equ+est+eus+fao+fas+fil+fin+fra+frm+fry+gla+gle+glg+grc+guj+hat+heb+hin+hrv+hun+hye+iku++ind+isl+ita+ita_old+jav+jpn+jpn_vert+kan+kat+kat_old+kaz+khm+kir+kmr+kor+kor_vert+lao+lat+lav+lit+ltz+mal+mar+mkd+mlt+mon+mri+msa+mya+nep+nld+nor+oci+ori+osd+pan+pol+por+pus+que+ron+san+sin+slk+slk_frak+slv+snd+spa+spa_old+sqi+srp+srp_latn+sun+swa+swe+syr+tam+tat+tel+tgk+tgl+tha+tir+ton+tur+uig+ukr+urd++uzb+uzb_cyrl+vie+yid+yor')

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
        embed = discord.Embed(title=f'{member.display_name} está escuchando {activity.title}', description=f'Artista: {activity.artist}\nÁlbum: {activity.album}', color=activity.colour)
        embed.set_thumbnail(url=activity.album_cover_url)
        embed.add_field(name='Duración: ', value=str(activity.duration), inline=True)
        embed.add_field(name='Escuchar en Spotify', value=f'[Link]({activity.track_url})', inline=True)

        await ctx.send(embed=embed)

    else:
        await ctx.send(f'{member.display_name} no está escuchando música en Spotify en este momento.')

@bot.command()
async def stream(ctx, member: discord.Member = None):

    member = member or ctx.author
    activity = next((activity for activity in member.activities if isinstance(activity, discord.Streaming) and activity.platform == 'Twitch'), None)

    if activity:
        embed = discord.Embed(title=f'{member.display_name} está transmitiendo en vivo, ve a verlo!', url=activity.url, description=f'Jugando a: {activity.game}', color=discord.Color.purple())
        embed.add_field(name='Título', value=activity.details, inline=False)
        embed.set_thumbnail(url=member.avatar.url)     

        await ctx.send(embed=embed)

    else:
        await ctx.send(f'{member.display_name} no está transmitiendo en Twitch en este momento.')

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def chat (ctx, *, mensaje: str = None):
    if not mensaje:
        await ctx.send('Dí algo para que el bot lo repita.')
        return
    await ctx.send(mensaje)

@chat.error
async def chat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")

@bot.command()
async def dl(ctx, url: str):
    frames = [
        "[          ] 0%",
        "[=         ] 10%",
        "[==        ] 20%",
        "[===       ] 30%",
        "[====      ] 40%",
        "[=====     ] 50%",
        "[======    ] 60%",
        "[=======   ] 70%",
        "[========  ] 80%",
        "[========= ] 90%",
        "[==========] 100%"
    ]

    loading_message = await ctx.send('Downloading...')
    
    for frame in frames:
        # Edit the message with the current loading frame
        await loading_message.edit(content=f'Downloading... {frame}')
        await asyncio.sleep(0.3)

    await loading_message.edit(content='Download complete!')

    # Define la función de gancho de progreso
    def progress_hook(d):
        if d['status'] == 'finished':
            print(f"Finished downloading: {d['filename']}")


    # Configuración de opciones para yt-dlp / opción config yt_dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Cambiado para evitar fusión
        'outtmpl': './%(title)s.%(ext)s',  # Guarda el video en el directorio actual con el nombre del título
        'ffmpeg_location': '/home/container/ffmpeg/bin',
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'cookieFile': cookies_file,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Obtén el nombre del archivo descargado
        filename = f"{ydl.prepare_filename(ydl.extract_info(url))}"
        
        # Verifica si el archivo existe
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                await ctx.send(file=discord.File(file, filename=filename))
            os.remove(filename)
        else:
            await ctx.send("No se pudo encontrar el archivo descargado.")

    except Exception as e:
        embed = discord.Embed(title='❌ERROR!', description=f'No se pudo enviar el video, puede que sea muy largo o pesado\n {e}', color=discord.Color.red())
        await ctx.send(embed=embed)
        print(f"Ocurrió un error: {e}")

@bot.command()
async def translate(ctx, lang: str, *, text: str):
    #Comando de traducción que usa Google Translate desde deep-translator.
    # Validación del texto
    if not text.strip():
        await ctx.send("Por favor, proporciona el texto a traducir.")
        return
    
    try:
        # Traducir el texto usando Google Translator de deep-translator
        translated = GoogleTranslator(source='auto', target=lang).translate(text=text)
        
        # Enviar la traducción al canal
        await ctx.send(f"Texto original: {text}\nTraducción a {lang}: {translated}")

    except Exception as e:
        await ctx.send(f"Error al traducir: {e}")

@bot.command()
async def translateinfo(ctx):
    embed = discord.Embed(
        title='Prefijos de idioma para el comando >translate',
        description='Aquí tienes algunos ejemplos de prefijos de idiomas:\n',
        color=discord.Color.blue()
    )
    embed.add_field(name='Español', value='es', inline=True)
    embed.add_field(name='Inglés', value='en', inline=True)
    embed.add_field(name='Francés', value='fr', inline=True)
    embed.add_field(name='Alemán', value='de', inline=True)
    embed.add_field(name='Italiano', value='it', inline=True)
    embed.add_field(name='Portugués', value='pt', inline=True)
    embed.add_field(name='Ruso', value='ru', inline=True)
    embed.add_field(name='Chino (Simplificado)', value='zh-cn', inline=True)
    embed.add_field(name='Chino (Tradicional)', value='zh-tw', inline=True)
    embed.add_field(name='Japonés', value='ja', inline=True)
    embed.add_field(name='Coreano', value='ko', inline=True)
    embed.add_field(name='Árabe', value='ar', inline=True)
    embed.add_field(name='Hindi', value='hi', inline=True)
    embed.add_field(name='Turco', value='tr', inline=True)
    embed.add_field(name='Griego', value='el', inline=True)
    embed.add_field(name='Holandés', value='nl', inline=True)
    embed.add_field(name='Sueco', value='sv', inline=True)

    embed.add_field(
        name='Más información sobre los códigos de idioma:',
        value='[Consulta ISO 639-1](https://es.wikipedia.org/wiki/ISO_639-1)',
        inline=False
    )

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        return
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('El comando mencionado no existe.')
    elif isinstance(error, discord.ext.commands.MemberNotFound):
        await ctx.send('El miembro mencionado no existe, asegúrate de escribirlo correctamente')
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send(f'Falta un argumento requerido: {error.param}')
    elif isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send('Error en el argumento proporcionado, verifica que lo escribiste correctamente.')
    else:
        #registra cualquier otro error en terminal para depuración
        print(f'Error name exeption: {type(error).__name__} - {error}')

bot.run(DISCORD_TOKEN)
