from discord.ext import commands
import discord
from discord import Colour
from tools.tools import send_embed

# Adding Dictionaries
isSnipe = {}
isEditsnipe = {}
snipeMessageContent = {}
editsnipeMessageContent = {}
snipeMessageAuthor = {}
editsnipeMessageAuthor = {}

color = Colour.blue()


class Misc(commands.Cog):
    """A few miscellaneous commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        isSnipe[message.channel.id] = True
        author = (f'{message.author.name}#{message.author.discriminator}')
        snipeMessageAuthor[message.channel.id] = author
        if message.content is not None:
            snipeMessageContent[message.channel.id] = message.content
        else:
            snipeMessageContent[message.channel.id] = ('`The deleted '
                                                       'message had no text.`')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):

        isEditsnipe[message_before.channel.id] = True
        author = (f'{message_before.author.name}#'
                  f'{message_before.author.discriminator}')
        editsnipeMessageAuthor[message_before.channel.id] = author
        if message_before.content is not None:
            content = message_before.content
            editsnipeMessageContent[message_before.channel.id] = content
        else:
            defaultmsg = '`The edited message had no text.`'
            editsnipeMessageContent[message_before.channel.id] = defaultmsg

    @commands.command()
    async def ping(self, ctx):
        """Gets the bot's current websocket latency"""

        newEmbed = discord.Embed(
            description=f'Pong! {round(self.bot.latency * 1000)}ms',
            color=color)
        await send_embed(ctx, newEmbed)

    @commands.command()
    async def snipe(self, ctx):
        """Snipes the last deleted message"""

        # If there's a pre-existing sniped messag
        if ctx.channel.id in isSnipe.keys():
            newEmbed = discord.Embed(
                description=snipeMessageContent[ctx.channel.id],
                color=color)
            newEmbed.set_footer(
                text=f"{snipeMessageAuthor[ctx.channel.id]}")
            await send_embed(ctx, newEmbed)

        # If there's nothing to snipe
        else:
            newEmbed = discord.Embed(
                description='There\'s nothing to snipe!',
                color=color)
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def editsnipe(self, ctx):
        """Snipes the last edited message"""

        # If there's a pre-existing sniped edited message
        if ctx.channel.id in isEditsnipe.keys():
            newEmbed = discord.Embed(
                description=editsnipeMessageContent[ctx.channel.id],
                color=color)
            newEmbed.set_footer(
                text=f"{editsnipeMessageAuthor[ctx.channel.id]}")
            await send_embed(ctx, newEmbed)

        # If there's nothing to editsnipe
        else:
            newEmbed = discord.Embed(
                description='There\'s no edit to snipe!', color=color)
            await send_embed(ctx, newEmbed)


def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
