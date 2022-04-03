import discord
import config
from discord.ext import commands
from tools.tools import send_embed
from discord import Color

color = Color.blue()


class Help(commands.Cog):
    """The help message module"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *args):
        """Shows the bot's modules"""

        if not args:
            newEmbed = discord.Embed(
                title='Modules',
                color=color,
                description=(f'Use `{config.prefix}help <module>` to gain more'
                             ' information about that module'))

            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            newEmbed.add_field(name='Modules', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                newEmbed.add_field(
                    name='Not belonging to a module',
                    value=commands_desc, inline=False)

        elif len(args) == 1:

            for cog in self.bot.cogs:
                if cog.lower() == args[0].lower():

                    newEmbed = discord.Embed(
                        title=f'{cog} - Commands',
                        description=self.bot.cogs[cog].__doc__,
                        color=color)

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            newEmbed.add_field(
                                name=f"`{config.prefix}{command.name}`",
                                value=command.help,
                                inline=False)
                    break

            else:
                newEmbed = discord.Embed(
                    title="Module not found",
                    description=("I've never heard from a "
                                 f"module called `{input[0]}`"),
                    color=color)

        elif len(args) > 1:
            newEmbed = discord.Embed(
                title="Too many modules requested",
                description="Please request only one module at once",
                color=color)

        else:
            newEmbed = discord.Embed(
                title="Unknown error",
                description=("There was an error trying"
                             "to process your request"),
                color=color)

        await send_embed(ctx, newEmbed)


def setup(bot):
    bot.add_cog(Help(bot))
