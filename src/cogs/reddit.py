import discord
import os
import discord.ext
import asyncio
from dotenv import load_dotenv
import praw
import random
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds= True

reddit = praw.Reddit(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    user_agent = 'discord_bot:v1.0.0 (by u/ANGELUSR11)'
)

class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        subreddit = reddit.subreddit("MemesESP")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            meme_title = meme.title
            meme_url = meme.url
            meme_post_link = f"https://reddit.com{meme.permalink}"

            embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Fuente: r/MemesESP")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

    @commands.command()
    async def shitpost(self, ctx):
        subreddit = reddit.subreddit("shitposting")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            meme_title = meme.title
            meme_url = meme.url
            meme_post_link = f"https://reddit.com{meme.permalink}"

            embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Fuente: r/shitposting")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

    @commands.command()
    async def cat(self, ctx):
        subreddit = reddit.subreddit("cats")
        memes = [submission for submission in subreddit.hot(limit=50) if not submission.stickied]

        image_memes = [meme for meme in memes if meme.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_memes:
            meme = random.choice(image_memes)
            meme_title = meme.title
            meme_url = meme.url
            meme_post_link = f"https://reddit.com{meme.permalink}"

            embed = discord.Embed(title=meme_title, url=meme_post_link, color=discord.Color.orange())
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Fuente: r/cats")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontraron memes de imágenes.")

async def setup(bot):
    await bot.add_cog(RedditCog(bot)) 
