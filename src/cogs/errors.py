import discord
import discord.ext
from discord.ext import commands

class ErrorsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            return
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send('This command does not exist.')
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send('The mentioned member does not exist, make sure you type it correctly.')
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'A required argument is missing: {error.param}')
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send('Error in the argument provided, check that you wrote it correctly.')
        #other errors in terminal
        else:
            print(f'Error name exception: {type(error).__name__} - {error}')

async def setup(bot):
    await bot.add_cog(ErrorsCog(bot))
