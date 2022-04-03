from discord.ext import commands
import discord
import datetime
import config
from discord import Colour
from tools.tools import send_embed, convertUtcToIst, send_embed_channel

syl_db = config.syl_db

# Adding Collections
afk_col = syl_db["afk"]

color = Colour.blue()


class AFK(commands.Cog):
    """Away from keyboard commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def afk(self, ctx, *, args=None):
        """Sets an AFK message"""

        try:
            # Assign the afk message
            if args is None:
                afkmsg = 'AFK'
            else:
                afkmsg = str(args)

            # Send confirmation to author
            newEmbed = discord.Embed(
                title='AFK Set',
                description=f"<@{ctx.author.id}>, I set your AFK : {afkmsg}",
                color=color)
            await send_embed(ctx, newEmbed)

            # Add a new entry to the afk_db
            time = convertUtcToIst(datetime.datetime.now())

            afk_col.update_one({'id': str(ctx.author.id)}, {"$set":
                               {'afkmsg': afkmsg, 'time': time}}, upsert=True)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I could not set your AFK!',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Removing the AFK
        x = afk_col.find_one({'id': str(message.author.id)})
        try:
            if x is not None:
                newEmbed = discord.Embed(
                    title='AFK Removed',
                    description=f'Welcome back {message.author}!',
                    color=color)
                await send_embed_channel(message, newEmbed)
                afk_col.delete_one({'id': str(message.author.id)})
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=(f'There was an error '
                             f'removing your AFK {message.author}'))
            newEmbed.set_footer(text=str(e))
            await send_embed_channel(message, newEmbed)

        # If an AFK user is pinged
        if message.mentions is not None:
            for member in message.mentions:
                y = afk_col.find_one({'id': str(member.id)})
                if y is not None:
                    try:
                        newEmbed = discord.Embed(
                            title='Member AFK',
                            description=f"{y['afkmsg']}",
                            color=color)
                        newEmbed.set_footer(text=f"<@{member.id}> is AFK since"
                                                 f"{y['time']}")
                        await send_embed_channel(message, newEmbed)
                    except Exception as e:
                        newEmbed = discord.Embed(
                            title='Error',
                            description='There was an error processing AFK(s)')
                        newEmbed.set_footer(text=str(e))
                        await send_embed_channel(message, newEmbed)


def setup(bot):
    bot.add_cog(AFK(bot))
