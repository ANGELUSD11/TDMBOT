import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

class ConvertCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def text_to_bin(self, text):
        return ' '.join(format(byte, '08b') for byte in text.encode('utf-8'))
    
    def bin_to_text(self, bin):
        try:
            bytes_list = [int(b, 2) for b in bin.split()]
            return bytes(bytes_list).decode('utf-8')
        except Exception as e:
            return f"❌ Error al decodificar: {e}"
        
    @commands.command()
    async def convertir(self, ctx, modo: str, *, entrada: str):
        if modo.lower() == "a_binario":
            resultado = self.text_to_bin(entrada)
            await ctx.send(f"🔤 ➡️ 🧠\n```{resultado}```")
        elif modo.lower() == "a_texto":
            resultado = self.bin_to_text(entrada)
            await ctx.send(f"🧠 ➡️ 🔤\n```{resultado}```")
        else:
            await ctx.send("❌ Modo inválido. Usa `a_binario` o `a_texto`.")

async def setup(bot):
    await bot.add_cog(ConvertCog(bot))