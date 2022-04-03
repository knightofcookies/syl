import pytz
from discord.errors import Forbidden


def convertUtcToIst(utctimeobject):
    obj = utctimeobject.replace(tzinfo=pytz.UTC)
    timeIST = obj.astimezone(pytz.timezone(
        'Asia/Kolkata')).strftime("%d/%m/%Y %H:%M")
    return timeIST


async def send_embed(ctx, newEmbed):
    try:
        await ctx.send(embed=newEmbed)
    except Forbidden:
        try:
            await ctx.send('I can\'t send embeds. '
                           'Please check my permissions.')
        except Forbidden:
            await ctx.author.send((f'I can\'t send messages in '
                                   f'{ctx.channel.name} on {ctx.guild.name}'))


async def send_embed_channel(message, newEmbed):
    try:
        await message.channel.send(embed=newEmbed)
    except Forbidden:
        try:
            await message.channel.send('I can\'t send embeds.'
                                       ' Please check my permissions.')
        except Forbidden:
            await message.author.send(f'I can\'t send messages in '
                                      f'{message.channel.name} on '
                                      f'{message.guild.name}')
