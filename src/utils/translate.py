#itils/translate.py
import discord
from discord.ext import commands
from googletrans import Translator

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class WikipediaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

bot = commands.Bot(command_prefix='>', intents=intents)

translator = Translator()

@bot.command()
@commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
async def translate(ctx, lang: str = None, *, text: str = None):
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
    #Comando de traducción que usa Google Translate desde deep-translator.
    # Validación del texto
    if not text or not text.strip():
        await ctx.send("Por favor proporciona un texto a traducir.")
        return

    if not lang or not lang.strip():
        await ctx.send("Por favor proporciona un idioma a traducir.")
        return

    lang = lang.strip().lower()

    if lang not in valid_lang:
        await ctx.send("Por favor proporciona un idioma válido a traducir.")
        return

    if len(text) > 500:
        await ctx.send("El texto es demasiado largo, por favor escribe un texto más corto.")
        return
    
    try:
        # Traducir el texto usando Google Translator de deep-translator
        translated = GoogleTranslator(source='auto', target=lang).translate(text=text)
        
        # Enviar la traducción al canal
        await ctx.send(f"**Texto original**: {text}\n**Traducción a {lang}**: {translated}")

    except Exception as e:
        await ctx.send(f"Error al traducir, intentalo nuevamente más tarde")
        #intern log sensitive information
        print(f'Error: {e}')

@translate.error
async def translate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tiempo_restante = round(error.retry_after)
        await ctx.send(f"Debes esperar {tiempo_restante} segundos antes de usar el comando nuevamente.")


def setup(bot):
    bot.add_cog(WikipediaCog(bot))
