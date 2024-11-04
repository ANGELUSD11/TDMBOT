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

@bot.command
async def translate(ctx, lang: str, *, text: str):
    try:
        translation = translator.translate(text=text, lang=lang)
        await ctx.send(f'**Texto original:**{text}\n**Traducción ({lang}):**{translation.text}')
    except Exception as e:
        await ctx.send(f'Ocurrió un error al traducir: {e}')

def setup(bot):
    bot.add_cog(WikipediaCog(bot))