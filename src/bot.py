import os
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import requests
import asyncio
import json
import grpc
import logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True
bot = commands.Bot(command_prefix = '>', intents = intents)

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '.env')
load_dotenv(dotenv_path=env_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL = os.getenv("DISCORD_CHANNEL")
GENERAL_CHANNEL = os.getenv("GENERAL_CHANNEL")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CSE_ID = os.getenv("CSE_ID")
SERVER_ID = os.getenv("SERVER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

#valid user ids
allowed_users = ['472146563758686208', '580904606771445783']

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    activity = discord.Activity(type=discord.ActivityType.watching, name='ANGELUS11💠|>')
    await bot.change_presence(activity=activity)
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    
    if os.path.exists(cogs_dir):
        
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await bot.load_extension(cog_name)
                    print(f'Cog {cog_name} cargado con éxito.')
                except Exception as e:
                    print(f'Error al cargar el cog: {cog_name}: {e}')

    channel_ids = [747832973214351382, 982093327799312404]
    start_message = 'Bot started!'
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        #if the bot find channel
        if channel:
            await channel.send(start_message)
        else:
            print(f'No se pudo encontrar el canal: {channel_id}')

    check_new_video.start()
    check_live_stream.start()

@bot.event
async def on_shutdown():
    print('Closing conexions...')
    try:
        grpc.shutdown()
    except Exception as e:
        print(f'Error: {e}')

    print('Bot shutdown.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    elif message.content.lower() == 'hola':
        await message.channel.send(f'hola {message.author.name}')
    
    elif message.content.lower() == 'que':
        await message.channel.send('so')

    elif message.content.lower() == 'rra':
        await message.channel.send('llado')
    
    # Procesar otros comandos
    await bot.process_commands(message)

# /global variable for last yt video
last_video_id = None
# /global variable for last yt stream
last_live_id = None

#verify and notify latest video in the channel 
@tasks.loop(minutes=60)
async def check_new_video():
    global last_video_id
    url = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1'
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    if 'items' in data and data['items']:
        latest_video = data['items'][0]
        #la variable video_id contiene el video actual
        video_id = latest_video['id']['videoId']
        #last_video_id contiene el último video encontrado mientras que video_id contiene el video actual
        if video_id != last_video_id:
            last_video_id = video_id
            try:
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                channel = await bot.fetch_channel(DISCORD_CHANNEL)
                await channel.send(f'@everyowone ANGELUS11💠 ha subido un nuevo video :D ve a verlo!\n{video_url}')
            except discord.NotFound:
                print(f'No se pudo encontrar el canal con el id: {DISCORD_CHANNEL}')
            except discord.Forbidden:
                print(f'El bot no tiene permisos para enviar mensajes al canal: {DISCORD_CHANNEL}')
    else:
        print('No se encontraron videos.')
        return

@check_new_video.before_loop
async def before_check_new_video():
    await bot.wait_until_ready()


#verify and notify latest livestream in the channel 
@tasks.loop(minutes=10)
async def check_live_stream():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&type=video&eventType=live&key={YOUTUBE_API_KEY}"
    global last_live_id
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    if 'items' in data and data['items']:
        latest_live = data['items'][0]
        live_id = latest_live['id']['videoId']

        # Verifica si hay una nueva transmisión en vivo
        if live_id != last_live_id:
            last_live_id = live_id
            try:
                live_url = f'https://www.youtube.com/watch?v={live_id}'
                channel = await bot.fetch_channel(GENERAL_CHANNEL)
                await channel.send(f'@everyowone ¡ANGELUS11💠 ha comenzado una transmisión en vivo!\n{live_url}')
            except discord.NotFound:
                print(f'No se pudo encontrar el canal con el id: {GENERAL_CHANNEL}')
            except discord.Forbidden:
                print(f'El bot no tiene permisos para enviar mensajes al canal: {GENERAL_CHANNEL}')
    else:
        print('No se encontraron streams.')
        return

@check_live_stream.before_loop
async def before_check_live_stream():
    await bot.wait_until_ready()

bot.run(DISCORD_TOKEN)
