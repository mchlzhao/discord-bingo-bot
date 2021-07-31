import discord
from discord.ext import commands

from bot.bot import bot

def char_to_emoji(c):
    return f':regional_indicator_{c.lower()}:'

def str_to_emoji(s):
    return ''.join(map(char_to_emoji, s))

@bot.command(name='embed')
async def embed_command(ctx):
    embed = discord.Embed(
        title='Sample embed'
    )
    embed.add_field(name='Player 1', value=str_to_emoji('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    await ctx.send(embed=embed)
