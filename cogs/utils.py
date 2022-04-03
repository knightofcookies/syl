import discord
from discord.ext import commands
from discord import Colour
from tools.tools import send_embed

color = Colour.blue()


class Utilities(commands.Cog):
    """A few utility commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Gets a user's avatar"""

        try:
            if member is None:
                member = ctx.author
            newEmbed = discord.Embed(
                title=f"{member.name}#{member.discriminator}"
            )
            newEmbed.set_image(
                url=member.avatar_url
            )
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description="I couldn't get that user's avatar!"
            )
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['e'])
    async def enlarge(self, ctx, emoji: discord.Emoji):
        """Enlarges an emoji"""

        try:
            newEmbed = discord.Embed(
                title='Emote'
            )
            newEmbed.set_image(
                url=emoji.url
            )
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description="I couldn't enlarge that emoji!"
            )
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)


def setup(bot):
    bot.add_cog(Utilities(bot))
