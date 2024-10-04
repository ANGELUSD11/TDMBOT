# cogs/fun.py
import discord
from discord.ext import commands
import random
import praw

from utils.config import (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)

# Inicializar Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        """Envía un meme del subreddit MemesESP."""
        subreddit = reddit.subreddit("MemesESP")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]
        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            embed = discord.Embed(title=meme.title, url=f"https://reddit.com{meme.permalink}")
            embed.set_image(url=meme.url)
            embed.set_footer(text="Fuente: r/MemesESP")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

    @commands.command()
    async def dankmeme(self, ctx):
        """Envía un meme del subreddit dankmemes."""
        subreddit = reddit.subreddit("dankmemes")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]
        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            embed = discord.Embed(title=meme.title, url=f"https://reddit.com{meme.permalink}")
            embed.set_image(url=meme.url)
            embed.set_footer(text="Fuente: r/dankmemes")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

    @commands.command()
    async def shitpost(self, ctx):
        """Envía un meme del subreddit shitposting."""
        subreddit = reddit.subreddit("shitposting")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            meme_title = meme.title
            meme_url = meme.url
            meme_post_link = f"https://reddit.com{meme.permalink}"

            embed = discord.Embed(title=meme_title, url=meme_post_link)
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Fuente: r/shitposting")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

def setup(bot):
    bot.add_cog(Fun(bot))
