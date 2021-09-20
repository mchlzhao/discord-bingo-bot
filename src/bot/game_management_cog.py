from discord.ext import commands

from src.bot.base_cog import BaseCog
from src.bot.display_error import DisplayError
from src.bot.embed_generator import EmbedGenerator
from src.bot.util import (
    MAX_EVENTS)
from src.core.game_engine import GameEngine


class GameManagementCog(BaseCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='game.start',
                      aliases=['start', 'game.begin', 'begin'])
    async def start_game(self, ctx, *args):
        event_strs = list(map(str, args))
        if len(event_strs) == 0:
            raise DisplayError('You need to specify some events.')
        if len(event_strs) > MAX_EVENTS:
            raise DisplayError(f'There can only be up to {MAX_EVENTS} events.')
        response = self.engine.start_game(str(ctx.guild.id), event_strs)
        if response.display_error is not None:
            raise DisplayError(response.display_error)
        await ctx.send(
            embed=EmbedGenerator.get_start_embed(response.response['events']))

    @commands.command(name='game.finish',
                      aliases=['finish', 'game.end', 'end'])
    async def end_game(self, ctx):
        # TODO: present confirmation prompt
        response = self.engine.finish_game(str(ctx.guild.id))
        if response.display_error is not None:
            raise DisplayError(response.display_error)
        await ctx.send(
            embed=EmbedGenerator.get_end_embed(response.response['entries']))
