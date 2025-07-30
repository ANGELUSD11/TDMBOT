import discord
from discord import FFmpegPCMAudio
from ..core.ttsengine import generate_speech
import discord.ext
import os
from discord.ext import commands
import tesserocr
import requests
import asyncio
import yt_dlp
from deep_translator import GoogleTranslator
from PIL import Image
import io
from io import BytesIO
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

model = genai.GenerativeModel("gemini-1.5-flash")
#chat = model.start_chat(history=[])

class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini_api = os.getenv("GEMINI_API_KEY")
        self.ffmpeg_path = os.getenv("FFMPEG_PATH")

        genai.configure(api_key= self.gemini_api)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ocr(self, ctx, lang="eng"):

        idiomas_disponibles = [
        "spa", "eng", "ara", "afr", "rus", "chi_sim", "chi_tra", "fra", "deu", "ita", "jpn",
        "kor", "hin", "tur", "por", "nld", "ukr", "pol", "ces", "dan", "swe", "nor",
        "fin", "hun", "bul", "gre", "heb", "tha", "vie", "ind", "mal", "tam", "tel",
        "ben", "urd", "amh", "mya", "nep", "mar", "kan", "guj", "ori", "pan", "sin",
        "khm", "lao", "tat", "uzb", "aze", "kat", "mon", "bos", "slv", "lit", "lav",
        "est", "isl", "sqi", "mkd", "bre", "cor", "glg", "eus", "fao", "mri", "swa"
        ]

        if lang not in idiomas_disponibles:
            await ctx.send(f"❌ Idioma no válido. Usa: {', '.join(idiomas_disponibles)}.")
            return

        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url

            try:
                if ctx.message.attachments[0].size > 5 * 1024 * 1024:
                    await ctx.send('⚡La imagen es demasiado grande, sube una imagen de menos de 5mb')
                    return

                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                image_path = "/tmp/temp_image.png"
                img.save(image_path)

                with tesserocr.PyTessBaseAPI(lang=lang, path="/home/container/Tesseract-OCR/tessdata") as api:
                    api.SetImageFile(image_path)
                    text = api.GetUTF8Text()

                if text.strip():
                    embed = discord.Embed(title='Texto extraido', description=text[:1024], color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('❌Error, no se encontró texto en la imagen')

            except Exception as e:
                await ctx.send(f'Ocurrió un error al procesar la imagen: {str(e)}.')

            finally:
                if os.path.exists(image_path):
                    os.remove(image_path)
        else:
            await ctx.send('Por favor adjunta una imagen a procesar.')

    @ocr.error
    async def ocr_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after)
            await ctx.send(f'❌Por favor espera {remaining_time} segundos antes de usar el comando nuevamente.')

    @commands.command()
    async def dl(self, ctx, url: str):
        # Detectar la plataforma y configurar las opciones adecuadas
        if 'x.com' in url or 'twitter.com' in url:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'merge_output_format': 'mp4',
                'outtmpl': '%(id)s.%(ext)s',  # Guarda con el ID del video
                'quiet': True,
            }
        elif 'instagram.com' in url:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'outtmpl': '%(id)s.%(ext)s',
                'quiet': True,
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'outtmpl': '%(id)s.%(ext)s',
                'quiet': True,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                # En caso de playlist, tomar solo el primer video
                if 'entries' in info:
                    info = info['entries'][0]

                # Obtener el nombre del archivo descargado
                filename = ydl.prepare_filename(info)

            # Verificar si el archivo existe
            if os.path.exists(filename):
                # Verificar tamaño del archivo
                if os.path.getsize(filename) > 8 * 1024 * 1024:
                    await ctx.send("⚠️ El archivo es demasiado grande para enviarse por Discord (8 MB).")
                    os.remove(filename)
                    return

                # Enviar el archivo al canal de Discord
                with open(filename, 'rb') as f:
                    await ctx.send(file=discord.File(f, filename=os.path.basename(filename)))

                # Eliminar el archivo después de enviarlo
                os.remove(filename)

            else:
                await ctx.send("❌ No se encontró el archivo descargado.")

        except Exception as e:
            embed = discord.Embed(
                title='❌ ¡ERROR!',
                description=f'No se pudo enviar el video, puede que sea muy largo o pesado.\n\n**Error:** `{str(e)}`',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            print(f"[ERROR] Ocurrió un error al intentar descargar el video: {e}")



    @commands.command()
    async def translate(self, ctx, lang: str, *, text: str=None):
        #this list contains all the valid language codes
        valid_lang = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as',
                      'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm', 
                      'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 
                      'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee', 
                      'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 
                      'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 
                      'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 
                      'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 
                      'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk', 
                      'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'ku', 'kv', 'kw', 
                      'ky', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 
                      'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 
                      'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 
                      'no', 'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 
                      'pa', 'pi', 'pl', 'ps', 'pt', 'qc', 'rm', 'rn', 'ro', 
                      'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 
                      'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 
                      'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 
                      'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 
                      'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 
                      'yo', 'za', 'zh', 'zu']
        if not text or not text.strip() and not lang or not lang.strip():
            await ctx.send('Por favor proporciona texto e idioma a traducir (idioma, texto).')
            return
        lang = lang.strip().lower()

        if lang not in valid_lang:
            await ctx.send('Por favor proporciona un idioma válido a traducir, >translateinfo.')
            return
        if len(text) > 500:
            await ctx.send('El texto es demasiado largo, escribe uno más corto.')
            return
        
        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(text=text)
            for i in range(0, len(translated), 2000):
                await ctx.send(f"**Texto original:** {text}\n**Traducción a {lang}:** {translated[i:i+2000]}")
        except Exception as e:
            await ctx.send('Ocurrió un error al traducir, intentelo más tarde.')
            print(e)

    @commands.command()
    async def translateinfo(self, ctx):
        embed = discord.Embed(
            title='Prefijos de idioma para >translate',
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

    @commands.command()
    async def ia(self, ctx, *, prompt: str = None):
        if not prompt:
            await ctx.send('Escribe algo para preguntarle a la IA de Gemini.')
            return
        try:
            contexto_base = (
                "Estás integrada en un bot de Discord desarrollado por ANGELUS11, un desarrollador colombiano. "
                "Responde siempre de forma clara, concisa y útil ante las dudas de los usuarios. "
            )

            prompt_final = f'{contexto_base} Usuario: {prompt}'
            
            if ctx.message.attachments:
                image_url = ctx.message.attachments[0].url
                img_response = requests.get(image_url)
                image_bytes = img_response.content

                image = Image.open(BytesIO(image_bytes))
                img_iaresponse = model.generate_content([prompt_final, image])
                text = img_iaresponse.text
            else:
                response = model.generate_content(prompt_final)
                text = response.text

            for i in range(0, len(text), 2000):
                await ctx.send(text[i:i+2000])

            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if voice_client and voice_client.is_connected():
                audio_path = generate_speech(text)
                voice_client.audio_path = audio_path 
                try:
                    if not voice_client.is_playing():
                        voice_client.play(
                            FFmpegPCMAudio(audio_path, executable=self.ffmpeg_path),
                            after=lambda e: os.remove(audio_path) if os.path.exists(audio_path) else None
                        )
                finally:
                    if os.path.exists(audio_path) and not voice_client.is_playing():
                        os.remove(audio_path)
                        
        except ResourceExhausted as e:
            await ctx.send('⚠️ La IA ha alcanzado su límite de uso. Inténtalo más tarde.')
            await asyncio.sleep(55)
            print(f"[ERROR] ResourceExhausted error in the AI command: {e}")

        except Exception as e:
            await ctx.send('An error occurred while processing your request.')
            print(f"[ERROR] A error occurred in the AI command:\n{e}")

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
