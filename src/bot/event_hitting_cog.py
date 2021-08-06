import discord
from discord.ext import commands

from src.bot.util import (
    char_to_index, index_to_char)
from src.core.game_engine import GameEngine


class EventHittingCog(commands.Cog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='hit')
    async def hit(self, ctx, *args):
        server_id = ctx.guild.id
        search_str = ' '.join(args)
        if len(search_str) == 1 and search_str.isalpha():
            self.engine.hit(server_id, index=char_to_index(search_str))
        else:
            self.engine.hit(server_id, desc=search_str)
        embed = discord.Embed(
            title='HIT',
            description=f'Event has been hit'
        )
        await ctx.send(embed=embed)

    @commands.command(name='unhit')
    async def unhit(self, ctx, *args):
        server_id = ctx.guild.id
        search_str = ' '.join(args)
        if len(search_str) == 1 and search_str.isalpha():
            self.engine.unhit(server_id, index=char_to_index(search_str))
        else:
            self.engine.unhit(server_id, desc=search_str)
        embed = discord.Embed(
            title='HIT',
            description=f'Event has been unhit'
        )
        await ctx.send(embed=embed)
