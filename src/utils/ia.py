import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands
from discord.ext import tasks
from PIL import Image
from io import BytesIO
import requests
import discord.ext.commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True
bot = commands.Bot(command_prefix = '>', intents = intents)

GEMINI_API_KEY = 'AIzaSyBW4ZB-F62rFw0wJ_st_E_dza-pTIRjRR8'

genai.configure(api_key= GEMINI_API_KEY)
model = genai.GenerativeModel('Gemini-1.5-flash')
chat = model.start_chat(history=[])

@bot.command()
async def ia(ctx, *, mensaje: str = None):
    if not mensaje:
        await ctx.send('Escribe algo para preguntarle a la IA de Gemini.')
        return
    try:
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
            img_response = requests.get(image_url)
            image_bytes = img_response.content

            image = Image.open(BytesIO(image_bytes))

            img_iaresponse = model.generate_content([mensaje, image])

            text = img_iaresponse.text
            
            for i in range(0, len(text), 2000):
                await ctx.send(text[i:i+2000])
        else:
            response = model.generate_content(mensaje)
            text = response.text
            for i in range(0, len(text), 2000):
                await ctx.send(text[i:i+2000])
    except Exception as e:
        await ctx.send('Hubo un error al generar una respuesta:')
        print(e)