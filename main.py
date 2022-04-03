# Importing things
import discord
import os
from discord.ext import commands
import config
from config import ka
from tools.tools import send_embed


# Defining 'bot'
bot = commands.Bot(case_insensitive=True,
                   command_prefix=config.prefix,
                   activity=discord.Game(name=f"{config.prefix}help"),
                   description='I\'m a simple music bot',
                   help_command=None,
                   intents=discord.Intents.all())

color = discord.Colour.blue()

# Printing to the console when the bot is ready


@bot.event
async def on_ready():
    print('Bot is ready.', bot.user)

# Loading cogs from the other files
for i in os.scandir(path="cogs"):
    if i.name.endswith(".py"):
        bot.load_extension(f'cogs.{i.name[:-3]}')

# Error handling


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        pass

    elif isinstance(error, commands.MissingRequiredArgument):
        newEmbed = discord.Embed(title='Error : Missing Argument',
                                 description=('Please enter all the arguments '
                                              'required to make '
                                              'the command work.'),
                                 color=color)
        await send_embed(ctx, newEmbed)

    elif isinstance(error, commands.BotMissingPermissions):
        newEmbed = discord.Embed(title='Missing Permissions',
                                 description=('I don\'t have the '
                                              'required permissions to '
                                              'run this command.'),
                                 color=color)
        await send_embed(ctx, newEmbed)

    elif isinstance(error, commands.BadArgument):
        newEmbed = discord.Embed(
            title='Bad Argument',
            description='One or more of the arguments you entered is invalid.',
            color=color)
        await send_embed(ctx, newEmbed)

    else:
        newEmbed = discord.Embed(
            title='Error', description=str(error), color=color)
        await send_embed(ctx, newEmbed)

# Keeping the bot alive
ka()

# Running the bot
bot.run(config.token)
