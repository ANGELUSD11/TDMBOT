import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

class ConvertCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def text_to_bin(self, text):
        return ' '.join(format(byte, '08b') for byte in text.encode('utf-8'))
    
    def bin_to_text(self, bin):
        try:
            if ' ' not in bin:
                bin = ' '.join(bin[i:i+8] for i in range(0, len(bin), 8))
            bytes_list = [int(b, 2) for b in bin.split()]
            return bytes(bytes_list).decode('utf-8')
        except Exception as e:
            return f"❌ Error al decodificar: {e}"

    def if_not_bin(self, text):
        # Elimina espacios para validar longitud si es una sola cadena
        sin_espacios = text.replace(' ', '')
        if len(sin_espacios) % 8 != 0:
            return False  # No divisible en bloques de 8

        # Valida cada bloque
        bloques = sin_espacios if ' ' not in text else text.split()
        if isinstance(bloques, str):  # Si es una sola cadena, la partimos en bloques de 8
            bloques = [bloques[i:i+8] for i in range(0, len(bloques), 8)]

        return all(len(b) == 8 and all(char in "01" for char in b) for b in bloques)
        
    @commands.command()
    async def convert(self, ctx, modo: str, *, entrada: str):
        if modo.lower() == "to_bin":
            resultado = self.text_to_bin(entrada)
            await ctx.send(f"🔤 ➡️ 🧠\n```{resultado}```")
        elif modo.lower() == "to_text":
            if not self.if_not_bin(entrada):
                await ctx.send("❌ El valor ingresado no es válido.")
                return
            resultado = self.bin_to_text(entrada)
            await ctx.send(f"🧠 ➡️ 🔤\n```{resultado}```")
        else:
            await ctx.send("❌ Modo inválido. Usa `to_bin` o `to_text`.")

async def setup(bot):
    await bot.add_cog(ConvertCog(bot))
