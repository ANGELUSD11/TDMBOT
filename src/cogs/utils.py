import discord
import discord.ext
import os
from discord.ext import commands
import pytesseract
import requests
import asyncio
import yt_dlp
from deep_translator import GoogleTranslator
from PIL import Image
from io import BytesIO
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

pytesseract.pytesseract.tesseract_cmd = r'/home/container/Tesseract-OCR/tesseract.exe'
model = genai.GenerativeModel("gemini-1.5-flash")
#chat = model.start_chat(history=[])

class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini_api = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key= self.gemini_api)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ocr(self, ctx):
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
                    await ctx.send('⚡La imagen es demasiado grande, sube una imagen de menos de 5mb')
                    return

                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))

                text = pytesseract.image_to_string(img, lang='eng+rus+ara+afr+amh+asm+aze_cyrl+bel+bod+bos+bre+bul+cat+ceb+ces+'
                                                            'chi_sim+chi_sim_vert+chr+cos+cym+dan+dan_frak+deu+deu_frak+deu_latf'
                                                            '+div+dzo+ell+enm+epo+equ+est+eus+fao+fas+fil+fin+fra+frm+fry+gla+gle+'
                                                            'glg+grc+guj+hat+heb+hin+hrv+hun+hye+iku++ind+isl+ita+ita_old+jav+jpn+'
                                                            'jpn_vert+kan+kat+kat_old+kaz+khm+kir+kmr+kor+kor_vert+lao+lat+lav+lit+'
                                                            'ltz+mal+mar+mkd+mlt+mon+mri+msa+mya+nep+nld+nor+oci+ori+osd+pan+pol+por'
                                                            '+pus+que+ron+san+sin+slk+slk_frak+slv+snd+spa+spa_old+sqi+srp+srp_latn+'
                                                            'sun+swa+swe+syr+tam+tat+tel+tgk+tgl+tha+tir+ton+tur+uig+ukr+urd++uzb+uzb_cyrl'
                                                            '+vie+yid+yor')

                if text.strip():
                    embed = discord.Embed(title='Texto extraido', description=text[:1024], color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('❌Error, no se encontró texto en la imagen')

            except Exception as e:
                await ctx.send(f'Ocurrió un error al procesar la imagen: {str(e)}.')
        else:
            await ctx.send('Por favor adjunta una imagen a procesar.')

    @ocr.error
    async def ocr_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after)
            await ctx.send(f'❌Por favor espera {remaining_time} segundos antes de usar el comando nuevamente.')

    @commands.command()
    async def dl(self, ctx, url: str):
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

        def progress_hook(d):
            if d['status'] == 'finished':
                print(f"Finished downloading: {d['filename']}")

        #options for downloads
        if 'instagram.com' in url:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Cambiado para evitar fusión
                'outtmpl': './%(title)s.%(ext)s',  # Guarda el video en el directorio actual con el nombre del título
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'progress_hooks': [progress_hook]
            }

        elif 'youtube.com' in url:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Cambiado para evitar fusión
                'outtmpl': './%(title)s.%(ext)s',  # Guarda el video en el directorio actual con el nombre del título
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'progress_hooks': [progress_hook]
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Cambiado para evitar fusión
                'outtmpl': './%(title)s.%(ext)s',  # Guarda el video en el directorio actual con el nombre del título
                'ffmpeg_location': '/home/container/ffmpeg/bin',
                'noplaylist': True,
                'progress_hooks': [progress_hook]
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        
            filename = f"{ydl.prepare_filename(ydl.extract_info(url))}"
        
            # Verify if the file exist
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

    @commands.command()
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
    async def translate(self, ctx, lang: str, *, text: str=None):
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
            await ctx.send(f"**Texto original:** {text}\n**Traducción a {lang}:** {translated}")
        except Exception as e:
            await ctx.send('Ocurrió un error al traducir, intentelo más tarde.')
            print(e)

    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = round(error.retry_after)
            await ctx.send(f'Debes esperar {remaining_time} segundos antes de usar el comando nuevamente.')

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
            if ctx.message.attachments:
                image_url = ctx.message.attachments[0].url
                img_response = requests.get(image_url)
                image_bytes = img_response.content

                image = Image.open(BytesIO(image_bytes))

                prompt = f'Responde única y exclusivamente en español, no uses otros idiomas: {prompt}'

                img_iaresponse = model.generate_content([prompt, image])

                text = img_iaresponse.text

                for i in range(0, len(text), 2000):
                    await ctx.send(text[i:i+2000])

            else:
                response = model.generate_content(prompt)
                text = response.text
                for i in range(0, len(text), 2000):
                    await ctx.send(text[i:i+2000])

        except Exception as e:
            await ctx.send('Ocurrió un error al generar una respuesta.')
            print(e)

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
