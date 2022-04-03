# Imports
import requests
import discord
import random
from discord.ext import commands
from discord import Colour
from tools.tools import send_embed
import asyncpraw
import config

# Embed color
color = Colour.blue()

# For API requests
base_url = "https://api.truthordarebot.xyz/api"


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent='Syl by Huroatar'
        )

    @commands.command(aliases=['t'])
    async def truth(self, ctx):
        """Sends a PG truth question"""

        try:
            # Sending a request to the API
            r = requests.get(url=f"{base_url}/truth", params={'rating': 'pg'})

            # Extracting data in JSON format
            data = r.json()

            newEmbed = discord.Embed(
                title='Truth - PG', description=data['question'], color=color)
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=('I couldn\'t fetch a question.'
                             ' Please try again later.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['t pg13', 't_pg13'])
    async def truthpg13(self, ctx):
        """Sends a PG13 truth question"""

        try:
            # Sending a request to the API
            r = requests.get(url=f"{base_url}/truth",
                             params={'rating': 'pg13'})

            # Extracting data in JSON format
            data = r.json()

            newEmbed = discord.Embed(
                title='Truth - PG13',
                description=data['question'],
                color=color)
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=('I couldn\'t fetch a question.'
                             ' Please try again later.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['d'])
    async def dare(self, ctx):
        """Sends a PG dare question"""

        try:
            # Sending a request to the API
            r = requests.get(url=f"{base_url}/dare", params={'rating': 'pg'})

            # Extracting data in JSON format
            data = r.json()

            newEmbed = discord.Embed(
                title='Dare - PG', description=data['question'], color=color)
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=('I couldn\'t fetch a question.'
                             ' Please try again later.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['d pg13', 'd_pg13'])
    async def darepg13(self, ctx):
        """Sends a PG13 dare question"""

        try:
            # Sending a request to the API
            r = requests.get(url=f"{base_url}/dare", params={'rating': 'pg13'})

            # Extracting data in JSON format
            data = r.json()

            newEmbed = discord.Embed(
                title='Dare - PG13', description=data['question'], color=color)
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=('I couldn\'t fetch a question.'
                             ' Please try again later.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def hug(self, ctx):
        """A wholly wholesome hug command"""

        hugs_list = [
            "<@{}> and <@{}> lock themselves in a warm embrace.",
            "<@{}> gently hugs <@{}>.",
            "<@{}> tightly wraps their arms around <@{}> and never lets go.",
            "<@{}> and <@{}> share a hug. It is a very nice hug.",
            "<@{}> jumps and hugs <@{}> with glee.",
            ("<@{}> cuddles <@{}>. "
             "They share another one because hugs are good.")
        ]

        try:
            message = ctx.message
            if len(message.mentions) == 1:
                if ctx.author.id == message.mentions[0].id:
                    hug_text = (f"<@{ctx.author.id}> wraps their arms "
                                "around themself. Mood.")
                    newEmbed = discord.Embed(
                        description=hug_text,
                        color=color
                    )
                else:
                    i = random.randint(0, len(hugs_list) - 1)
                    newEmbed = discord.Embed(description=hugs_list[i].format(
                        ctx.author.id, message.mentions[0].id), color=color)
                await send_embed(ctx, newEmbed)

            elif len(message.mentions) < 5:
                hug_text = (f"<@{ctx.author.id}> has to stretch"
                            " their arms to embrace")
                for member in message.mentions:
                    hug_text += f" <@{member.id}> "
                newEmbed = discord.Embed(
                    description=hug_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

            else:
                hug_text = (f"<@{ctx.author.id}> equally distributes "
                            "hugs.")
                newEmbed = discord.Embed(
                    description=hug_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

        except Exception as e:

            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t execute that command.',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        """A wholly wholesome pat command"""

        pats_list = [
            "<@{}> gently pats <@{}>.",
            "<@{}> gives <@{}> a tender headpat.",
            "<@{}> vigorously headpats <@{}>. Everyone nods in approval.",
            "<@{}> and <@{}> pat each other. Quite a transaction, huh?",
            "<@{}> keeps patting <@{}> because they love it."
        ]

        try:
            message = ctx.message
            if len(message.mentions) == 1:
                if ctx.author.id == message.mentions[0].id:
                    pat_text = (f"<@{ctx.author.id}> raises an arm "
                                "to pat themself. Mood.")
                    newEmbed = discord.Embed(
                        description=pat_text,
                        color=color
                    )
                else:
                    i = random.randint(0, len(pats_list) - 1)
                    newEmbed = discord.Embed(description=pats_list[i].format(
                        ctx.author.id, message.mentions[0].id), color=color)
                    await send_embed(ctx, newEmbed)

            elif len(message.mentions) < 5:
                pat_text = (f"<@{ctx.author.id}> lightly pats")
                for member in message.mentions:
                    pat_text += f" <@{member.id}> "
                newEmbed = discord.Embed(
                    description=pat_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

            else:
                pat_text = (f"<@{ctx.author.id}> equally distributes"
                            "pats.")
                newEmbed = discord.Embed(
                    description=pat_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t execute that command.',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        """A wholly wholesome kiss command"""

        kiss_list = [
            "<@{}> gives <@{}> the greatest kiss of all time.",
            "The world comes to a halt as <@{}> and <@{}> kiss.",
            "<@{}> and <@{}> share a nice kiss.",
            "<@{}> tenderly plants a kiss atop <@{}>'s forehead."
        ]

        try:
            message = ctx.message
            if len(message.mentions) == 1:
                if ctx.author.id == message.mentions[0].id:
                    kiss_text = (f"<@{ctx.author.id}> joins their lips to "
                                 "kiss themself.")
                    newEmbed = discord.Embed(
                        description=kiss_text,
                        color=color
                    )
                else:
                    i = random.randint(0, len(kiss_list) - 1)
                    newEmbed = discord.Embed(description=kiss_list[i].format(
                        ctx.author.id, message.mentions[0].id), color=color)
                    await send_embed(ctx, newEmbed)

            elif len(message.mentions) < 5:
                kiss_text = (f"<@{ctx.author.id}> kissses")
                for member in message.mentions:
                    kiss_text += f" <@{member.id}> "
                newEmbed = discord.Embed(
                    description=kiss_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

            else:
                kiss_text = (f"<@{ctx.author.id}> distributes "
                             "smooches for a living.")
                newEmbed = discord.Embed(
                    description=kiss_text,
                    color=color
                )
                await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t execute that command.',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def reddit(self, ctx, sub: str):
        """Gets a hot post from a subreddit"""

        try:

            subreddit = await self.reddit.subreddit(sub)
            index = random.randint(1, 30)
            i = 0
            async for post in subreddit.hot(limit=30):
                i += 1
                if i == index:
                    newEmbed = discord.Embed(
                        title=post.title,
                        description=post.selftext,
                        color=color
                    )
                    newEmbed.set_footer(text=f'r/{sub}')
                    if not post.is_self:
                        newEmbed.set_image(url=post.url)
                    break

            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description="I couldn't fetch an image from that subreddit.",
                color=color
            )
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)


def setup(bot):
    bot.add_cog(Fun(bot))
